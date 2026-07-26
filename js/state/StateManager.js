class StateManager{

    constructor(events){

        this._events=events;

        this._state={};

        this._initial={};

    }

    define(key,defaultValue){

        this._state[key]=defaultValue;

        this._initial[key]=defaultValue;

    }

    get(key){

        return this._state[key];

    }

    set(key,value){

        const prev=this._state[key];

        if(prev===value)return;

        this._state[key]=value;

        this._events.emit("state:"+key,{key,value,prev});

        this._events.emit("state:change",{key,value,prev});

    }

    toggle(key){

        this.set(key,!this._state[key]);

    }

    reset(key){

        if(key){

            this.set(key,this._initial[key]);

        }else{

            Object.keys(this._state).forEach(k=>this.set(k,this._initial[k]));

        }

    }

    all(){

        return{...this._state};

    }

    observe(key,callback){

        this._events.on("state:"+key,callback);

        callback({key,value:this._state[key],prev:undefined});

    }

}

window.StateManager=StateManager;
