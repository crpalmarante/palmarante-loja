#!/bin/bash
# ============================================================
# Deploy do Sistema RH (Python + COBOL + Apache2)
# Uso: ./deploy.sh [caminho_destino]
# Default: diretorio atual
# ============================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[ERRO]${NC} $1"; exit 1; }

DIR="${1:-$(pwd)}"
SERVICE_NAME="palmarante-rh"
APACHE_CONF="palmarante-rh"
SERVER_PORT=8080
SERVER_USER="${SUDO_USER:-www-data}"
SERVER_GROUP="${SUDO_USER:-www-data}"

[[ $EUID -eq 0 ]] && SUDO="" || SUDO="sudo"

echo "=============================================="
echo "  Deploy Sistema RH - Palmarante"
echo "  Destino: $DIR"
echo "  Porta interna: $SERVER_PORT"
echo "=============================================="
echo ""

# ---------- Verificacoes ----------
[[ ! -f "$DIR/server.py" ]] && err "server.py nao encontrado em $DIR"

command -v python3     >/dev/null || err "Python3 nao encontrado"
command -v cobc        >/dev/null || err "GnuCOBOL (cobc) nao encontrado"
command -v apache2     >/dev/null || warn "Apache2 nao encontrado (proxy sera pulado)"
command -v systemctl   >/dev/null || warn "systemctl nao encontrado (service sera pulado)"

PYVER=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
log "Python $PYVER encontrado"

# ---------- 1. Compilar COBOL ----------
echo ""
echo "--- [1/5] Compilando COBOL ---"
cd "$DIR"
make compilar 2>&1 | grep -v warning || err "Falha na compilacao COBOL"
log "COBOL compilado"

# ---------- 2. Criar diretorios de dados ----------
echo ""
echo "--- [2/5] Diretorios de dados ---"
mkdir -p "$DIR/dados" "$DIR/uploads/funcionarios" "$DIR/uploads/comprovantes"
chmod -R 755 "$DIR/dados" "$DIR/uploads"
log "Diretorios criados"

# ---------- 3. systemd service ----------
echo ""
echo "--- [3/5] systemd service ---"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

$SUDO tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Palmarante RH - Servidor Web Python/COBOL
After=network.target apache2.service
Wants=apache2.service

[Service]
Type=simple
User=$SERVER_USER
Group=$SERVER_GROUP
WorkingDirectory=$DIR
ExecStart=/usr/bin/python3 $DIR/server.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

$SUDO systemctl daemon-reload 2>/dev/null || true
log "Service criado: $SERVICE_FILE"
warn "Ativar com: $SUDO systemctl enable --now $SERVICE_NAME"

# ---------- 4. Apache2 Reverse Proxy ----------
echo ""
echo "--- [4/5] Apache2 Reverse Proxy ---"

if command -v apache2 &>/dev/null; then
    $SUDO a2enmod proxy proxy_http rewrite ssl headers 2>/dev/null || true

    VHOST_FILE="/etc/apache2/sites-available/${APACHE_CONF}.conf"

    $SUDO tee "$VHOST_FILE" > /dev/null << APEOF
<VirtualHost *:80>
    ServerName 177.190.69.20
    ServerAdmin admin@palmarante.com.br

    ErrorLog \${APACHE_LOG_DIR}/palmarante-rh-error.log
    CustomLog \${APACHE_LOG_DIR}/palmarante-rh-access.log combined

    # Tudo via proxy reverso para o Python server
    # (mais seguro: .cbl, .dat, .json nunca expostos)
    ProxyPreserveHost On

    ProxyPass / http://127.0.0.1:$SERVER_PORT/
    ProxyPassReverse / http://127.0.0.1:$SERVER_PORT/

    <Proxy http://127.0.0.1:$SERVER_PORT/*>
        Require all granted
    </Proxy>
</VirtualHost>
APEOF

    $SUDO a2dissite 000-default.conf 2>/dev/null || true
    $SUDO a2ensite ${APACHE_CONF}.conf 2>/dev/null || true
    $SUDO systemctl reload apache2 2>/dev/null || true

    log "Apache configurado: $VHOST_FILE"
    warn "Para HTTPS: sudo certbot --apache -d 177.190.69.20"
else
    warn "Apache2 nao encontrado. Configure o proxy manualmente ou execute:"
    warn "  sudo python3 server.py     # servira na porta 8080"
fi

# ---------- 5. Final ----------
echo ""
echo "--- [5/5] Finalizando ---"

# Copiar deploy.sh para o destino se executou de outro lugar
[[ "$DIR" != "$(pwd)" ]] && cp "$0" "$DIR/deploy.sh" 2>/dev/null || true

echo ""
echo "=============================================="
echo "  DEPLOY CONCLUIDO!"
echo "=============================================="
echo ""
echo "  Para iniciar o servico agora:"
echo "    $SUDO systemctl enable --now $SERVICE_NAME"
echo ""
echo "  Para ver logs:"
echo "    $SUDO journalctl -u $SERVICE_NAME -f"
echo ""
echo "  Para testar localmente:"
echo "    curl http://localhost:8080"
echo ""
echo "  Para testar via Apache:"
echo "    curl http://177.190.69.20"
echo ""
echo "  Para recarregar Apache apos alteracoes:"
echo "    $SUDO systemctl reload apache2"
echo ""
echo "  Para HTTPS (Let's Encrypt):"
echo "    $SUDO apt install certbot python3-certbot-apache"
echo "    $SUDO certbot --apache -d 177.190.69.20"
echo ""
echo "  Uso do deploy.sh:"
echo "    ./deploy.sh                    # deploy no diretorio atual"
echo "    ./deploy.sh /caminho/para/rh   # deploy em outro diretorio"
echo ""
