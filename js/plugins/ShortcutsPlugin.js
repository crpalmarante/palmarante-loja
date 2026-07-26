const ShortcutsPlugin={

    version:"1.0.0",

    description:"Atalhos de teclado globais do FiscalUI",

    init(api){

        this._api=api;

        this._map={};

        this._handler=(e)=>{

            const key=this._keyStr(e);

            const action=this._map[key];

            if(action){

                e.preventDefault();

                action(e);

            }

        };

        document.addEventListener("keydown",this._handler);

        return this;

    },

    destroy(instance){

        document.removeEventListener("keydown",instance._handler);

    },

    add(keys,description,action){

        const keysStr=Array.isArray(keys)?keys.join("+"):keys;

        this._map[keysStr]=action;

        if(!this._descriptions)this._descriptions={};

        this._descriptions[keysStr]=description;

    },

    _keyStr(e){

        const parts=[];

        if(e.ctrlKey||e.metaKey)parts.push("Ctrl");

        if(e.shiftKey)parts.push("Shift");

        if(e.altKey)parts.push("Alt");

        const key=e.key.length===1?e.key.toUpperCase():e.key;

        if(!["Control","Shift","Alt","Meta"].includes(e.key)){

            parts.push(key);

        }

        return parts.join("+");

    }

};

window.ShortcutsPlugin=ShortcutsPlugin;
