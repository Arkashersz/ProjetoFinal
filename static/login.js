import CreateSession from "./session.js"
let url = window.location.href.split("/")
let session = new CreateSession()

session.Nova_sessao(url[url.length - 1])

document.getElementById("logout").addEventListener("click",()=>{
  session.Esquecer_sessao()  
  window.location.href = "http://127.0.0.1:5000/login"
})

