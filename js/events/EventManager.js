class EventManager{

    constructor(){

        this._listeners={};

    }

    on(event,callback){

        if(!this._listeners[event])this._listeners[event]=[];

        this._listeners[event].push(callback);

        return ()=>this.off(event,callback);

    }

    off(event,callback){

        if(!this._listeners[event])return;

        this._listeners[event]=this._listeners[event].filter(cb=>cb!==callback);

    }

    emit(event,data){

        if(!this._listeners[event])return;

        this._listeners[event].forEach(cb=>{

            try{cb(data)}catch(e){console.error("[EventManager]",event,e)}

        });

    }

    once(event,callback){

        const wrapper=(data)=>{

            this.off(event,wrapper);

            callback(data);

        };

        this.on(event,wrapper);

    }

    clear(event){

        if(event){

            delete this._listeners[event];

        }else{

            this._listeners={};

        }

    }

    listeners(event){

        return this._listeners[event]||[];

    }

}

window.EventManager=EventManager;
