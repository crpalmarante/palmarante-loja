# Capítulo 14 — Motion Design (Sistema de Movimento)

## Visão Geral

O Motion Design é responsável por definir o comportamento visual das transições, animações e microinterações do FiscalUI Framework.

Seu objetivo não é tornar a interface chamativa, mas comunicar estados, orientar o usuário e transmitir fluidez durante a utilização do sistema.

No FiscalUI, movimento é informação.

Toda animação deve possuir um propósito claro.

---

# Objetivos

O Motion Design possui os seguintes objetivos:

- Melhorar a percepção da interface.
- Guiar a atenção do usuário.
- Comunicar mudanças de estado.
- Reduzir sensação de espera.
- Tornar a navegação mais natural.
- Reforçar a identidade visual do Framework.

---

# Filosofia

As animações devem ser:

• Discretas

• Elegantes

• Funcionais

• Consistentes

• Performáticas

Nunca devem distrair o usuário.

---

# Princípios

O Motion Design do FiscalUI segue cinco princípios.

## Clareza

Toda animação deve explicar uma ação.

Exemplo

Clique em um botão

↓

Botão responde imediatamente

↓

Usuário entende que a ação foi registrada.

---

## Continuidade

Mudanças de tela devem parecer naturais.

Nunca ocorrer mudanças bruscas.

---

## Hierarquia

Elementos mais importantes recebem maior destaque visual.

Exemplo

Modal

↓

Fade + Scale

Enquanto o fundo apenas perde opacidade.

---

## Feedback

Toda ação importante deve produzir uma resposta visual.

Exemplo

Salvar

↓

Loading

↓

Sucesso

↓

Toast

---

## Performance

Animações nunca podem comprometer a velocidade da aplicação.

---

# Arquitetura

```text
Motion Engine

│

├── Transitions

├── Microinteractions

├── Feedback

├── Navigation

├── Loading

├── Glass Effects

└── Accessibility
```

---

# Tipos de Movimento

O Framework utiliza seis categorias.

## Entrada

Quando um componente aparece.

Exemplos

- Fade In
- Slide In
- Scale In

---

## Saída

Quando um componente desaparece.

Exemplos

- Fade Out
- Slide Out
- Scale Out

---

## Ênfase

Destaca um elemento.

Exemplos

- Pulso suave
- Brilho discreto
- Pequena expansão

---

## Navegação

Mudança entre páginas.

Exemplos

Workspace

↓

Fade

↓

Novo Workspace

---

## Feedback

Resposta imediata às ações.

Exemplos

Hover

Clique

Erro

Sucesso

---

## Estado

Mudança de informações.

Exemplo

Loading

↓

Dados carregados

↓

Tabela

---

# Duração

As animações utilizam tempos padronizados.

```text
Instantânea

100 ms
```

---

```text
Rápida

150 ms
```

---

```text
Normal

250 ms
```

---

```text
Suave

350 ms
```

---

```text
Longa

500 ms
```

Nenhum componente define tempos próprios.

Todos utilizam Motion Tokens.

---

# Curvas de Animação

Utilizar apenas curvas oficiais.

```text
Ease

Ease In

Ease Out

Ease In Out

Linear
```

---

# Hover

Todo componente interativo responde ao ponteiro.

Exemplos

Botão

↓

Leve aumento de brilho.

Card

↓

Elevação discreta.

Menu

↓

Mudança de fundo.

---

# Focus

Ao receber foco.

O componente deve:

- destacar borda
- aumentar contraste
- manter consistência com o tema

Nunca utilizar animações exageradas.

---

# Clique

Ao clicar.

Exemplo

```text
Botão

↓

Leve compressão

↓

Retorno

↓

Loading (quando necessário)
```

---

# Loading

O Motion Design reduz a sensação de espera.

Exemplos

Skeleton

Spinner

Barra de progresso

Shimmer

---

# Skeleton

Sempre preferido ao Spinner.

Fluxo

```text
Tela

↓

Skeleton

↓

Conteúdo
```

Evita mudanças bruscas.

---

# Sidebar

Ao expandir.

```text
Ícones

↓

Texto aparece

↓

Largura aumenta
```

Tudo ocorre suavemente.

---

# Drawer

No Mobile.

```text
Desliza da esquerda

↓

Overlay

↓

Workspace permanece abaixo
```

---

# Modal

Sequência

```text
Fundo

↓

Overlay

↓

Scale

↓

Fade

↓

Modal
```

Ao fechar.

A sequência é invertida.

---

# Toast

Surge discretamente.

```text
Fade

↓

Slide

↓

Permanece

↓

Fade Out
```

Nunca bloqueia a interface.

---

# Dropdown

Fluxo

```text
Clique

↓

Fade

↓

Slide Vertical

↓

Itens
```

---

# Tooltip

Nunca aparece instantaneamente.

Possui pequeno atraso.

Desaparece imediatamente ao perder foco.

---

# Accordion

A altura deve ser animada.

Nunca abrir ou fechar abruptamente.

---

# Tabs

A troca entre abas deve preservar contexto.

Indicador desliza suavemente.

Conteúdo realiza Fade.

---

# Dashboard

KPIs

Animação apenas na primeira renderização.

Nunca repetir constantemente.

---

# Gráficos

Os gráficos podem animar.

Somente no carregamento inicial.

---

# Liquid Glass

O tema Liquid Glass utiliza animações específicas.

Exemplos

Blur

Reflexos

Mudança de opacidade

Elevação

Refração simulada

Esses efeitos devem ser sutis.

---

# Motion Tokens

Todo movimento utiliza tokens.

```text
Motion Fast

Motion Normal

Motion Slow

Motion Bounce

Motion Fade

Motion Scale

Motion Slide
```

---

# Performance

Utilizar apenas propriedades aceleradas por GPU.

Permitidas

```text
transform

opacity
```

Evitar

```text
top

left

width

height
```

Sempre que possível.

---

# Redução de Movimento

Usuários que preferem menos animações devem ser respeitados.

Quando a preferência do sistema indicar redução de movimento:

- remover animações decorativas
- manter apenas feedback essencial
- reduzir duração

---

# Estados

Todos os componentes devem possuir estados definidos.

```text
Idle

Hover

Focus

Pressed

Loading

Success

Warning

Error

Disabled
```

Cada mudança entre estados deve utilizar transições suaves.

---

# Consistência

Todos os componentes utilizam exatamente o mesmo sistema de movimento.

Nunca criar animações específicas para uma tela.

---

# Integração

O Motion Design trabalha em conjunto com:

- Theme Engine
- Responsive Engine
- Accessibility Framework
- JavaScript Core
- Component Library

---

# Benefícios

- Interface mais fluida.
- Melhor experiência do usuário.
- Redução da carga cognitiva.
- Feedback imediato.
- Identidade visual consistente.
- Sensação de qualidade e refinamento.

---

# Boas Práticas

✔ Animar apenas quando houver ganho de usabilidade.

✔ Priorizar simplicidade.

✔ Manter consistência entre componentes.

✔ Respeitar preferências de acessibilidade.

✔ Utilizar Motion Tokens.

✔ Evitar animações repetitivas.

---

# O que evitar

✖ Animações longas.

✖ Efeitos excessivos.

✖ Movimentos sem propósito.

✖ Mudanças bruscas de layout.

✖ Animações que prejudiquem a leitura.

✖ Componentes com tempos diferentes.

---

# Conclusão

O Motion Design do FiscalUI não existe para decorar a interface.

Ele existe para comunicar, orientar e reforçar a experiência do usuário.

Toda animação deve transmitir informação, mantendo a interface elegante, consistente e alinhada com a identidade visual do tema **Liquid Glass**.

Ao centralizar as regras de movimento em um único sistema, o FiscalUI garante que todos os módulos do ERP apresentem um comportamento uniforme, previsível e de alto nível profissional.
