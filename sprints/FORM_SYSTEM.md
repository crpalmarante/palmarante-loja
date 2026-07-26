# Capítulo 16 — Form System (Sistema de Formulários)

## Visão Geral

O Form System define a arquitetura, os componentes e as diretrizes para criação de formulários no FiscalUI Framework.

Seu objetivo é garantir que todos os formulários do ERP apresentem comportamento uniforme, aparência consistente e integração completa com os demais módulos do Framework.

Os formulários são considerados componentes de primeira classe da arquitetura.

---

# Objetivos

O Form System possui os seguintes objetivos:

• Padronizar formulários.

• Facilitar manutenção.

• Melhorar produtividade.

• Reduzir erros de preenchimento.

• Garantir acessibilidade.

• Integrar com JavaScript Core.

• Preparar comunicação com Backend.

---

# Filosofia

Todo formulário deve ser:

• Simples

• Consistente

• Responsivo

• Acessível

• Reutilizável

• Independente das regras de negócio

---

# Arquitetura

```
Application

↓

Workspace

↓

Form Container

↓

Sections

↓

Groups

↓

Fields

↓

Validation

↓

Backend
```

---

# Estrutura

Todo formulário segue a mesma organização.

```
Título

↓

Toolbar

↓

Dados Gerais

↓

Informações Complementares

↓

Anexos

↓

Observações

↓

Rodapé
```

---

# Containers

O formulário é composto por:

```
Form

↓

Section

↓

Field Group

↓

Field

↓

Actions
```

---

# Organização

Exemplo

```
Cadastro de Clientes

──────────────────────────

Dados Gerais

Endereço

Contato

Fiscal

Financeiro

Observações
```

Cada bloco é uma Section.

---

# Grid

Todos os formulários utilizam o Grid oficial.

Desktop

```
Nome              CPF

Cidade            UF
```

Tablet

```
Nome

CPF

Cidade

UF
```

Mobile

```
Nome

CPF

Cidade

UF
```

---

# Componentes

O Form System fornece:

```
Input

Textarea

Select

Autocomplete

Checkbox

Radio

Switch

Date

Time

DateTime

Money

Percent

Upload

Color

Password

Email

Telefone

CPF

CNPJ

CEP

NCM

CFOP

IBGE

IE

IM

PIX
```

---

# Campos Especializados

O FiscalUI fornece componentes próprios para documentos brasileiros.

Exemplos

```
CPF

CNPJ

CEP

Inscrição Estadual

NCM

CFOP

CST

IBS

CBS

Município IBGE
```

Todos possuem máscara e validação visual.

---

# Estados

Todo campo possui estados.

```
Default

Hover

Focus

Filled

Readonly

Disabled

Loading

Success

Warning

Error
```

---

# Label

Todo campo deve possuir Label.

Correto

```
Nome

[____________]
```

Evitar

```
Placeholder

Nome
```

Placeholder não substitui Label.

---

# Campo Obrigatório

Campos obrigatórios devem indicar isso visualmente.

Exemplo

```
Nome *

```

Sem depender apenas da cor.

---

# Placeholder

Placeholder apenas complementa.

Exemplo

```
Digite o nome completo
```

Nunca identificar o campo.

---

# Ajuda

Todo campo pode possuir.

```
Ícone ?

↓

Tooltip

↓

Ajuda
```

---

# Validação

O Form System possui apenas validação de interface.

Exemplos

Campo vazio.

Formato.

Quantidade.

Máscara.

Obrigatoriedade.

As regras fiscais pertencem ao Backend.

---

# Máscaras

Suporte nativo.

```
CPF

000.000.000-00
```

```
CNPJ

00.000.000/0000-00
```

```
CEP

00000-000
```

```
Telefone

(00) 00000-0000
```

```
Moeda

1.234,56
```

```
Percentual

99,99%
```

---

# Autocomplete

Campos podem utilizar pesquisa dinâmica.

Exemplo

```
Cliente

↓

Digite

↓

Lista

↓

Selecionar
```

---

# Select

Tipos

```
Single

Multi

Searchable

Grouped
```

---

# Upload

Suporta

```
Imagem

PDF

XML

ZIP

Planilhas

Documentos
```

---

# Calendário

Componentes

```
Date

Time

DateTime

Range
```

---

# Layout

Formulários utilizam Sections.

```
Dados Gerais

────────────────

Endereço

────────────────

Contato

────────────────

Fiscal
```

---

# Toolbar

Ações principais.

```
Novo

Salvar

Cancelar

Duplicar

Excluir

Imprimir
```

Sempre posicionada no topo.

---

# Navegação

TAB segue ordem lógica.

ENTER pode avançar.

ESC fecha modais.

---

# Atalhos

```
CTRL + S

Salvar
```

```
CTRL + N

Novo
```

```
CTRL + P

Imprimir
```

```
CTRL + F

Pesquisar
```

---

# Mensagens

Tipos

```
Erro

Aviso

Sucesso

Informação
```

Sempre próximas ao campo.

---

# Grupos

Campos relacionados permanecem agrupados.

Exemplo

```
Endereço

Rua

Número

Cidade

UF

CEP
```

---

# Campos Somente Leitura

Visualmente diferentes.

Permitem seleção de texto.

Não recebem foco desnecessário.

---

# Formulários Longos

Utilizar.

```
Accordion

Tabs

Stepper

Sections
```

Nunca páginas extremamente longas.

---

# Integração

Fluxo

```
Usuário

↓

Formulário

↓

JavaScript Core

↓

API REST

↓

Python

↓

COBOL

↓

PostgreSQL
```

---

# Persistência

O formulário nunca grava diretamente.

Fluxo

```
Salvar

↓

Service

↓

API

↓

Backend

↓

Resposta

↓

Interface
```

---

# Performance

Utilizar.

Lazy Loading

Autocomplete

Virtualização

Cache

Validação incremental

---

# Acessibilidade

Todos os campos possuem.

Label.

ARIA.

Foco.

Mensagens.

Contraste.

Teclado.

---

# Responsividade

Desktop

2 ou 3 colunas.

Tablet

2 colunas.

Mobile

1 coluna.

---

# Temas

Todos os campos adaptam-se automaticamente aos temas.

```
Light

Dark

Glass

Corporate
```

---

# Componentes Compostos

Exemplos.

```
Endereço

↓

CEP

↓

Pesquisa

↓

Preenchimento automático
```

---

```
Empresa

↓

CNPJ

↓

Consulta

↓

Dados
```

---

# Eventos

Todos os campos emitem eventos.

```
Focus

Blur

Change

Input

Select

Validate

Clear
```

Nunca comunicam diretamente com outros componentes.

---

# Estrutura de Arquivos

```
components/

form/

input/

textarea/

select/

autocomplete/

upload/

datepicker/

money/

cpf/

cnpj/

cep/

validation/
```

---

# Boas Práticas

✔ Labels sempre visíveis.

✔ Campos agrupados.

✔ Máscaras padronizadas.

✔ Validação amigável.

✔ Mensagens claras.

✔ Navegação por teclado.

✔ Layout consistente.

✔ Uso de Design Tokens.

---

# O que evitar

✖ Labels ocultos.

✖ Placeholder como Label.

✖ Mensagens genéricas.

✖ Campos desalinhados.

✖ Formulários excessivamente longos.

✖ Máscaras inconsistentes.

✖ JavaScript acoplado ao Backend.

---

# Roadmap

O Form System será expandido com:

• Form Builder visual.

• Editor Drag-and-Drop.

• Validação declarativa.

• Componentes inteligentes.

• Assistente de formulários.

• Gerador automático de CRUD.

---

# Conclusão

O Form System estabelece um padrão único para todos os formulários do FiscalUI Framework.

Ao separar estrutura, apresentação, comportamento e integração com o Backend, o Framework garante formulários consistentes, reutilizáveis, acessíveis e preparados para aplicações corporativas de grande porte.

Sua arquitetura permite integração transparente com serviços em Python, COBOL e PostgreSQL, preservando a independência do Frontend e a evolução futura do sistema.
