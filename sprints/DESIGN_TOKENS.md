# Design Tokens

## Conceito

Design Tokens são a menor unidade de configuração visual do FiscalUI.

Eles representam valores reutilizáveis que definem a identidade do sistema.

Nenhum componente deve utilizar valores fixos.

Ao invés de escrever:

```css
color:#16B3AC;
```

Utiliza-se:

```css
color:var(--color-primary);
```

Dessa forma toda a identidade visual pode ser alterada sem modificar os componentes.

---

# Objetivos

Os Design Tokens foram criados para:

- Padronizar a interface.
- Facilitar manutenção.
- Permitir múltiplos temas.
- Garantir consistência.
- Evitar duplicação de estilos.

---

# Estrutura

```text
Design Tokens

│

├── Colors

├── Typography

├── Spacing

├── Radius

├── Borders

├── Shadows

├── Elevation

├── Motion

├── Opacity

└── Z-Index
```

---

# Cores

As cores representam a identidade visual do FiscalUI.

Não possuem significado funcional.

Os componentes interpretam os tokens.

## Primárias

```text
Primary

Primary Hover

Primary Active
```

---

## Secundárias

```text
Secondary

Secondary Hover

Secondary Active
```

---

## Superfícies

```text
Background

Surface

Glass Surface

Overlay

Container

Panel
```

---

## Texto

```text
Primary Text

Secondary Text

Muted Text

Disabled Text

Inverse Text
```

---

## Bordas

```text
Border

Border Hover

Border Focus

Border Active
```

---

## Estados

```text
Success

Warning

Danger

Info
```

Essas cores não pertencem aos botões.

São cores semânticas.

---

# Tipografia

Toda tipografia do sistema utiliza tokens.

Nunca se define tamanho diretamente.

## Família

```text
Primary Font

Monospace Font
```

---

## Escala

```text
Display

H1

H2

H3

H4

Body

Small

Caption
```

---

## Peso

```text
Light

Regular

Medium

SemiBold

Bold
```

---

# Espaçamento

Todo espaçamento utiliza escala.

Nunca valores aleatórios.

```text
0

2

4

8

12

16

24

32

40

48

64

80

96
```

Todos os componentes compartilham essa escala.

---

# Bordas

```text
None

Small

Medium

Large

Extra Large

Rounded

Pill
```

---

# Sombras

A profundidade da interface é controlada pelos tokens.

```text
Shadow XS

Shadow SM

Shadow MD

Shadow LG

Shadow XL

Glass Shadow
```

---

# Glass

Como o tema principal é Liquid Glass, existem tokens específicos.

```text
Glass Blur

Glass Opacity

Glass Border

Glass Shadow

Glass Highlight
```

Todos os cartões utilizam exatamente os mesmos parâmetros.

---

# Motion

As animações também são padronizadas.

```text
Fast

Normal

Slow
```

Curvas

```text
Ease

Ease In

Ease Out

Ease In Out
```

Nenhuma animação utiliza tempos diferentes.

---

# Opacidade

```text
100%

90%

80%

60%

40%

20%

10%
```

---

# Camadas

```text
Base

Dropdown

Modal

Dialog

Notification

Tooltip

Fullscreen
```

Define qual elemento fica acima de outro.

---

# Exemplo Conceitual

```text
Botão

↓

Primary Color

↓

Primary Text

↓

Medium Radius

↓

Shadow SM

↓

Motion Fast
```

Todo componente é apenas uma composição de tokens.

---

# Sistema de Temas

Os tokens tornam possível a troca completa da aparência.

```text
Light Theme

↓

Mesmo componente

↓

Dark Theme

↓

Mesmo componente

↓

Liquid Glass

↓

Mesmo componente
```

Os componentes não mudam.

Apenas os tokens.

---

# Benefícios

- Consistência visual.
- Facilidade de manutenção.
- Temas instantâneos.
- Redução de CSS.
- Escalabilidade.
- Reutilização máxima.

---

# Princípio

Os componentes não possuem identidade visual própria.

Toda identidade do FiscalUI nasce dos Design Tokens.

Os componentes apenas consomem esses valores.

Essa separação torna possível evoluir completamente o visual do sistema sem alterar uma única linha da estrutura dos componentes.
