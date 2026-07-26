class ToastService{

    constructor(events){

        this._events=events;

        this._container=null;

        this._ensureContainer();

    }

    _ensureContainer(){

        if(this._container)return;

        this._container=document.createElement("div");

        this._container.className="toast-container";

        document.body.appendChild(this._container);

    }

    show(message,type="info",duration=4000){

        const toast=document.createElement("div");

        toast.className="toast toast-"+type;

        toast.innerHTML='<span class="toast-msg">'+message+'</span><button class="toast-close">&times;</button>';

        toast.querySelector(".toast-close").onclick=()=>this._dismiss(toast);

        this._container.appendChild(toast);

        requestAnimationFrame(()=>toast.classList.add("toast-visible"));

        if(duration>0)setTimeout(()=>this._dismiss(toast),duration);

        this._events.emit("toast:show",{message,type});

        return toast;

    }

    _dismiss(toast){

        toast.classList.remove("toast-visible");

        toast.addEventListener("transitionend",()=>toast.remove());

    }

    success(msg,d){return this.show(msg,"success",d)}

    error(msg,d){return this.show(msg,"error",d)}

    warning(msg,d){return this.show(msg,"warning",d)}

    info(msg,d){return this.show(msg,"info",d)}

}

window.ToastService=ToastService;
