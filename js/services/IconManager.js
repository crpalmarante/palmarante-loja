class IconManager{

    constructor(events){

        this._events=events;

        this._cache={};

        this._loaded=false;

    }

    async loadSprite(url="img/icons.svg"){

        if(this._loaded)return;

        try{

            const res=await fetch(url);

            const svg=await res.text();

            const div=document.createElement("div");

            div.style.display="none";

            div.innerHTML=svg;

            document.body.insertBefore(div,document.body.firstChild);

            this._loaded=true;

            this._events.emit("icons:loaded",{url});

        }catch(e){

            this._events.emit("icons:error",{url,error:e});

            console.warn("IconManager: sprite not loaded",url);

        }

    }

    html(name,size="sm",extra=""){

        const cls=["icon","icon-"+size,extra].filter(Boolean).join(" ");

        return'<svg class="'+cls+'" aria-hidden="true"><use href="#'+name+'"/></svg>';

    }

    btn(name,size="sm",ariaLabel){

        const label=ariaLabel||name.replace("icon-","");

        return'<button class="icon-btn" aria-label="'+label+'" title="'+label+'">'+

            this.html(name,size)+

        '</button>';

    }

    text(name,label,size="sm"){

        return'<span class="icon-text">'+

            this.html(name,size)+

            '<span>'+label+'</span>'+

        '</span>';

    }

    isLoaded(){

        return this._loaded;

    }

}

window.IconManager=IconManager;
