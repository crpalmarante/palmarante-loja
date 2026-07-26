# Capítulo 15 — Icon System (Sistema de Ícones)

## Visão Geral

O Icon System define os padrões para utilização de ícones em todo o FiscalUI Framework.

Os ícones representam ações, estados, objetos e categorias da aplicação, complementando a interface visual sem substituir textos importantes.

Todo ícone deve possuir significado consistente, aparência uniforme e integração completa com os demais componentes do Framework.

---

# Objetivos

O Icon System possui os seguintes objetivos:

- Padronizar toda a iconografia do Framework.
- Melhorar a identificação das ações.
- Reduzir carga cognitiva.
- Facilitar aprendizado da interface.
- Integrar-se ao Theme Engine.
- Garantir acessibilidade.

---

# Filosofia

Os ícones complementam a informação.

Nunca substituem completamente o texto.

Exemplo correto

```
🖨 Imprimir
```

Evitar

```
🖨
```

Exceto quando houver Tooltip e ARIA.

---

# Arquitetura

```
Icon System

│

├── Biblioteca SVG

├── Tokens

├── Categorias

├── Estados

├── Temas

├── Acessibilidade

└── API JavaScript
```

---

# Tecnologia

O FiscalUI utiliza exclusivamente SVG.

Não utilizar:

- PNG
- JPG
- GIF
- Font Icons

SVG oferece:

- Escalabilidade
- Melhor desempenho
- Menor consumo
- Personalização por CSS
- Compatibilidade com temas

---

# Estrutura

```
assets/

icons/

navigation/

actions/

status/

files/

users/

finance/

fiscal/

dashboard/

system/
```

---

# Categorias

## Navegação

```
Home

Menu

Voltar

Avançar

Pesquisar

Filtros

Configurações
```

---

## Ações

```
Novo

Salvar

Editar

Excluir

Duplicar

Cancelar

Confirmar

Atualizar

Exportar

Importar

Imprimir
```

---

## Fiscal

```
NF-e

NFC-e

CT-e

MDF-e

NCM

CFOP

IBS

CBS

ICMS

IPI

PIS

COFINS
```

---

## Empresas

```
Empresa

Filial

Cliente

Fornecedor

Transportadora

Representante
```

---

## Produtos

```
Produto

Estoque

Código de Barras

Lote

Validade

Unidade

Preço
```

---

## Financeiro

```
Caixa

Banco

PIX

Boleto

Dinheiro

Cartão

Receber

Pagar
```

---

## Dashboard

```
KPIs

Gráficos

Indicadores

Relatórios

Alertas

Performance
```

---

# Estilo

Todos os ícones seguem o mesmo padrão.

Características

- Linhas arredondadas
- Cantos suaves
- Espessura uniforme
- Geometria consistente
- Visual minimalista

Inspirado em:

- Odoo 19
- Fluent UI
- Heroicons
- Lucide
- Material Symbols

---

# Espessura

Padrão

```
2px
```

Nunca misturar espessuras.

---

# Tamanhos

```
XS

16 px
```

---

```
SM

20 px
```

---

```
MD

24 px
```

Padrão do Framework.

---

```
LG

32 px
```

---

```
XL

48 px
```

---

```
XXL

64 px
```

---

# Tokens

Os ícones utilizam Design Tokens.

```
Icon Color

Icon Hover

Icon Disabled

Icon Active

Icon Size

Icon Stroke
```

Nunca definir cores diretamente.

---

# Estados

Todos os ícones possuem estados.

```
Default

Hover

Focus

Active

Disabled

Loading
```

---

# Cores

As cores são definidas pelo Theme Engine.

Exemplo

```
Light

Cinza Escuro
```

```
Dark

Cinza Claro
```

```
Glass

Branco Translúcido
```

---

# Ícones Animados

Alguns ícones podem utilizar Motion Design.

Exemplos

```
Loading

Rotação

↓

Refresh

Rotação

↓

Download

Pequeno movimento
```

Nunca utilizar animações decorativas.

---

# Botões

Todo botão pode possuir.

```
Ícone

↓

Texto
```

ou

```
Somente Ícone
```

Neste caso

Tooltip obrigatório.

ARIA obrigatório.

---

# Sidebar

Modo Expandido

```
📦 Produtos
```

Modo Compacto

```
📦
```

Tooltip obrigatório.

---

# Data Grid

Ações rápidas.

```
Editar

Excluir

Visualizar

Duplicar

Imprimir
```

Sempre alinhadas.

---

# Dashboard

Os KPIs utilizam ícones.

Exemplo

```
📈 Receita

📦 Produtos

👥 Clientes

🧾 NF-e
```

---

# Cores Semânticas

Os ícones podem utilizar cores semânticas.

```
Sucesso

Verde
```

```
Erro

Vermelho
```

```
Aviso

Amarelo
```

```
Informação

Azul
```

Essas cores vêm do Theme Engine.

---

# Acessibilidade

Todo ícone deve possuir:

- aria-label
- Tooltip (quando isolado)
- Contraste adequado
- Área mínima de clique

---

# Área de Clique

Mesmo um ícone pequeno deve possuir área mínima.

```
44 x 44 px
```

Conforme recomendações de acessibilidade.

---

# Performance

Todos os SVGs devem ser:

- otimizados
- sem atributos desnecessários
- reutilizáveis
- carregados sob demanda

---

# API JavaScript

O Icon Manager controla.

```
Registrar

↓

Carregar

↓

Cache

↓

Renderizar

↓

Atualizar
```

---

# Exemplo HTML

```html
<button class="ui-button">

<svg class="ui-icon">

...

</svg>

<span>

Salvar

</span>

</button>
```

---

# Estrutura dos Arquivos

```
icons/

save.svg

edit.svg

delete.svg

refresh.svg

print.svg

download.svg

upload.svg

user.svg

company.svg

nfe.svg

nfce.svg

dashboard.svg

report.svg
```

---

# Integração

O Icon System integra-se com:

- Theme Engine
- Motion Design
- Accessibility Framework
- Component Library
- JavaScript Core

---

# Boas Práticas

✔ Utilizar SVG.

✔ Utilizar Design Tokens.

✔ Manter proporções.

✔ Utilizar nomes padronizados.

✔ Reutilizar ícones.

✔ Respeitar acessibilidade.

---

# O que evitar

✖ Misturar estilos.

✖ Utilizar imagens raster.

✖ Alterar espessuras.

✖ Utilizar ícones sem significado.

✖ Excesso de detalhes.

---

# Roadmap Futuro

O Icon System será expandido com:

- Biblioteca oficial FiscalUI Icons.
- Editor de ícones.
- Pacote NPM.
- SVG Sprite automático.
- Suporte a temas personalizados.
- Catálogo visual online.

---

# Conclusão

O Icon System estabelece uma linguagem visual única para o FiscalUI Framework.

Ao padronizar formato, estilo, tamanhos, estados e integração com o Theme Engine, o Framework garante uma experiência consistente, moderna e acessível em todos os módulos do ERP.

Os ícones deixam de ser simples elementos gráficos e passam a fazer parte da arquitetura visual do sistema, contribuindo para a produtividade, usabilidade e identidade do FiscalUI.
