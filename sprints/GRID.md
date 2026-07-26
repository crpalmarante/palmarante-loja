# Capítulo 08 — Sistema de Grid

## Conceito

O Sistema de Grid é responsável por organizar toda a distribuição espacial dos componentes do FiscalUI.

Nenhum componente define sua própria posição na tela.

Todos os componentes ocupam regiões previamente definidas pelo Grid.

Isso garante:

- alinhamento consistente
- espaçamento uniforme
- responsividade
- facilidade de manutenção

---

# Objetivos

O Grid possui cinco objetivos principais.

• Padronizar o layout

• Facilitar a criação de telas

• Adaptar automaticamente aos dispositivos

• Evitar CSS específico por página

• Maximizar o reaproveitamento dos componentes

---

# Filosofia

O Grid não pertence ao componente.

O componente pertence ao Grid.

Ou seja:

Primeiro define-se a estrutura.

Depois inserem-se os componentes.

Nunca o contrário.

---

# Estrutura

O FiscalUI utiliza um Grid baseado em 12 colunas.

```text
┌───────────────────────────────────────────────┐

1 2 3 4 5 6 7 8 9 10 11 12

└───────────────────────────────────────────────┘
```

As colunas possuem largura variável.

Os espaços entre colunas são chamados de Gutter.

---

# Breakpoints

Desktop XL

≥1600px

Desktop

≥1280px

Notebook

≥1024px

Tablet

≥768px

Mobile

<768px

---

# Distribuição

Exemplo

```text
┌──────────────────────────────────────────────┐

████████████

12

└──────────────────────────────────────────────┘
```

---

Metade

```text
██████ ██████

6      6
```

---

Terços

```text
████ ████ ████

4     4    4
```

---

Quartos

```text
███ ███ ███ ███

3   3   3   3
```

---

# Grid Responsivo

Desktop

```text
┌─────────────────────────────────────┐

□ □ □ □

└─────────────────────────────────────┘
```

Tablet

```text
┌────────────────────────────┐

□ □

□ □

└────────────────────────────┘
```

Mobile

```text
┌─────────────┐

□

□

□

□

└─────────────┘
```

---

# Containers

Existem três tipos.

Container

Largura máxima.

Ideal para formulários.

---

Fluid

Ocupa toda a largura.

Ideal para dashboards.

---

Compact

Centralizado.

Ideal para login.

---

# Espaçamento

Todo espaçamento utiliza Tokens.

Nunca:

margin:17px

Sempre:

Spacing MD

Spacing LG

Spacing XL

---

# Alinhamento

Horizontal

Left

Center

Right

Stretch

---

Vertical

Top

Center

Bottom

Stretch

---

# Ordem

O Grid permite alterar a ordem dos elementos.

Desktop

```text
A B C
```

Mobile

```text
A

C

B
```

Sem alterar o HTML.

---

# Áreas

O Grid suporta regiões.

```text
┌──────────────────────────────┐

Header

──────────────

Sidebar | Content

──────────────

Footer

└──────────────────────────────┘
```

---

# Workspace

O Workspace também utiliza Grid.

```text
Header

Toolbar

Filters

Content

Status
```

Cada região pode conter um Grid interno.

---

# Dashboard

Exemplo

```text
┌─────────────────────────────────────────┐

KPI KPI KPI KPI

───────────────

Chart

───────────────

Tabela

└─────────────────────────────────────────┘
```

---

# Formulários

Exemplo

```text
Nome

────────────────────

CNPJ

────────────────────

Cidade

UF
```

Desktop

2 colunas.

Tablet

2 colunas.

Mobile

1 coluna.

---

# Tabelas

As tabelas ocupam sempre 12 colunas.

Nunca ficam "flutuando".

---

# Cards

Os Cards ocupam regiões do Grid.

Exemplo

```text
Dashboard

3

3

3

3
```

ou

```text
8

4
```

ou

```text
9

3
```

---

# Princípios

O Grid controla a posição.

Os componentes controlam a aparência.

Essa separação elimina milhares de linhas de CSS específico.

---

# Benefícios

• Layout consistente

• Fácil manutenção

• Totalmente responsivo

• Escalável

• Independente dos componentes

• Compatível com qualquer módulo

---

# Conclusão

Todo elemento visual do FiscalUI deve existir dentro do Sistema de Grid.

O Grid é responsável pela estrutura espacial da aplicação.

Os componentes apenas ocupam os espaços definidos por ele.
