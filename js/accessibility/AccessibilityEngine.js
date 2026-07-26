class AccessibilityEngine{

    constructor(events,state){

        this._events=events;

        this._state=state;

        this._focusStack=[];

        this._liveRegion=null;

        this._reducedMotion=false;

        this._boundKeyDown=this._onKeyDown.bind(this);

    }

    init(){

        this._reducedMotion=window.matchMedia("(prefers-reduced-motion:reduce)").matches;

        window.matchMedia("(prefers-reduced-motion:reduce)").addEventListener("change",e=>{

            this._reducedMotion=e.matches;

            document.documentElement.classList.toggle("reduced-motion",e.matches);

            this._events.emit("accessibility:reducedMotion",{reduced:e.matches});

        });

        document.documentElement.classList.toggle("reduced-motion",this._reducedMotion);

        this._ensureLiveRegion();

        this._ensureSkipLink();

        this._watchDynamicContent();

        this._events.on("modal:open",()=>{

            requestAnimationFrame(()=>this._trapFocus());

        });

        this._events.on("modal:close",()=>{

            this._releaseFocus();

        });

        this._events.on("toast:show",({message})=>{

            this.announce(message,"polite");

        });

        if(this._state){

            this._state.define("reducedMotion",this._reducedMotion);

            this._state.define("focusTrapActive",false);

        }

        document.addEventListener("keydown",this._boundKeyDown);

        this._events.emit("accessibility:ready",{});

    }

    destroy(){

        document.removeEventListener("keydown",this._boundKeyDown);

    }

    announce(message,priority="polite"){

        if(!this._liveRegion)this._ensureLiveRegion();

        const region=this._liveRegion;

        region.setAttribute("aria-live",priority);

        region.textContent="";

        requestAnimationFrame(()=>{

            region.textContent=message;

        });

    }

    focus(el){

        if(!el)return;

        el.setAttribute("tabindex","-1");

        el.focus();

    }

    trapFocus(container){

        this._focusTrapContainer=container;

        this._focusTrapActive=true;

        if(this._state)this._state.set("focusTrapActive",true);

        const focusable=this._getFocusable(container);

        if(focusable.length){

            focusable[0].focus();

        }

    }

    releaseFocus(){

        this._focusTrapActive=false;

        this._focusTrapContainer=null;

        if(this._state)this._state.set("focusTrapActive",false);

        const last=this._focusStack.pop();

        if(last)last.focus();

    }

    saveFocus(){

        this._focusStack.push(document.activeElement);

    }

    _ensureLiveRegion(){

        if(this._liveRegion)return;

        this._liveRegion=document.createElement("div");

        this._liveRegion.className="sr-only live-region";

        this._liveRegion.setAttribute("aria-live","polite");

        this._liveRegion.setAttribute("aria-atomic","true");

        document.body.appendChild(this._liveRegion);

    }

    _ensureSkipLink(){

        if(document.querySelector(".skip-link"))return;

        const link=document.createElement("a");

        link.className="skip-link";

        link.href="#main-content";

        link.textContent="Pular para o conteúdo principal";

        document.body.insertBefore(link,document.body.firstChild);

        const main=document.getElementById("workspace-view")||document.querySelector("main");

        if(main&&!main.id)main.id="main-content";

    }

    _trapFocus(){

        const modal=document.querySelector(".modal-overlay.modal-open");

        if(!modal)return;

        this.saveFocus();

        this.trapFocus(modal);

    }

    _releaseFocus(){

        this.releaseFocus();

    }

    _getFocusable(container){

        if(!container)return[];

        const selectors='a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

        const items=Array.from(container.querySelectorAll(selectors));

        return items.filter(el=>el.offsetParent!==null);

    }

    _onKeyDown(e){

        if(this._focusTrapActive&&e.key==="Tab"){

            const container=this._focusTrapContainer;

            if(!container)return;

            const focusable=this._getFocusable(container);

            if(focusable.length===0){

                e.preventDefault();

                return;

            }

            const first=focusable[0];

            const last=focusable[focusable.length-1];

            if(e.shiftKey){

                if(document.activeElement===first){

                    e.preventDefault();

                    last.focus();

                }

            }else{

                if(document.activeElement===last){

                    e.preventDefault();

                    first.focus();

                }

            }

        }

        if(e.key==="Escape"){

            if(this._focusTrapActive){

                this._events.emit("key:escape",{});

            }

        }

    }

    _watchDynamicContent(){

        const observer=new MutationObserver(()=>{

            const toasts=document.querySelectorAll(".toast:not([role])");

            toasts.forEach(t=>{

                t.setAttribute("role","alert");

            });

            const modals=document.querySelectorAll(".modal-overlay:not([role])");

            modals.forEach(m=>{

                m.setAttribute("role","dialog");

                m.setAttribute("aria-modal","true");

            });

        });

        observer.observe(document.body,{childList:true,subtree:true});

    }

}

window.AccessibilityEngine=AccessibilityEngine;
