const Format={

    date(date,style="short"){

        if(!date)return"";

        const d=typeof date==="string"?new Date(date):date;

        if(isNaN(d.getTime()))return"";

        if(style==="short")return d.toLocaleDateString("pt-BR");

        if(style==="long")return d.toLocaleDateString("pt-BR",{day:"numeric",month:"long",year:"numeric"});

        if(style==="datetime")return d.toLocaleDateString("pt-BR",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"});

        if(style==="time")return d.toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});

        return d.toLocaleDateString("pt-BR");

    },

    currency(value,symbol="R$"){

        if(value===null||value===undefined)return symbol+" 0,00";

        return symbol+" "+Number(value).toLocaleString("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});

    },

    percent(value){

        if(value===null||value===undefined)return"0,00%";

        return Number(value).toLocaleString("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2})+"%";

    },

    number(value){

        if(value===null||value===undefined)return"0";

        return Number(value).toLocaleString("pt-BR");

    },

    cpf(value){

        if(!value)return"";

        const v=value.replace(/\D/g,"").padStart(11,"0").slice(0,11);

        return v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/,"$1.$2.$3-$4");

    },

    cnpj(value){

        if(!value)return"";

        const v=value.replace(/\D/g,"").padStart(14,"0").slice(0,14);

        return v.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,"$1.$2.$3/$4-$5");

    },

    phone(value){

        if(!value)return"";

        const v=value.replace(/\D/g,"").slice(0,11);

        if(v.length<=10)return v.replace(/(\d{2})(\d{4})(\d{4})/,"($1) $2-$3");

        return v.replace(/(\d{2})(\d{5})(\d{4})/,"($1) $2-$3");

    },

    cep(value){

        if(!value)return"";

        const v=value.replace(/\D/g,"").slice(0,8);

        return v.replace(/(\d{5})(\d{3})/,"$1-$2");

    },

    plural(count,singular,plural){

        return count===1?singular:plural||singular+"s";

    },

    capitalize(str){

        if(!str)return"";

        return str.charAt(0).toUpperCase()+str.slice(1);

    }

};

window.Format=Format;
