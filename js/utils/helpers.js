const Helpers={

    debounce(fn,wait=300){

        let timer;

        return function(...args){

            clearTimeout(timer);

            timer=setTimeout(()=>fn.apply(this,args),wait);

        };

    },

    throttle(fn,limit=300){

        let inThrottle=false;

        return function(...args){

            if(!inThrottle){

                fn.apply(this,args);

                inThrottle=true;

                setTimeout(()=>inThrottle=false,limit);

            }

        };

    },

    uuid(){

        return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,c=>{

            const r=Math.random()*16|0;

            return(c==="x"?r:r&0x3|0x8).toString(16);

        });

    },

    clamp(value,min,max){

        return Math.min(Math.max(value,min),max);

    },

    randomId(prefix="el"){

        return prefix+"-"+Math.random().toString(36).slice(2,9);

    },

    sleep(ms){

        return new Promise(r=>setTimeout(r,ms));

    },

    truncate(str,len=50){

        if(!str)return"";

        return str.length>len?str.slice(0,len)+"...":str;

    },

    slugify(str){

        if(!str)return"";

        return str

            .toLowerCase()

            .normalize("NFD").replace(/[\u0300-\u036f]/g,"")

            .replace(/[^a-z0-9]+/g,"-")

            .replace(/^-|-$/g,"");

    }

};

window.Helpers=Helpers;
