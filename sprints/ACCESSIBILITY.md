# Capítulo 13 — Accessibility Framework (Framework de Acessibilidade)

## Visão Geral

A acessibilidade é um dos pilares fundamentais do FiscalUI Framework.

Ela não deve ser tratada como um recurso opcional ou implementada posteriormente. Todos os componentes, layouts e interações devem nascer acessíveis desde sua concepção.

O objetivo é garantir que qualquer usuário, independentemente de limitações físicas, sensoriais ou cognitivas, consiga utilizar o sistema com segurança, eficiência e autonomia.

---

# Objetivos

O Accessibility Framework tem como objetivos:

- Garantir conformidade com padrões internacionais.
- Permitir navegação completa utilizando apenas o teclado.
- Compatibilidade com leitores de tela.
- Melhorar a experiência para todos os usuários.
- Reduzir barreiras de acesso.
- Facilitar auditorias de acessibilidade.

---

# Princípios

O FiscalUI adota quatro princípios fundamentais inspirados na WCAG.

## 1. Perceptível

Toda informação deve poder ser percebida.

Exemplos:

- Texto alternativo em imagens.
- Contraste adequado.
- Legendas.
- Ícones acompanhados de texto quando necessário.

---

## 2. Operável

Toda funcionalidade deve ser acessível.

Exemplos:

- Navegação por teclado.
- Atalhos.
- Ordem lógica de foco.
- Tempo suficiente para interação.

---

## 3. Compreensível

A interface deve ser previsível.

Exemplos:

- Botões com nomes claros.
- Mensagens objetivas.
- Erros explicativos.
- Fluxos consistentes.

---

## 4. Robusto

O sistema deve funcionar em diferentes tecnologias assistivas.

Exemplos:

- Screen Readers.
- Navegadores.
- Sistemas Operacionais.
- Dispositivos móveis.

---

# Arquitetura

```text
Application

↓

Accessibility Engine

↓

Componentes

↓

Usuário
```

O Accessibility Engine atua transversalmente em todos os componentes.

---

# HTML Semântico

O Framework utiliza HTML semântico sempre que possível.

Exemplos:

```html
<header>

<nav>

<main>

<section>

<article>

<aside>

<footer>
```

Evitar:

```html
<div class="header">

<div class="menu">

<div class="content">
```

Sempre que existir uma tag semântica equivalente, ela deve ser utilizada.

---

# Atributos ARIA

Quando o HTML semântico não for suficiente, utilizar atributos ARIA.

Exemplos:

```html
aria-label

aria-labelledby

aria-describedby

aria-expanded

aria-controls

aria-current

aria-hidden

role
```

Todos os componentes interativos devem possuir atributos ARIA adequados.

---

# Navegação por Teclado

Todo o sistema deve ser completamente utilizável sem mouse.

Teclas obrigatórias:

```text
TAB

SHIFT + TAB

ENTER

ESPAÇO

ESC

SETAS

HOME

END

PAGE UP

PAGE DOWN
```

---

# Ordem de Foco

A navegação por TAB deve seguir a ordem visual da interface.

Nunca permitir que o foco "salte" entre áreas sem lógica.

Exemplo:

```text
Logo

↓

Pesquisa

↓

Menu

↓

Workspace

↓

Toolbar

↓

Tabela

↓

Rodapé
```

---

# Indicador de Foco

Todo elemento focável deve apresentar um indicador visual claro.

Exemplo:

- Contorno destacado.
- Mudança de cor.
- Sombra.
- Realce compatível com o tema.

Nunca remover o foco padrão sem substituí-lo por outro equivalente.

---

# Contraste

O contraste entre texto e fundo deve atender aos requisitos mínimos da WCAG.

Aplicações:

- Texto principal.
- Texto secundário.
- Botões.
- Links.
- Campos de formulário.
- Mensagens de erro.

O Theme Engine deverá garantir esses níveis de contraste em todos os temas oficiais.

---

# Formulários

Todos os campos devem possuir:

- Label visível.
- Identificador único.
- Mensagem de ajuda (quando necessário).
- Mensagem de erro associada.
- Indicação de obrigatoriedade.

Exemplo:

```html
<label for="cnpj">
    CNPJ
</label>

<input id="cnpj" required>

<span id="erro-cnpj">
    CNPJ inválido.
</span>
```

---

# Mensagens

Mensagens devem ser claras.

Evitar:

"Erro."

Preferir:

"Não foi possível salvar o cadastro. Verifique os campos obrigatórios."

---

# Ícones

Ícones nunca devem ser o único meio de comunicação.

Exemplo correto:

```text
🗑 Excluir
```

Evitar:

```text
🗑
```

Quando o texto não for exibido, utilizar `aria-label`.

---

# Tabelas

Toda tabela deve informar:

- Cabeçalhos.
- Escopo das colunas.
- Descrição quando necessário.
- Estado vazio.
- Estado de carregamento.

---

# Modais

Ao abrir um modal:

- O foco deve ser movido para o modal.
- O foco não pode escapar do modal.
- ESC fecha o modal.
- Ao fechar, o foco retorna ao elemento anterior.

---

# Notificações

Toasts e alertas devem ser anunciados para leitores de tela sem interromper a navegação do usuário.

---

# Cores

A cor nunca deve ser o único indicador de informação.

Exemplo incorreto:

Campo vermelho.

Exemplo correto:

Campo vermelho + ícone + mensagem de erro.

---

# Animações

Usuários com preferência por redução de movimento devem receber animações simplificadas ou desativadas.

O Motion Engine deverá respeitar essa configuração automaticamente.

---

# Internacionalização

Todos os textos devem permitir tradução.

Evitar textos fixos no HTML ou JavaScript.

Utilizar recursos de internacionalização para facilitar localização.

---

# Testes de Acessibilidade

Antes da publicação, cada componente deve ser validado quanto a:

- Navegação por teclado.
- Compatibilidade com leitores de tela.
- Contraste.
- HTML semântico.
- Atributos ARIA.
- Ordem de foco.
- Mensagens.
- Responsividade.

---

# Checklist de Componentes

Cada componente deverá responder positivamente às seguintes perguntas:

- Pode ser utilizado apenas com teclado?
- Possui foco visível?
- É compreensível sem depender de cores?
- Utiliza HTML semântico?
- Possui atributos ARIA quando necessário?
- Funciona com leitores de tela?
- Mantém contraste adequado em todos os temas?
- É responsivo?
- Possui documentação de acessibilidade?

---

# Integração com outros módulos

O Accessibility Framework atua em conjunto com:

- Theme Engine
- Responsive Engine
- Motion Design
- Component Library
- JavaScript Core

---

# Benefícios

- Inclusão digital.
- Conformidade com padrões internacionais.
- Melhor experiência de uso.
- Redução de erros.
- Facilidade de manutenção.
- Maior qualidade do produto.

---

# Conclusão

A acessibilidade não é um complemento do FiscalUI.

Ela faz parte da arquitetura do Framework.

Todo componente desenvolvido deverá nascer acessível, garantindo uma experiência consistente, inclusiva e preparada para diferentes usuários, dispositivos e tecnologias assistivas.

O compromisso com a acessibilidade reforça a qualidade técnica do FiscalUI e assegura sua utilização em ambientes corporativos, governamentais e de missão crítica.
