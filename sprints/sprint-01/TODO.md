# TODO — Sprint 02 (Navegação)

## Design System — Dark Glassmorphism

```
Fundo:       gradiente escuro geométrico
Superfície:  vidro translúcido com blur
Topbar:      flutuante (não colada no topo)
Painéis:     grandes, cantos 20~24px, bordas suaves iluminadas
Layout:      duas colunas principais
Botões:      pill shape
Cards:       internos com camadas (profundidade ERP)
Sensação:    densa, profissional, escura
```

## Sidebar (retrátil)
- [ ] Sidebar colapsável: só ícone quando fechada, ícone + texto quando aberta
- [ ] Salvar estado (colapsado/aberto) no localStorage
- [ ] Tooltip nos itens quando colapsado
- [ ] Animação suave na transição

## Header
- [ ] `Logo · NomeDoModulo` à esquerda
- [ ] Aplicativos do módulo atual no centro
- [ ] Informações do usuário + sair à direita
- [ ] Ao clicar em um módulo da sidebar, header atualiza os aplicativos

## Toolbar
- [ ] Botão "Novo" (pill)
- [ ] Campo de pesquisa
- [ ] Alternador de visualização (Lista / Grid / Kanban)

## Workspace
- [ ] Área principal com painéis glassmorphism
- [ ] Cantos arredondados grandes (20~24px)
- [ ] Bordas suaves iluminadas
- [ ] backdrop-filter blur

## Status Bar
- [ ] Rodapé com informações do sistema

## Menu / JSON
- [ ] Reestruturar `menu.json` para separar módulos de aplicativos
- [ ] Cada módulo: `{ id, label, icon, apps: [...] }`
- [ ] Cada aplicativo: `{ id, label, icon, href }`

## Geral
- [ ] Refatorar `app.js` em módulos (Sidebar.js, Header.js, Toolbar.js, Router.js)
- [ ] Aplicar dark glassmorphism no sistema todo
