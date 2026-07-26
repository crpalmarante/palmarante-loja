/*=========================================================
    FiscalBrasil ERP
    File    : app.js
=========================================================*/

/*=========================================================
  SVG SPRITE (delegado ao IconManager via FiscalUI)
=========================================================*/

/*=========================================================
  AUTH
=========================================================*/

const token=localStorage.getItem("auth_token");

if(!token){

    window.location.href="login.html";

}

/*=========================================================
  STATE
=========================================================*/

let userData=null;

let menuData=[];

let currentMod=null;

/*=========================================================
  API
=========================================================*/

async function apiFetch(path,options={}){

    const headers={

        "X-Auth-Token":token,

        ...options.headers

    };

    try{

        const res=await fetch(path,{...options,headers});

        if(!res.ok){

            const text=await res.text().catch(()=>"");

            throw new Error("HTTP "+res.status+": "+(text||res.statusText));

        }

        return res.json();

    }catch(e){

        if(window.FiscalUI&&FiscalUI.errors){

            FiscalUI.errors.capture(e,{level:"error",api:path});

        }

        return{status:"error",message:e.message};

    }

}

/*=========================================================
  VALIDAR TOKEN
=========================================================*/

const authData=await apiFetch("/api/auth/me");

if(authData.status!=="ok"){

    localStorage.removeItem("auth_token");

    localStorage.removeItem("pos_usuario");

    window.location.href="login.html";

}

userData=authData.conta;

localStorage.setItem("pos_usuario",JSON.stringify(userData));

/*=========================================================
  MENU
=========================================================*/

try{

    const res=await fetch("assets/data/menu.json");

    menuData=await res.json();

}catch(e){

    if(window.FiscalUI&&FiscalUI.errors){

        FiscalUI.errors.warn("menu.json not loaded");

    }else{

        console.error("menu.json not loaded",e);

    }

}

/*=========================================================
  FILTER MENU BY PERMISSIONS
=========================================================*/

function hasPermission(id){

    if(userData.tipo==="usuario")return true;

    const perms=(userData.permissoes||"").split(",").map(s=>s.trim()).filter(Boolean);

    return perms.includes(id);

}

function filterMenu(items){

    const result=[];

    for(const item of items){

        if(item.section){

            result.push(item);

            continue;

        }

        if(item.children){

            const filtered=filterMenu(item.children);

            const hasVisible=filtered.some(c=>!c.section);

            if(hasPermission(item.id)||hasVisible){

                result.push({...item,children:filtered});

            }

        }else{

            if(hasPermission(item.id)){

                result.push(item);

            }

        }

    }

    return result;

}

const filteredMenu=filterMenu(menuData);

/*=========================================================
  MODULE MAPPING
=========================================================*/

const moduleMap={

    nfe:"faturamento",

    nfce:"faturamento",

    produtos:"faturamento",

    clientes:"faturamento",

    relatorios:"faturamento",

    empresas:"faturamento",

    config:"configuracoes",

    dashboard:"dashboard"

};

const moduleTitles={

    nfe:"NF-e",

    nfce:"NFC-e",

    produtos:"Produtos",

    clientes:"Clientes",

    relatorios:"Relatórios",

    empresas:"Empresas",

    config:"Configuração",

    dashboard:"Dashboard"

};

const moduleToolbar={

    nfe:["+ Novo","Importar","Exportar","Pesquisar"],

    nfce:["+ Novo","Importar","Exportar","Pesquisar"],

    produtos:["+ Novo","Importar","Exportar","Pesquisar"],

    clientes:["+ Novo","Importar","Exportar","Pesquisar"],

    relatorios:["Gerar","Exportar","Imprimir","Pesquisar"],

    empresas:["+ Nova","Editar","Pesquisar"],

    config:["Salvar","Carregar","Pesquisar"],

    dashboard:["Atualizar","Exportar","Configurar"]

};

/*=========================================================
  ICON HELPER
=========================================================*/

function icon(name){

    return `<svg class="icon"><use href="#${name}"/></svg>`;

}

/*=========================================================
  RENDER MENU
=========================================================*/

function renderMenu(items,level=0){

    let html="";

    for(const item of items){

        if(item.section){

            html+=`<div class="menu-section">${item.section}</div>`;

            continue;

        }

        const id=item.id;

        const hasChildren=item.children&&item.children.length>0;

        if(hasChildren){

            html+=`<div class="menu-item has-children" data-id="${id}" onclick="toggleSubmenu('${id}')">

                ${icon(item.icon)}

                <span class="menu-label">${item.label}</span>

                <svg class="icon icon-16 menu-arrow"><use href="#icon-chevron-down"/></svg>

            </div>`;

            html+=`<div class="menu-submenu" id="sub-${id}">`;

            html+=renderMenu(item.children,level+1);

            html+=`</div>`;

        }else{

            const href=item.href||"#";

            html+=`<a class="menu-item" href="${href}" data-id="${id}">

                ${icon(item.icon)}

                <span class="menu-label">${item.label}</span>

            </a>`;

        }

    }

    return html;

}

/*=========================================================
  TOGGLE SUBMENU
=========================================================*/

window.toggleSubmenu=function(id){

    const el=document.getElementById("sub-"+id);

    if(!el)return;

    el.classList.toggle("open");

    const arrow=el.previousElementSibling?.querySelector(".menu-arrow");

    if(arrow)arrow.classList.toggle("rotated");

};

/*=========================================================
  HIGHLIGHT ACTIVE
=========================================================*/

function highlightActive(){

    const current=window.location.pathname.split("/").pop()||"index.html";

    document.querySelectorAll(".menu-item").forEach(el=>{

        const href=el.getAttribute("href");

        if(href===current){

            el.classList.add("active");

            let parent=el.closest(".menu-submenu");

            while(parent){

                parent.classList.add("open");

                const prev=parent.previousElementSibling;

                if(prev&&prev.classList.contains("has-children")){

                    const arrow=prev.querySelector(".menu-arrow");

                    if(arrow)arrow.classList.add("rotated");

                }

                parent=parent.parentElement?.closest(".menu-submenu");

            }

        }

    });

}

/*=========================================================
  USER SECTION
=========================================================*/

function userSection(){

    const nome=userData.nome||userData.usuario;

    const tipo=userData.tipo==="usuario"?"Administrador":"Funcionário";

    return `

        <div class="sidebar-user">

            <div class="user-avatar">${nome.charAt(0).toUpperCase()}</div>

            <div class="user-info">

                <div class="user-name">${nome}</div>

                <div class="user-role">${tipo}</div>

            </div>

            <button class="user-logout" onclick="logout()" title="Sair">

                <svg class="icon"><use href="#icon-logout"/></svg>

            </button>

        </div>

    `;

}

/*=========================================================
  LOGOUT
=========================================================*/

window.logout=function(){

    apiFetch("/api/auth/logout",{method:"POST"}).catch(()=>{});

    localStorage.removeItem("auth_token");

    localStorage.removeItem("pos_usuario");

    window.location.href="login.html";

};

/*=========================================================
  GET MODULE FROM URL
=========================================================*/

function getModFromUrl(){

    const params=new URLSearchParams(window.location.search);

    return params.get("mod");

}

/*=========================================================
  FIND MODULE IN MENU
=========================================================*/

function findModule(modId){

    const menuId=moduleMap[modId];

    if(!menuId)return null;

    return filteredMenu.find(m=>m.id===menuId)||null;

}

/*=========================================================
  RENDER LAUNCHPAD
=========================================================*/

function renderLaunchpad(){

    document.getElementById("launchpad").style.display="";

    document.getElementById("workspace-view").style.display="none";

    const sidebar=document.getElementById("sidebar");

    if(!sidebar)return;

    sidebar.innerHTML=`

        <div class="sidebar-brand">

            ${icon("icon-building")}

            <span class="brand-text">FiscalBrasil</span>

        </div>

        <div class="sidebar-collapse" onclick="toggleSidebar()">

            <svg class="icon"><use href="#icon-chevron-left"/></svg>

        </div>

        <nav class="sidebar-nav">

            ${renderMenu(filteredMenu)}

        </nav>

        ${userSection()}

    `;

    highlightActive();

    setGreeting();

}

/*=========================================================
  MODULE CONTENT
=========================================================*/

function moduleContent(modId){

    var tables={

        nfe:{title:"Lista de NF-e",cols:["Número","Cliente","Valor","Status","Data"]},

        nfce:{title:"Lista de NFC-e",cols:["Número","Cliente","Valor","Status","Data"]},

        produtos:{title:"Lista de Produtos",cols:["Código","Produto","NCM","Estoque","Valor"]},

        clientes:{title:"Lista de Clientes",cols:["Código","Nome","CPF/CNPJ","Telefone","E-mail"]},

        relatorios:{title:"Relatórios",cols:["Nome","Tipo","Período","Criado em","Status"]},

        empresas:{title:"Empresas",cols:["CNPJ","Razão Social","Fantasia","Regime","Status"]},

        config:{title:"Configurações",cols:["Parâmetro","Valor","Módulo","Descrição"]},

        dashboard:{title:"Dashboard",cols:["Indicador","Valor","Período","Variação"]}

    };

    var cfg=tables[modId];

    if(!cfg)return `<div class="glass-panel"><p class="workspace-placeholder">Módulo em desenvolvimento.</p></div>`;

    var rows="";

    for(var i=0;i<5;i++){

        rows+=`<tr>${cfg.cols.map(()=>"<td>—</td>").join("")}</tr>`;

    }

    return `

        <div class="glass-panel">

            <h3 style="margin-bottom:var(--space-4);font-size:var(--font-lg);font-weight:var(--font-semibold)">${cfg.title}</h3>

            <table>

                <thead>

                    <tr>${cfg.cols.map(c=>`<th>${c}</th>`).join("")}</tr>

                </thead>

                <tbody>${rows}</tbody>

            </table>

        </div>

    `;

}

/*=========================================================
  RENDER WORKSPACE
=========================================================*/

function renderWorkspace(modId){

    document.getElementById("launchpad").style.display="none";

    document.getElementById("workspace-view").style.display="flex";

    const mod=findModule(modId);

    const title=moduleTitles[modId]||modId.toUpperCase();

    const toolbarActions=moduleToolbar[modId]||["Pesquisar"];

    /* breadcrumb */

    document.getElementById("workspace-breadcrumb").textContent="FiscalBrasil / "+title;

    document.getElementById("workspace-title").textContent=title;

    /* toolbar */

    const toolbarActions2=toolbarActions.slice();

    toolbarActions2.push("Filtros");

    const toolbarEl=document.getElementById("workspace-toolbar");

    toolbarEl.innerHTML=toolbarActions2.map(a=>{

        if(a==="Filtros")return`<button class="toolbar-btn filter-toggle" onclick="toggleFilters()">${a}</button>`;

        return`<button class="toolbar-btn${a.startsWith('+')?' primary':''}">${a}</button>`;

    }).join("");

    /* filters */

    document.getElementById("workspace-filters").style.display="none";

    /* content */

    const contentEl=document.getElementById("workspace-content");

    contentEl.innerHTML=moduleContent(modId);

    /* status bar */

    const statusEl=document.getElementById("status-bar");

    const nome=userData.nome||userData.usuario;

    statusEl.innerHTML=`

        <div class="status-bar-left">

            <span>Usuário: ${nome}</span>

            <span>Empresa: Fiscal Brasil</span>

        </div>

        <div class="status-bar-right">

            <span>Versão 1.0.0</span>

            <span>Ambiente: Produção</span>

            <span id="status-clock"></span>

        </div>

    `;

    function updateClock(){

        const now=new Date();

        document.getElementById("status-clock").textContent=now.toLocaleString("pt-BR");

    }

    updateClock();

    setInterval(updateClock,1000);

    /* sidebar contextual */

    const sidebar=document.getElementById("sidebar");

    if(!sidebar)return;

    let sidebarHtml=`

        <div class="sidebar-brand" onclick="goToLaunchpad()" style="cursor:pointer">

            <svg class="icon"><use href="#icon-chevron-left"/></svg>

            <span class="brand-text">Voltar</span>

        </div>

        <div class="sidebar-collapse" onclick="toggleSidebar()">

            <svg class="icon"><use href="#icon-chevron-left"/></svg>

        </div>

    `;

    if(mod&&mod.children&&mod.children.length>0){

        sidebarHtml+=`<nav class="sidebar-nav">${renderMenu(mod.children)}</nav>`;

    }else{

        sidebarHtml+=`<nav class="sidebar-nav">

            <a class="menu-item active" href="#">

                ${icon("icon-file-text")}

                <span class="menu-label">${title}</span>

            </a>

        </nav>`;

    }

    sidebarHtml+=`<div class="sidebar-recentes">

        <div class="recentes-title">Recentes</div>

        <a class="recente-item" href="#">

            <svg class="icon icon-16"><use href="#icon-clock"/></svg>

            <span class="menu-label">Último acesso</span>

        </a>

    </div>`;

    sidebarHtml+=userSection();

    sidebar.innerHTML=sidebarHtml;

    sidebarOverlay();

}

/*=========================================================
  GO TO LAUNCHPAD (overridden by Router on fiscalui:ready)
=========================================================*/

window.goToLaunchpad=function(){

    history.pushState(null,"","/");

    renderLaunchpad();

};

/*=========================================================
  GREETING
=========================================================*/

function setGreeting(){

    const el=document.getElementById("welcome-greeting");

    if(!el)return;

    var h=new Date().getHours();

    var greeting="Olá";

    if(h<12)greeting="Bom dia";

    else if(h<18)greeting="Boa tarde";

    else greeting="Boa noite";

    el.textContent=greeting+", "+(userData.nome||userData.usuario);

}

/*=========================================================
  SIDEBAR COLLAPSE
=========================================================*/

window.toggleSidebar=function(){

    const sidebar=document.getElementById("sidebar");

    sidebar.classList.toggle("collapsed");

    const collapsed=sidebar.classList.contains("collapsed");

    localStorage.setItem("sidebar_collapsed",collapsed);

    if(window.FiscalUI)FiscalUI.state.set("sidebarCollapsed",collapsed);

};

/*=========================================================
  THEME ENGINE (delegate to FiscalUI core)
=========================================================*/

window.toggleTheme=function(){

    if(window.FiscalUI){

        const cur=document.documentElement.getAttribute("data-theme")||"dark";

        const themes=["dark","light","high-contrast"];

        const next=themes[(themes.indexOf(cur)+1)%themes.length];

        FiscalUI.state.set("theme",next);

    }

};

/*=========================================================
  FILTERS TOGGLE
=========================================================*/

window.toggleFilters=function(){

    const el=document.getElementById("workspace-filters");

    if(el.style.display==="none"){

        el.style.display="";

    }else{

        el.style.display="none";

    }

};

window.clearFilters=function(){

    document.querySelectorAll(".filter-input").forEach(i=>i.value="");

    document.querySelectorAll(".filter-select").forEach(s=>s.selectedIndex=0);

};

/*=========================================================
  MOBILE MENU
=========================================================*/

window.toggleMobileMenu=function(){

    const sidebar=document.getElementById("sidebar");

    sidebar.classList.toggle("mobile-open");

    let overlay=document.querySelector(".sidebar-overlay");

    if(!overlay){

        overlay=document.createElement("div");

        overlay.className="sidebar-overlay";

        overlay.onclick=function(){

            sidebar.classList.remove("mobile-open");

            overlay.classList.remove("open");

        };

        document.body.appendChild(overlay);

    }

    overlay.classList.toggle("open",sidebar.classList.contains("mobile-open"));

};

function sidebarOverlay(){

    let overlay=document.querySelector(".sidebar-overlay");

    if(!overlay){

        overlay=document.createElement("div");

        overlay.className="sidebar-overlay";

        overlay.onclick=function(){

            document.getElementById("sidebar").classList.remove("mobile-open");

            overlay.classList.remove("open");

        };

        document.body.appendChild(overlay);

    }

}

/*=========================================================
  TOPBAR
=========================================================*/

(function renderTopbar(){

    const nav=document.getElementById("topbar-nav");

    if(nav){

        nav.innerHTML=filteredMenu.map(m=>`

            <a href="${m.href||'#'}" data-id="${m.id}">${m.label}</a>

        `).join("");

        const first=nav.querySelector("a");

        if(first)first.classList.add("active");

    }

    const userName=document.getElementById("topbar-user-name");

    if(userName){

        userName.textContent=userData.nome||userData.usuario;

    }

})();

/*=========================================================
  BOOT
=========================================================*/

(function boot(){

    const mod=getModFromUrl();

    if(mod&&moduleMap[mod]){

        currentMod=mod;

        renderWorkspace(mod);

    }else{

        renderLaunchpad();

    }

    console.log("FiscalBrasil ERP loaded —",userData.nome);

})();

/*=========================================================
  ROUTER REGISTRATION
=========================================================*/

FiscalUI.on("fiscalui:ready",function(){

    function goMod(mod){

        if(mod&&moduleMap[mod]){

            currentMod=mod;

            renderWorkspace(mod);

        }else{

            renderLaunchpad();

        }

    }

    FiscalUI.router

        .add("/",()=>renderLaunchpad())

        .add("/nfe",()=>goMod("nfe"))

        .add("/nfce",()=>goMod("nfce"))

        .add("/produtos",()=>goMod("produtos"))

        .add("/clientes",()=>goMod("clientes"))

        .add("/relatorios",()=>goMod("relatorios"))

        .add("/empresas",()=>goMod("empresas"))

        .add("/config",()=>goMod("config"))

        .add("/dashboard",()=>goMod("dashboard"));

    const curPath=window.location.pathname+window.location.search;

    FiscalUI.router.resolve(curPath);

    FiscalUI.state.set("currentPath",curPath);

    FiscalUI.plugins.register("shortcuts",ShortcutsPlugin);

    FiscalUI.plugins.enable("shortcuts");

    var sp=FiscalUI.plugins.get("shortcuts")._instance;

    sp.add(["Ctrl","N"],"Nova NF-e",()=>console.log("Nova NF-e"));

    sp.add(["Ctrl","F"],"Pesquisar",()=>document.querySelector(".filter-input")?.focus());

    sp.add(["Escape"],"Fechar modal",()=>{

        if(FiscalUI.state.get("modalOpen"))FiscalUI.modal.close();

    });

    FiscalUI.on("fiscalui:ready",()=>{

        console.log("FiscalUI v"+FiscalUI.version+" — plugins:",FiscalUI.plugins.list().length);

    });

});

window.goToLaunchpad=function(){

    FiscalUI.router.navigate("/");

};
