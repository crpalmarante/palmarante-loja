# Plano do Sistema POS + Fiscal (Palmarante Loja)

## Arquitetura

```
Browser (pos.html)
    |
    | HTTP REST
    v
server.py (Python HTTP)
    |
    |--- chamada COBOL (subprocess) ---> .dat (fonte de verdade)
    |       |
    |       +--- cadastrar_produto.cbl        produtos.dat
    |       +--- registrar_venda.cbl          vendas.dat + itens_venda.dat
    |       +--- finalizar_pedido.cbl         vendas.dat (altera forma_pg)
    |       +--- gerir_empresa.cbl            empresa.dat
    |       +--- gerir_filiais.cbl            filiais.dat
    |       +--- gerir_funcionarios.cbl       funcionarios.dat
    |       +--- gerir_usuarios.cbl           usuarios.dat
    |       +--- gerir_atributos.cbl          atributos.dat
    |       +--- gerir_imagens.cbl            produto_imagens.dat
    |       +--- gerir_numeracao.cbl          numeracao.dat
    |       +--- batch_json_produtos.cbl      produtos.json
    |       +--- batch_json_vendas.cbl        vendas.json
    |       +--- batch_json_numeracao.cbl     numeracao.json
    |
    |--- fiscal/ (Python nativo - XML, assinatura, transmissao)
    |       |
    |       +--- config.py        Config. empresa + numeracao + CRT
    |       +--- certificado.py   Carregar/validar A1 (PFX/P12)
    |       +--- assinatura.py    Assinatura XML (signxml)
    |       +--- nfce.py          NFC-e XML (mod 65)
    |       +--- nfe.py           NF-e XML (mod 55)
    |       +--- danfe.py         DANFE/DANFE-NFC-e HTML
    |       +--- transmissao.py   SOAP SEFAZ
    |
    |--- dados/
            +--- *.dat (COBOL)  fonte de verdade
            +--- *.json (cached para web)
```

## Fluxo de Vendas

```
POS (Vender)              Caixa                    Fiscal
    |                        |                        |
    |-- Cria pedido -------->|                        |
    |   (PENDENTE)           |                        |
    |                        |-- Split payment        |
    |                        |-- Finalizar cobranca   |
    |                        |---------->             |
    |                        |            Emitir NFC-e (CPF/consumidor)
    |                        |            Emitir NF-e  (CNPJ)
    |                        |            Salvar em nfce.json / nfe.json
    |                        |            Gerar DANFE HTML
```

## Dados da Empresa (empresa.dat)

| Campo | Tipo | Descricao |
|---|---|---|
| nome | X(50) | Nome fantasia |
| cnpj | X(18) | CNPJ formatado |
| endereco | X(50) | Logradouro completo |
| telefone | X(15) | Telefone |
| email | X(40) | E-mail |
| certificado | X(100) | Caminho .pfx/.p12 |
| cert_senha | X(50) | Senha do certificado |
| cnpj_status | X(1) | S/N/P |
| inscricao_est | X(20) | Inscricao Estadual |
| logo | X(100) | Path do logo |
| cnae_prim_codigo | X(10) | CNAE primario |
| cnae_prim_desc | X(80) | Descricao CNAE primario |
| cnae_sec_codigos | X(100) | CNAEs secundarios |
| cnae_sec_desc | X(200) | Descricoes secundarias |
| tipo_fiscal | X(20) | Simples Nacional, Lucro Presumido, etc. |
| chave_pix | X(50) | Chave PIX |
| crt | 9(1) | CRT (1=SN, 2=SN excesso, 3=Normal) |

## Produto (produtos.dat)

| Campo | Tipo | Descricao |
|---|---|---|
| id | 9(6) | ID unico |
| nome | X(50) | Nome |
| preco | 9(7)V99 | Preco venda |
| preco_custo | 9(7)V99 | Preco custo |
| stock | 9(6) | Quantidade em stock |
| margem | 9(3)V99 | Margem % |
| ativo | X(1) | S/N |
| codigo_barras | X(14) | Codigo de barras |
| categoria | X(20) | Categoria |
| sub_categoria | X(20) | Sub-categoria |
| unidade | X(4) | UN, KG, L, CX, PC |
| ncm | X(8) | NCM fiscal |
| fornecedor | X(30) | Fornecedor |
| localizacao | X(15) | Localizacao no estoque |
| filial_id | 9(3) | Filial (0=matriz/todas) |
| **cst** | X(3) | CST/CSOSN (400, 500, 00, 40, etc.) |
| **cfop** | X(4) | CFOP (5102, 6102, etc.) |
| **icms_alq** | 9(3)V99 | Aliquota ICMS % |

## Numeracao (numeracao.dat)

| Campo | Tipo | Descricao |
|---|---|---|
| ambiente | 9(1) | 1=producao, 2=homologacao |
| serie_nfce | 9(3) | Serie NFC-e |
| prox_num_nfce | 9(9) | Proximo numero NFC-e |
| serie_nfe | 9(3) | Serie NF-e |
| prox_num_nfe | 9(9) | Proximo numero NF-e |

## Menu do POS

| Botão | Funcionalidade |
|---|---|
| Vender | PDV com carrinho, barcode, desconto |
| Produtos | Cadastro de produtos (formulario) |
| Vendas | Historico com filtros (Todos/Vendas/Orcamentos/Pendentes) |
| Relatorios | Saida COBOL |
| Caixa | Pedidos pendentes + split payment + PIX |
| Configuracoes | Empresa, filiais, fiscal, numeracao |

## Regra de Documento Fiscal

| Cenario | Documento |
|---|---|
| Consumidor final (CPF ou sem doc) | NFC-e (mod 65) |
| Pessoa juridica (CNPJ) | NF-e (mod 55) |
| Itens com servico=S | NFS-e + NFC-e/NF-e |
| Orcamento | Nenhum |

## Chave de Acesso

Formato: `cUF(2) + AAMM(2) + CNPJ(14) + mod(2) + serie(3) + nNF(9) + tpEmis(1) + cNF(8) + cDV(1)`

## Dependencias Python

```
cryptography         49.0.0
lxml                  6.1.1
signxml               5.1.0
zeep                  4.3.3
Jinja2                3.1.2
requests
```

## Endpoints REST

### GET
| Rota | Resposta |
|---|---|
| `/api/produtos` | Lista produtos + atributos |
| `/api/vendas` | Lista vendas com itens |
| `/api/empresa` | Dados empresa |
| `/api/filiais` | Lista filiais |
| `/api/funcionarios` | Lista funcionarios |
| `/api/usuarios` | Lista usuarios |
| `/api/atributos?produto_id=X` | Atributos do produto |
| `/api/produto/imagens?produto_id=X` | Imagens do produto |
| `/api/ncm?q=...` | Autocomplete NCM |
| `/api/pedidos-pendentes` | Vendas PENDENTE |
| `/api/fiscal/config` | Configuracao fiscal completa |
| `/api/numeracao` | Numeracao atual |
| `/api/nfce/{venda_id}` | Status NFC-e |
| `/api/nfce/{venda_id}/danfe` | DANFE NFC-e HTML |
| `/api/nfe/{venda_id}` | Status NF-e |
| `/api/nfe/{venda_id}/danfe` | DANFE NF-e HTML |

### POST
| Rota | Body | Funcao |
|---|---|---|
| `/api/produto/incluir` | form-urlencoded | Cadastrar produto |
| `/api/produto/alterar` | form-urlencoded | Alterar produto |
| `/api/produto/excluir` | form-urlencoded | Excluir produto |
| `/api/venda/registrar` | form-urlencoded | Registrar venda |
| `/api/empresa/gravar` | form-urlencoded | Salvar empresa |
| `/api/filial/incluir` | form-urlencoded | Incluir filial |
| `/api/filial/alterar` | form-urlencoded | Alterar filial |
| `/api/filial/excluir` | form-urlencoded | Excluir filial |
| `/api/funcionario/incluir` | form-urlencoded | Incluir funcionario |
| `/api/funcionario/alterar` | form-urlencoded | Alterar funcionario |
| `/api/funcionario/excluir` | form-urlencoded | Excluir funcionario |
| `/api/usuario/incluir` | form-urlencoded | Incluir usuario |
| `/api/usuario/alterar` | form-urlencoded | Alterar usuario |
| `/api/usuario/excluir` | form-urlencoded | Excluir usuario |
| `/api/login` | form-urlencoded | Login (unificado) |
| `/api/atributo/incluir` | form-urlencoded | Incluir atributo |
| `/api/atributo/alterar` | form-urlencoded | Alterar atributo |
| `/api/atributo/excluir` | form-urlencoded | Excluir atributo |
| `/api/produto/imagem/incluir` | form-urlencoded | Incluir imagem |
| `/api/produto/imagem/excluir` | form-urlencoded | Excluir imagem |
| `/api/pedido/finalizar` | form-urlencoded | Finalizar pedido (caixa) |
| `/api/numeracao/gravar` | form-urlencoded | Salvar numeracao |
| `/api/nfce/emitir` | venda_id=X | Emitir NFC-e |
| `/api/nfe/emitir` | venda_id=X | Emitir NF-e |

## Status dos Proximos Passos

| Item | Status |
|---|---|
| 1. **NFS-e** | ✅ Implementado (ABRASF 2.04, `fiscal/nfse.py`) |
| 2. **Transmissao real SEFAZ** | ✅ Implementado (SOAP, `fiscal/transmissao.py`) |
| 3. **Cancelamento** | ✅ Implementado (evento 110111, `fiscal/evento.py`) |
| 4. **Carta de Correcao (CC-e)** | ✅ Implementado (evento 110110, `fiscal/evento.py` + endpoint + frontend) |
| 5. **Relatorio fiscal** | ✅ Implementado (`fiscal/relatorio_fiscal.py` + endpoints + frontend faturamento.html) |
| 6. **Sped Fiscal** | ✅ Implementado (`fiscal/sped.py` + endpoints) |
| 7. **Modo contingencia** | ✅ Implementado (`fiscal/contingencia.py` + endpoints) |
| 8. **Multi-UF** | ✅ Implementado (UF configurável + todos 27 estados nos WS SEFAZ) |
| 9. **Dashboard fiscal** | ✅ Melhorado (`faturamento.html` com apuração completa) |
| 10. **Integracao contabil** | ✅ Implementado (planocontas.json + diarios.json + endpoints) |

---

*Ultima atualizacao: 2026-07-18*
