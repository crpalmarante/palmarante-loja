# Deploy - Sistema RH Palmarante

## Requisitos no servidor (177.190.69.20)

```bash
sudo apt update
sudo apt install -y python3 gnucobol apache2
```

## Passo a passo

### 1. Copiar os arquivos para o servidor

Do seu computador para o servidor remoto:

```bash
# No seu computador (maquina de desenvolvimento)
scp -r /home/palmarante/projetos_cobol/palmarante-loja usuario@177.190.69.20:/home/usuario/palmarante-loja
```

Ou se ja estiver no servidor, apenas navegue ate o diretorio.

### 2. Executar o deploy

```bash
cd /home/usuario/palmarante-loja
sudo bash deploy.sh
```

O script faz automaticamente:

| Etapa | O que faz |
|---|---|
| 1/5 | Compila todos os programas COBOL |
| 2/5 | Cria diretorios de dados (`dados/`, `uploads/`) |
| 3/5 | Cria servico **systemd** (`palmarante-rh.service`) |
| 4/5 | Configura **Apache2** como proxy reverso |
| 5/5 | Finaliza permissoes |

### 3. Iniciar o servico

```bash
sudo systemctl enable --now palmarante-rh
sudo systemctl reload apache2
```

### 4. Testar

```bash
curl http://177.190.69.20
```

## Arquitetura

```
Internet ──▶ Apache2 (porta 80)
                │
                ├── Arquivos estaticos (.html, .css, .js) ──▶ direto
                │
                └── /api/* ──▶ ProxyReverse ──▶ Python (porta 8080)
                                                    │
                                                    ├── server.py
                                                    ├── COBOL binaries
                                                    └── dados/ (JSON + .dat)
```

## Comandos uteis

```bash
# Ver status do servico
sudo systemctl status palmarante-rh

# Ver logs em tempo real
sudo journalctl -u palmarante-rh -f

# Reiniciar servico apos alteracoes
sudo systemctl restart palmarante-rh

# Logs do Apache
sudo tail -f /var/log/apache2/palmarante-rh-*.log
```

## HTTPS (recomendado)

```bash
sudo apt install -y certbot python3-certbot-apache
sudo certbot --apache -d 177.190.69.20
```

## Solucao de problemas

| Problema | Causa provavel | Solucao |
|---|---|---|
| `502 Bad Gateway` | Python nao rodando | `sudo systemctl restart palmarante-rh` |
| `File not found` | Caminho errado | Verificar `WorkingDirectory` no systemd |
| COBOL erro | Nao compilado | Rodar `make compilar` no diretorio |
| Permissao negada | Dono do arquivo errado | `sudo chown -R www-data:www-data dados/ uploads/` |

## Remocao

```bash
sudo systemctl stop palmarante-rh
sudo systemctl disable palmarante-rh
sudo rm /etc/systemd/system/palmarante-rh.service
sudo a2dissite palmarante-rh
sudo rm /etc/apache2/sites-available/palmarante-rh.conf
sudo systemctl daemon-reload
```
