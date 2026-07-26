class ResponsiveEngine{

    constructor(events,state){

        this._events=events;

        this._state=state;

        this._bp={

            xs:{min:0,max:575,label:"Telefone"},

            sm:{min:576,max:767,label:"Telefone Grande"},

            md:{min:768,max:1023,label:"Tablet"},

            lg:{min:1024,max:1439,label:"Notebook"},

            xl:{min:1440,max:1919,label:"Desktop"},

            xxl:{min:1920,max:Infinity,label:"UltraWide"}

        };

        this._bpOrder=["xs","sm","md","lg","xl","xxl"];

        this._current=null;

        this._prev=null;

        this._boundCheck=this._check.bind(this);

        this._resizeTimer=null;

    }

    init(){

        this._check();

        window.addEventListener("resize",this._boundCheck);

        window.addEventListener("orientationchange",()=>{

            setTimeout(this._boundCheck,200);

        });

        if(this._state){

            this._state.define("breakpoint","xl");

            this._state.define("isMobile",false);

            this._state.define("isTablet",false);

            this._state.define("isDesktop",true);

            this._state.define("viewportWidth",window.innerWidth);

            this._state.define("viewportHeight",window.innerHeight);

        }

        this._events.emit("responsive:ready",{breakpoint:this._current});

    }

    destroy(){

        window.removeEventListener("resize",this._boundCheck);

        window.removeEventListener("orientationchange",this._boundCheck);

    }

    get breakpoint(){return this._current}

    get prevBreakpoint(){return this._prev}

    is(name){return this._current===name}

    isMobile(){return this._current==="xs"||this._current==="sm"}

    isTablet(){return this._current==="md"}

    isDesktop(){return["lg","xl","xxl"].includes(this._current)}

    atLeast(minBp){

        const idx=this._bpOrder.indexOf(minBp);

        const cur=this._bpOrder.indexOf(this._current);

        return cur>=idx;

    }

    atMost(maxBp){

        const idx=this._bpOrder.indexOf(maxBp);

        const cur=this._bpOrder.indexOf(this._current);

        return cur<=idx;

    }

    between(minBp,maxBp){

        return this.atLeast(minBp)&&this.atMost(maxBp);

    }

    width(){return window.innerWidth}

    height(){return window.innerHeight}

    _check(){

        const w=window.innerWidth;

        const h=window.innerHeight;

        let matched=null;

        for(const id of this._bpOrder){

            const bp=this._bp[id];

            if(w>=bp.min&&w<=bp.max){matched=id;break}

        }

        if(!matched)matched="xl";

        if(matched!==this._current){

            this._prev=this._current;

            this._current=matched;

            this._events.emit("responsive:change",{

                breakpoint:this._current,

                prev:this._prev,

                width:w,

                height:h

            });

            if(this._state){

                this._state.set("breakpoint",this._current);

                this._state.set("isMobile",this.isMobile());

                this._state.set("isTablet",this.isTablet());

                this._state.set("isDesktop",this.isDesktop());

                this._state.set("viewportWidth",w);

                this._state.set("viewportHeight",h);

            }

        }

    }

}

window.ResponsiveEngine=ResponsiveEngine;
