class PluginManager{

    constructor(events,state){

        this._events=events;

        this._state=state;

        this._registry={};

        this._enabled=new Set();

    }

    register(name,plugin){

        if(this._registry[name]){

            this._events.emit("plugin:error",{name,error:"already registered"});

            return this;

        }

        const def={

            name,

            version:plugin.version||"1.0.0",

            description:plugin.description||"",

            dependencies:plugin.dependencies||[],

            _init:typeof plugin==="function"?plugin:plugin.init,

            _destroy:plugin.destroy,

            _enabled:false,

            _instance:null

        };

        this._registry[name]=def;

        this._events.emit("plugin:registered",{name,version:def.version});

        return this;

    }

    enable(name){

        const plugin=this._registry[name];

        if(!plugin){

            this._events.emit("plugin:error",{name,error:"not found"});

            return this;

        }

        if(plugin._enabled)return this;

        for(const dep of plugin.dependencies){

            if(!this._enabled.has(dep)){

                this.enable(dep);

            }

        }

        try{

            const api={

                name:plugin.name,

                version:plugin.version,

                events:this._events,

                state:this._state

            };

            if(plugin._init){

                const result=plugin._init(api);

                plugin._instance=result||true;

            }

            plugin._enabled=true;

            this._enabled.add(name);

            this._events.emit("plugin:enabled",{name});

        }catch(e){

            this._events.emit("plugin:error",{name,error:e});

        }

        return this;

    }

    disable(name){

        const plugin=this._registry[name];

        if(!plugin||!plugin._enabled)return this;

        try{

            if(plugin._destroy){

                plugin._destroy(plugin._instance);

            }

            plugin._instance=null;

            plugin._enabled=false;

            this._enabled.delete(name);

            this._events.emit("plugin:disabled",{name});

        }catch(e){

            this._events.emit("plugin:error",{name,error:e});

        }

        return this;

    }

    enableAll(){

        Object.keys(this._registry).forEach(n=>this.enable(n));

        return this;

    }

    disableAll(){

        Object.keys(this._registry).forEach(n=>this.disable(n));

        return this;

    }

    get(name){

        return this._registry[name]||null;

    }

    isEnabled(name){

        return this._enabled.has(name);

    }

    list(){

        return Object.keys(this._registry).map(name=>{

            const p=this._registry[name];

            return{

                name:p.name,

                version:p.version,

                description:p.description,

                dependencies:p.dependencies,

                enabled:p._enabled

            };

        });

    }

}

window.PluginManager=PluginManager;
