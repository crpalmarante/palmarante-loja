class LoadingService{

    constructor(events){

        this._events=events;

        this._count=0;

        this._el=null;

        this._ensureElement();

    }

    _ensureElement(){

        if(this._el)return;

        this._el=document.createElement("div");

        this._el.className="loading-overlay";

        this._el.innerHTML='<div class="loading-spinner"><div class="spinner-ring"></div><p class="loading-text">Carregando...</p></div>';

        document.body.appendChild(this._el);

    }

    show(text){

        this._count++;

        this._el.querySelector(".loading-text").textContent=text||"Carregando...";

        this._el.classList.add("loading-active");

        this._events.emit("loading:show",{text});

    }

    hide(){

        if(this._count>0)this._count--;

        if(this._count===0)this._el.classList.remove("loading-active");

        this._events.emit("loading:hide",{});

    }

    async wrap(promise,text){

        this.show(text);

        try{

            return await promise;

        }finally{

            this.hide();

        }

    }

}

window.LoadingService=LoadingService;
