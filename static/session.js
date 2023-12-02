
class CreateSession{
    Nova_sessao(nome){
        localStorage.setItem("Usuario",nome)
    }
    Get_sessao(){
        return localStorage.getItem("Usuario")
    }
    Esquecer_sessao(){
        localStorage.removeItem("Usuario")
    }
}

export default CreateSession