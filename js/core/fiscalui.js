/*=========================================================
    FiscalBrasil UI
    File    : fiscalui.js
    JavaScript Core — orquestrador do Framework.
=========================================================*/

(function(){

    "use strict";

    const events=new EventManager();

    const state=new StateManager(events);

    const storage=new StorageService();

    const toast=new ToastService(events);

    const loading=new LoadingService(events);

    const modal=new ModalService(events);

    const errors=new ErrorManager(events,toast);

    const router=new Router(events,state);

    const responsive=new ResponsiveEngine(events,state);

    const plugins=new PluginManager(events,state);

    const a11y=new AccessibilityEngine(events,state);

    const icons=new IconManager(events);

    const form=new FormService(events);

    state.define("theme","dark");

    state.define("sidebarCollapsed",false);

    state.define("currentPage","launchpad");

    state.define("user",null);

    state.define("filters",{});

    state.define("lang","pt-BR");

    state.define("modalOpen",false);

    state.define("loading",false);

    const FiscalUI={

        version:"0.1.0",

        events,

        state,

        storage,

        toast,

        loading,

        modal,

        router,

        responsive,

        plugins,

        errors,

        a11y,

        icons,

        form,

        Format,

        Helpers,

        init(){

            function syncThemeIcon(theme){

                const iconMap={dark:"icon-moon",light:"icon-sun","high-contrast":"icon-eye"};

                const icon=document.getElementById("theme-icon");

                if(icon)icon.setAttribute("href","#"+iconMap[theme]);

            }

            const savedTheme=storage.get("theme","dark");

            state.set("theme",savedTheme);

            document.documentElement.setAttribute("data-theme",savedTheme);

            syncThemeIcon(savedTheme);

            state.observe("theme",({value})=>{

                document.documentElement.setAttribute("data-theme",value);

                storage.set("theme",value);

                syncThemeIcon(value);

            });

            state.observe("sidebarCollapsed",({value})=>{

                const el=document.getElementById("sidebar");

                if(el)el.classList.toggle("collapsed",value);

                storage.set("sidebar_collapsed",value);

            });

            const savedSidebar=storage.get("sidebar_collapsed",false);

            if(savedSidebar)state.set("sidebarCollapsed",true);

            router.interceptClicks();

            router.init();

            responsive.init();

            errors.init();

            a11y.init();

            icons.loadSprite();

            form.init();

            events.emit("fiscalui:ready",{version:this.version});

        },

        on(event,callback){

            events.on(event,callback);

        },

        emit(event,data){

            events.emit(event,data);

        }

    };

    window.FiscalUI=FiscalUI;

    document.addEventListener("DOMContentLoaded",()=>FiscalUI.init());

})();
