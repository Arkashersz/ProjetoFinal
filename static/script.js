import CreateSession from "./session.js"

//Verificar se existe uma sessao logada 
let Create_se = new CreateSession()
console.log(Create_se.Get_sessao())
if(Create_se.Get_sessao() != null){
    window.location.href = `http://127.0.0.1:5000/home/${Create_se.Get_sessao()}`
}

