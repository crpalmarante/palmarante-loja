class ErrorManager{

    constructor(events,toast){

        this._events=events;

        this._toast=toast;

        this._history=[];

        this._maxHistory=50;

        this._onErrorBound=this._onError.bind(this);

        this._onRejectBound=this._onReject.bind(this);

    }

    init(){

        window.addEventListener("error",this._onErrorBound);

        window.addEventListener("unhandledrejection",this._onRejectBound);

        this._events.emit("error:ready",{});

    }

    destroy(){

        window.removeEventListener("error",this._onErrorBound);

        window.removeEventListener("unhandledrejection",this._onRejectBound);

    }

    capture(error,context={}){

        const entry=this._normalize(error,context);

        this._record(entry);

        this._events.emit("error:captured",entry);

        if(entry.level==="error"||entry.level==="fatal"){

            this._notify(entry);

        }

        return entry;

    }

    wrap(fn,context={}){

        const self=this;

        return function(...args){

            try{

                return fn.apply(this,args);

            }catch(e){

                self.capture(e,context);

            }

        };

    }

    wrapAsync(promise,context={}){

        const self=this;

        return promise.catch(e=>{

            self.capture(e,context);

            throw e;

        });

    }

    info(message,context){

        return this.capture(new Error(message),{...context,level:"info"});

    }

    warn(message,context){

        return this.capture(new Error(message),{...context,level:"warning"});

    }

    error(message,context){

        return this.capture(new Error(message),{...context,level:"error"});

    }

    fatal(message,context){

        return this.capture(new Error(message),{...context,level:"fatal"});

    }

    history(){

        return[...this._history];

    }

    clearHistory(){

        this._history=[];

    }

    _normalize(error,context={}){

        const message=error?.message||error?.reason||String(error);

        const stack=error?.stack||"";

        const level=context.level||"error";

        return{

            id:Helpers.uuid(),

            message,

            stack,

            level,

            timestamp:new Date().toISOString(),

            url:window.location.href,

            context

        };

    }

    _record(entry){

        this._history.unshift(entry);

        if(this._history.length>this._maxHistory){

            this._history.pop();

        }

        const method=entry.level==="fatal"?"error":entry.level==="warning"?"warn":"error";

        console[method](

            "[ErrorManager] %c%s",

            "color:"+(entry.level==="fatal"?"#ef4444":entry.level==="warning"?"#f59e0b":"#3b82f6"),

            entry.message

        );

    }

    _notify(entry){

        if(!this._toast)return;

        const msgs={

            error:"Ocorreu um erro inesperado.",

            fatal:"Erro crítico. Entre em contato com o suporte."

        };

        this._toast.error(msgs[entry.level]||entry.message);

    }

    _onError(e){

        this.capture(e.error||e,{

            level:"error",

            source:e.filename,

            line:e.lineno,

            col:e.colno

        });

    }

    _onReject(e){

        this.capture(e.reason,{level:"error",type:"unhandledrejection"});

    }

}

window.ErrorManager=ErrorManager;
