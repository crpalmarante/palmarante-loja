class ModalService{

    constructor(events){

        this._events=events;

        this._overlay=null;

        this._ensureOverlay();

    }

    _ensureOverlay(){

        if(this._overlay)return;

        this._overlay=document.createElement("div");

        this._overlay.className="modal-overlay";

        this._overlay.innerHTML='<div class="modal-box"><div class="modal-header"><h3 class="modal-title"></h3><button class="modal-close">&times;</button></div><div class="modal-body"></div><div class="modal-footer"></div></div>';

        this._overlay.querySelector(".modal-close").onclick=()=>this.close();

        this._overlay.addEventListener("click",e=>{if(e.target===this._overlay)this.close()});

        document.body.appendChild(this._overlay);

    }

    open(config){

        const title=this._overlay.querySelector(".modal-title");

        const body=this._overlay.querySelector(".modal-body");

        const footer=this._overlay.querySelector(".modal-footer");

        title.textContent=config.title||"";

        body.innerHTML="";

        if(typeof config.body==="string"){

            body.innerHTML=config.body;

        }else if(config.body instanceof HTMLElement){

            body.appendChild(config.body);

        }

        footer.innerHTML="";

        if(config.buttons){

            config.buttons.forEach(btn=>{

                const el=document.createElement("button");

                el.textContent=btn.label||"";

                el.className="modal-btn modal-btn-"+((btn.variant||"").toLowerCase()||"primary");

                el.onclick=()=>{

                    if(btn.action)btn.action();

                    if(btn.close!==false)this.close();

                };

                footer.appendChild(el);

            });

        }

        this._overlay.classList.add("modal-open");

        this._events.emit("modal:open",config);

        return this;

    }

    close(){

        this._overlay.classList.remove("modal-open");

        this._events.emit("modal:close",{});

    }

    confirm(message,title="Confirmação"){

        return new Promise(resolve=>{

            this.open({

                title,

                body:"<p>"+message+"</p>",

                buttons:[

                    {label:"Cancelar",variant:"secondary",action:()=>resolve(false)},

                    {label:"Confirmar",variant:"primary",action:()=>resolve(true)},

                ]

            });

        });

    }

    alert(message,title="Aviso"){

        return new Promise(resolve=>{

            this.open({

                title,

                body:"<p>"+message+"</p>",

                buttons:[{label:"OK",variant:"primary",action:()=>resolve(true)}]

            });

        });

    }

}

window.ModalService=ModalService;
