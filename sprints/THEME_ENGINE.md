# Capítulo 10 — Theme Engine (Sistema de Temas)

## Conceito

O Theme Engine é responsável por controlar toda a aparência visual do FiscalUI.

Os componentes não conhecem cores, sombras ou fontes.

Eles conhecem apenas Design Tokens.

O Theme Engine fornece os valores desses Tokens.

```text
Componentes

↓

Design Tokens

↓

Theme Engine

↓

Tema Ativo
```

---

# Objetivos

O Theme Engine possui cinco objetivos.

• Permitir múltiplos temas

• Personalização por empresa

• Mudança instantânea

• Centralizar aparência

• Eliminar CSS duplicado

---

# Filosofia

O componente nunca muda.

Quem muda é o tema.

Exemplo

```text
Button

↓

Mesmo HTML

↓

Mesmo CSS

↓

Tema Dark

↓

Tema Light

↓

Tema Glass

↓

Tema Corporate
```

---

# Arquitetura

```text
Theme Engine

│

├── Light

├── Dark

├── Liquid Glass

├── Corporate

├── High Contrast

└── Custom
```

Todos compartilham exatamente os mesmos Tokens.

---

# Estrutura

```text
themes/

│

├── light/

│      colors.css

│      typography.css

│      shadows.css

│

├── dark/

│      colors.css

│      typography.css

│      shadows.css

│

├── glass/

│      colors.css

│      blur.css

│      opacity.css

│

├── corporate/

│

└── custom/
```

---

# Temas Oficiais

## Light

Características

• Fundo claro

• Alto contraste

• Ideal para ambientes corporativos

---

## Dark

Características

• Fundo escuro

• Menor fadiga visual

• Ideal para uso contínuo

---

## Liquid Glass

Características

• Transparência

• Blur

• Reflexos suaves

• Cartões flutuantes

• Sombras leves

• Visual premium

---

## Corporate

Tema institucional.

Cada empresa poderá utilizar:

• Cor primária

• Cor secundária

• Logo

• Tipografia

Sem alterar os componentes.

---

## High Contrast

Voltado para acessibilidade.

Características

• Alto contraste

• Bordas evidentes

• Fontes maiores

• Sem transparências

---

# Estrutura de um Tema

Cada tema fornece apenas valores.

```text
Color

↓

Background

↓

Surface

↓

Border

↓

Shadow

↓

Typography

↓

Motion
```

---

# Tokens

Exemplo

Tema Dark

```text
Primary

↓

#16B3AC
```

Tema Light

```text
Primary

↓

#0F8C82
```

O componente continua exatamente igual.

---

# Glass Theme

O tema Glass possui Tokens exclusivos.

```text
Glass Blur

Glass Border

Glass Shadow

Glass Reflection

Glass Transparency
```

Todos os Cards utilizam esses Tokens.

---

# Troca de Tema

O usuário pode alterar o tema sem reiniciar o sistema.

Fluxo

```text
Configuração

↓

Selecionar Tema

↓

Atualizar Tokens

↓

Repaint

↓

Interface Atualizada
```

Sem recarregar a página.

---

# Personalização

Cada empresa pode definir.

```text
Logo

Primary Color

Secondary Color

Fonte

Ícones

Wallpaper

Modo Escuro

Tema Preferido
```

Essas configurações não alteram o Framework.

---

# Persistência

O tema selecionado é armazenado.

```text
Usuário

↓

Preferência

↓

Banco

↓

Login

↓

Tema Restaurado
```

---

# Responsabilidades

O Theme Engine controla.

• Cores

• Fontes

• Bordas

• Sombras

• Transparências

• Motion

• Glass

• Espaçamento especial

---

Não controla.

• Layout

• Grid

• Componentes

• Navegação

---

# Compatibilidade

Todos os componentes devem funcionar em todos os temas.

Nenhum componente poderá depender de um tema específico.

---

# Benefícios

• Personalização

• Consistência

• Fácil manutenção

• Multiempresa

• White Label

• Baixo acoplamento

---

# Conclusão

O Theme Engine separa completamente aparência e comportamento.

Os componentes permanecem imutáveis.

A identidade visual é definida exclusivamente pelos temas, tornando o FiscalUI preparado para diferentes clientes, empresas e necessidades futuras.
