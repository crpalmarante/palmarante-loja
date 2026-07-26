/*=========================================================
    FiscalBrasil ERP
    File    : login.js
=========================================================*/

/*=========================================================
  STATE
=========================================================*/

const state={

    token:localStorage.getItem("auth_token"),

    mode:"signin"

};

if(state.token){

    window.location.href="index.html";

}

/*=========================================================
  DOM
=========================================================*/

const card=document.getElementById("login-card");

const subtitle=document.getElementById("login-subtitle");

/* sign in */

const siForm=document.getElementById("signin-form");

const siUser=document.getElementById("login-user");

const siPass=document.getElementById("login-pass");

const siError=document.getElementById("login-error");

const siLoading=document.getElementById("login-loading");

const siBtn=document.getElementById("login-btn");

/* sign up */

const suForm=document.getElementById("signup-form");

const suName=document.getElementById("reg-name");

const suUser=document.getElementById("reg-user");

const suPass=document.getElementById("reg-pass");

const suEmail=document.getElementById("reg-email");

const suError=document.getElementById("reg-error");

const suLoading=document.getElementById("reg-loading");

const suBtn=document.getElementById("reg-btn");

/*=========================================================
  TOGGLE
=========================================================*/

document.addEventListener("click",function(e){

    var btn=e.target.closest(".toggle-btn");

    if(!btn) return;

    siError.classList.remove("visible","success");

    suError.classList.remove("visible");

    if(state.mode==="signin"){

        state.mode="signup";

        card.classList.add("sign-up-mode");

        subtitle.textContent="Crie sua conta";

    }else{

        state.mode="signin";

        card.classList.remove("sign-up-mode");

        subtitle.textContent="Faça login para continuar";

    }

});

/*=========================================================
  SIGN IN
=========================================================*/

siForm.addEventListener("submit",async function(e){

    e.preventDefault();

    const usuario=siUser.value.trim();

    const senha=siPass.value.trim();

    if(!usuario||!senha){

        showError(siError,"Preencha usuário e senha");

        return;

    }

    setLoading(siLoading,siBtn,true);

    siError.classList.remove("visible","success");

    try{

        const res=await fetch("/api/auth/login",{

            method:"POST",

            headers:{"Content-Type":"application/x-www-form-urlencoded"},

            body:new URLSearchParams({usuario,senha})

        });

        const data=await res.json();

        if(data.status!=="ok"){

            showError(siError,data.mensagem||"Usuário ou senha incorretos");

            setLoading(siLoading,siBtn,false);

            return;

        }

        state.token=data.token;

        localStorage.setItem("auth_token",data.token);

        localStorage.setItem("pos_usuario",JSON.stringify(data));

        window.location.href="index.html";

    }catch(err){

        showError(siError,"Erro de conexão com o servidor");

        setLoading(siLoading,siBtn,false);

    }

});

/*=========================================================
  SIGN UP
=========================================================*/

suForm.addEventListener("submit",async function(e){

    e.preventDefault();

    const nome=suName.value.trim();

    const usuario=suUser.value.trim();

    const senha=suPass.value.trim();

    const email=suEmail.value.trim();

    if(!nome||!usuario||!senha||!email){

        showError(suError,"Preencha todos os campos");

        return;

    }

    setLoading(suLoading,suBtn,true);

    suError.classList.remove("visible");

    try{

        const res=await fetch("/api/auth/register",{

            method:"POST",

            headers:{"Content-Type":"application/x-www-form-urlencoded"},

            body:new URLSearchParams({nome,usuario,senha,email})

        });

        const data=await res.json();

        if(data.status!=="ok"){

            showError(suError,data.mensagem||"Erro ao criar conta");

            setLoading(suLoading,suBtn,false);

            return;

        }

        suForm.reset();

        setLoading(suLoading,suBtn,false);

        suError.classList.remove("visible");

        state.mode="signin";

        card.classList.remove("sign-up-mode");

        subtitle.textContent="Faça login para continuar";

        siError.textContent="Conta criada com sucesso! Faça login.";

        siError.classList.add("visible","success");

    }catch(err){

        showError(suError,"Erro de conexão com o servidor");

        setLoading(suLoading,suBtn,false);

    }

});

/*=========================================================
  UI HELPERS
=========================================================*/

function showError(el,msg){

    el.textContent=msg;

    el.classList.add("visible");

}

function setLoading(loadingEl,btnEl,on){

    if(on){

        loadingEl.classList.add("visible");

        btnEl.disabled=true;

    }else{

        loadingEl.classList.remove("visible");

        btnEl.disabled=false;

    }

}
