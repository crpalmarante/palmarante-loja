# Capítulo 12 — Responsive Engine

## Conceito

O Responsive Engine é responsável por adaptar automaticamente toda a interface do FiscalUI aos diferentes dispositivos e resoluções de tela.

A responsividade não pertence aos componentes.

Ela pertence ao Framework.

Cada componente apenas informa como deve se comportar.

O Responsive Engine toma as decisões.

---

# Objetivos

O Responsive Engine foi criado para:

• Utilizar um único código-fonte

• Eliminar versões Desktop e Mobile

• Garantir consistência

• Facilitar manutenção

• Melhorar a experiência do usuário

---

# Filosofia

Não existem duas interfaces.

Existe apenas uma interface.

Ela se reorganiza conforme o espaço disponível.

```text
Mesmo HTML

↓

Mesmo CSS

↓

Mesmo JavaScript

↓

Layouts diferentes
```

---

# Breakpoints Oficiais

```text
XS

0 — 575px

Telefone
```

---

```text
SM

576 — 767px

Telefone Grande
```

---

```text
MD

768 — 1023px

Tablet
```

---

```text
LG

1024 — 1439px

Notebook
```

---

```text
XL

1440 — 1919px

Desktop
```

---

```text
XXL

1920+

UltraWide
```

---

# Estratégia

O FiscalUI utiliza

**Mobile First**

ou seja

```text
Mobile

↓

Tablet

↓

Desktop
```

A interface cresce.

Nunca diminui.

---

# Estrutura

```text
Application

↓

Responsive Engine

↓

Layout

↓

Componentes
```

---

# Sidebar

Desktop

```text
██████████

Menu Aberto
```

Tablet

```text
██

Somente Ícones
```

Mobile

```text
☰

Drawer
```

---

# TopBar

Desktop

```text
Logo

Pesquisa

Empresa

Usuário

Notificações
```

Tablet

```text
Logo

Pesquisa

Usuário
```

Mobile

```text
☰

Logo

Usuário
```

---

# Workspace

Desktop

```text
Sidebar

Workspace
```

Tablet

```text
Sidebar Compacta

Workspace
```

Mobile

```text
Workspace

Drawer
```

---

# Dashboard

Desktop

```text
□ □ □ □
```

Tablet

```text
□ □

□ □
```

Mobile

```text
□

□

□

□
```

---

# Cards

Desktop

4 por linha

Tablet

2 por linha

Mobile

1 por linha

---

# Formulários

Desktop

```text
Nome        CPF

Cidade      UF
```

Tablet

```text
Nome

CPF

Cidade

UF
```

Mobile

```text
Nome

CPF

Cidade

UF
```

---

# Tabelas

Desktop

Tabela completa.

Tablet

Colunas secundárias ocultas.

Mobile

Visualização em Cards.

Exemplo

```text
Cliente

Empresa ABC

Valor

R$ 10.000

Status

Autorizada
```

---

# Toolbar

Desktop

Todos os botões.

Tablet

Ícones.

Mobile

Menu Overflow.

---

# Modais

Desktop

Centralizado.

Tablet

Maior.

Mobile

Tela cheia.

---

# Tipografia

Desktop

Escala completa.

Mobile

Redução automática dos títulos.

---

# Espaçamento

Desktop

Espaçamento XL.

Tablet

Espaçamento LG.

Mobile

Espaçamento MD.

---

# Imagens

Nunca possuem largura fixa.

Sempre ocupam

100%

do container.

---

# Performance

O Responsive Engine evita:

• JavaScript desnecessário

• Redesenhos excessivos

• Layout Shift

• Reflows constantes

---

# Princípios

Nunca:

Criar páginas Mobile.

Sempre:

Criar componentes responsivos.

---

# Benefícios

• Um único código

• Melhor manutenção

• Interface consistente

• Melhor UX

• Maior produtividade

---

# Conclusão

O Responsive Engine garante que todos os componentes do FiscalUI funcionem corretamente em qualquer dispositivo.

A adaptação da interface é responsabilidade do Framework, permitindo que os módulos do ERP permaneçam simples, consistentes e independentes da plataforma utilizada.
