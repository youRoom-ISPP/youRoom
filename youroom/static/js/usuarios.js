const buscador = document.getElementById('buscador');
const usuarios = JSON.parse(document.getElementById('usuarios').value);
const resultado = document.getElementById('resultado');

const filtrar = ()=> {
    resultado.innerHTML = '';
    const texto = buscador.value.toLowerCase();


    for(let usuario of usuarios){
        let nombre = usuario.user.username.toLowerCase();
        if(nombre.indexOf(texto) !== -1){
            resultado.innerHTML += '<div class="card tarjeta-listado mb-2 px-3 py-1"> <a class="listado-usuarios" href="/usuarios/'+usuario.user.username+'/">'+ usuario.user.username +'</a> </div>'
        }
    }

    if(resultado.innerHTML === ''){
        resultado.innerHTML += '<i class="listado-usuarios">No se ha encontrado ningún usuario ...</i>'
    }
}

filtrar();

buscador.addEventListener('keyup', filtrar);
