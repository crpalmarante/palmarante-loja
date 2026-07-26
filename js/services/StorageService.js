class StorageService{

    constructor(prefix="fiscalui_"){

        this._prefix=prefix;

    }

    _key(k){return this._prefix+k}

    get(key,fallback=null){

        try{

            const raw=localStorage.getItem(this._key(key));

            if(raw===null)return fallback;

            return JSON.parse(raw);

        }catch{

            return fallback;

        }

    }

    set(key,value){

        try{

            localStorage.setItem(this._key(key),JSON.stringify(value));

            return true;

        }catch{

            return false;

        }

    }

    remove(key){

        localStorage.removeItem(this._key(key));

    }

    clear(){

        const keys=Object.keys(localStorage).filter(k=>k.startsWith(this._prefix));

        keys.forEach(k=>localStorage.removeItem(k));

    }

    has(key){

        return localStorage.getItem(this._key(key))!==null;

    }

}

window.StorageService=StorageService;
