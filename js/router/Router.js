class Router{

    constructor(events,state){

        this._routes=[];

        this._events=events;

        this._state=state;

        this._currentPath=null;

        this._boundPop=this._onPopstate.bind(this);

    }

    add(pattern,handler){

        const parts=pattern.split("/").filter(Boolean);

        const regexParts=parts.map(p=>{

            if(p.startsWith(":"))return"(?<"+p.slice(1)+">[^/]+)";

            if(p==="*")return".*";

            return p.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");

        });

        const regex=new RegExp("^/?"+regexParts.join("/")+"$");

        this._routes.push({pattern,regex,handler,parts});

        return this;

    }

    resolve(path){

        if(!path||path==="#"||path==="")path="/";

        if(!path.startsWith("/"))path="/"+path;

        const qIdx=path.indexOf("?");

        const searchParams={};

        if(qIdx!==-1){

            new URLSearchParams(path.slice(qIdx)).forEach((v,k)=>searchParams[k]=v);

            path=path.slice(0,qIdx);

        }

        for(const route of this._routes){

            const m=path.match(route.regex);

            if(m){

                const params={...m.groups};

                return{handler:route.handler,params,path,searchParams};

            }

        }

        return null;

    }

    navigate(path,{replace=false,title=""}={}){

        if(!path||path==="#"||path==="")path="/";

        const resolved=this.resolve(path);

        if(!resolved){

            this._events.emit("router:not-found",{path});

            return this;

        }

        const method=replace?"replaceState":"pushState";

        history[method]({path},title||"FiscalBrasil",path);

        this._apply(resolved);

        return this;

    }

    init(basePath="/"){

        window.addEventListener("popstate",this._boundPop);

        this._events.on("router:navigate",({path,replace,title})=>{

            this.navigate(path,{replace,title});

        });

        const initialPath=window.location.pathname+window.location.search||basePath;

        const resolved=this.resolve(initialPath);

        if(resolved){

            this._apply(resolved);

        }else{

            const mod=new URLSearchParams(window.location.search).get("mod");

            if(mod){

                this._events.emit("router:mod",{mod,params:{}});

            }else{

                this._events.emit("router:not-found",{path:initialPath});

            }

        }

    }

    destroy(){

        window.removeEventListener("popstate",this._boundPop);

    }

    _apply(resolved){

        this._currentPath=resolved.path;

        if(this._state){

            const params=new URLSearchParams(resolved.searchParams).toString();

            const fullPath=resolved.path+(params?"?"+params:"");

            this._state.set("currentPath",fullPath);

        }

        this._events.emit("router:before",resolved);

        resolved.handler(resolved);

        this._events.emit("router:after",resolved);

    }

    _onPopstate(e){

        const path=e.state?.path||window.location.pathname+window.location.search;

        const resolved=this.resolve(path);

        if(resolved){

            this._apply(resolved);

        }else{

            this._events.emit("router:not-found",{path});

        }

    }

    linkHandler(e){

        const a=e.target.closest("a");

        if(!a)return;

        const href=a.getAttribute("href");

        if(!href||href.startsWith("#")||href.startsWith("http")||href.startsWith("//")||a.hasAttribute("download")||a.hasAttribute("target"))return;

        e.preventDefault();

        this.navigate(href);

    }

    interceptClicks(){

        document.addEventListener("click",this.linkHandler.bind(this));

    }

}

window.Router=Router;
