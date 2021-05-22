//   DECLARACION DE VARIABLES
var botones = document.querySelector('#botones')
const displayName = document.querySelector('#displayName');
const emailDisplay = document.querySelector('#email');
const contenido_log = document.querySelector('#contenido_log');
const amigos_list = document.querySelector('#amigos_list');
const chat_log = document.querySelector('#chat_log');
const form_chat = document.querySelector('#form_chat');
const input_chat = document.querySelector('#input_chat');
var userLocalUID = null;
var uid_contacto = null;



var db = firebase.firestore();




//   AUTENTICACION
firebase.auth().onAuthStateChanged((user) => {
  OnlineUser();  
  if (user) {
    userLocalUID=user.uid;
    //   console.log(user)            
    document.getElementById("imgAvatar").src = user.photoURL
    displayName.innerHTML = user.displayName
    emailDisplay.innerHTML = user.email

    botones.innerHTML = /*html*/`
      <button class="btn btn-app-red btn-block" type="button" id="btn_cerrar">Salir</button>
      `
    contenido_log.style.visibility = "visible";

    // ...
    cerrarSesion(user);
    contenidoChat(user);
    // obtenmensajes(user);
    updateSesion(user, true)
    // impresion_consola(user);

  } else {
    botones.innerHTML = /*html*/`
         <button class="btn btn-app-teal btn-block" type="button" id="btn_entrar">Entrar</button>
        `
    displayName.innerHTML = ''
    emailDisplay.innerHTML = ''
    document.getElementById("imgAvatar").src = ''
    iniciarSesion();
    contenido_log.style.visibility = "hidden";


  }
});


const iniciarSesion = () => {
  const btnentrar = document.querySelector('#btn_entrar');
  btnentrar.addEventListener('click', async () => {
    try {
      var provider = new firebase.auth.GoogleAuthProvider();
      await firebase.auth().signInWithPopup(provider)
    } catch (error) {
      console.log(error)
    }
  });
}



const cerrarSesion = (user) => {
  const btnCerrarSesion = document.querySelector('#btn_cerrar');
  btnCerrarSesion.addEventListener('click', () => {
    firebase.auth().signOut();
    updateSesion(user, false);
  });
}




const contenidoChat = (user) => {
  form_chat.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!input_chat.value.trim()) {
      console.log('Input vacio')
      return
    }

    firebase.firestore().collection('chat').add({
      texto: input_chat.value,
      uid: uid_contacto,
      to_uid: user.uid,
      fecha: Date.now(),      
    })
      .then(resp => {
        console.log('mensaje guardado')
        input_chat.value = ''
      })
      .catch(e => {
        console.log(e)
      })






  });
}

const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
function obtenmensajes() {
  chat_log.innerHTML = ''

  db.collection("chat").orderBy('fecha').where("to_uid", "==",  userLocalUID).where("uid", "==",  uid_contacto)
    .onSnapshot((querySnapshot) => {        
      chat_log.innerHTML = ''          
        querySnapshot.forEach((doc) => {  
          if (doc.data().uid == userLocalUID) {
            var fecha = new Date(doc.data().fecha)
            chat_log.innerHTML += /*html*/`        
              <blockquote class="blockquote-reverse"> <p>${doc.data().texto}</p> 
              <footer>${fecha.toLocaleString(undefined, options)}</footer> 
              </blockquote>
              `
          }
          else {
            var fecha = new Date(doc.data().fecha)
            chat_log.innerHTML += /*html*/`
              <blockquote> <p>${doc.data().texto}</p> 
              <footer>${fecha.toLocaleString(undefined, options)}</footer> 
              </blockquote>
              `
          }
        });
        topScroll();
    });



    topScroll();

}





///////////////////////////////////////////////////////////////////////////////////////


const OnlineUser = () => {

  db.collection("sesion")
    .onSnapshot((querySnapshot) => {
      amigos_list.innerHTML = ''
      querySnapshot.forEach((doc) => {
        if (doc.id != userLocalUID) {          
          if (doc.data().status == 'true') {
            console.log(doc.data().nombre+" "+doc.data().status)
            amigos_list.innerHTML += /*html*/`
                <li>
                    <a href="#amigos_lista" onclick="SelectIDChat('${doc.id}')">
                        <img class="img-avatar" src="${doc.data().avatar}" alt="">
                        <i class="ion-record text-green"></i> ${doc.data().nombre}
                        <div class="text-muted"><small>${doc.data().email}</small></div>
                    </a>
                </li>  
                `
          } else {
            amigos_list.innerHTML += /*html*/`
                <li>
                  <a href="#amigos_lista" onclick="SelectIDChat('${doc.id}')">
                      <img class="img-avatar" src="${doc.data().avatar}" alt="">
                      <i class="ion-record hidden"></i> ${doc.data().nombre}
                      <div class="text-muted"><small>${doc.data().email}</small></div>
                  </a>
                </li> 
                `
          }
        }





      });

    });

}




function updateSesion(user, estado) {
  db.collection("sesion").doc(user.uid).set({
    nombre: user.displayName,
    avatar: user.photoURL,
    email: user.email,
    status: `${estado}`

  })
    .then(() => {
      console.log("Document successfully written!");
    })
    .catch((error) => {
      console.error("Error writing document: ", error);
    });
}






function SelectIDChat(id) {  
  uid_contacto=id
  obtenmensajes();
}

function topScroll() {
  chat_log.scrollTop = chat_log.scrollHeight
}