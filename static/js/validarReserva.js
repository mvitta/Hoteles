const formulario = document.getElementById('formulario_html5');
const imprimirError = document.getElementById('msgError');

function validarTelefono(valor) {
    if (valor.match(/^[0-9]+$/)) {
        return true;
    } else {
        return false;
    }
}

function validarNombre(valor) {
    if (valor.match(/^[A-Za-z]+$/)) {
        return true;
    }
    else {
        return false;
    }
}

function validarApellido(valor) {
    if (valor.match(/^[A-Za-z]+$/)) {
        return true;
    }
    else {
        return false;
    }
}

function validarCorreo(valor) {
    if (valor.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)) {
        return true;
    }
    else {
        return false;
    }
}

formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    let error = "";
    let estado = "";
    const datos = document.getElementsByClassName('cajas');
    let nombre = datos[0].value;
    let apellido = datos[1].value;
    let correo = datos[2].value;
    let telefono = datos[3].value;
    let llegada = datos[4].value;
    let salida = datos[5].value;
    let permanencia = datos[6].value
    let numeroPersonas = datos[7].value
    let nivelEstudio = datos[8].value
    console.log([nombre, apellido, correo, telefono, llegada, salida, permanencia, numeroPersonas, nivelEstudio])
    if (!validarNombre(nombre)) {
        error += "<br><br> Nombre no es valido <br>";
    }
    else {
        estado = "OK";
    }
    if (!validarApellido(apellido)) {
        error += "Apellido no es valido <br>";
    }
    else {
        estado = "OK";
    }
    if (!validarCorreo(correo)) {
        error += "Correo no es valido <br>";
    }
    else {
        estado = "OK";
    }
    if (!validarTelefono(telefono)) {
        error += "Telefono no es valido <br>";
    }
    else {
        estado = "OK";
    }
    if (llegada == "") {
        error += "Debe selecionar una fecha de llegada <br>"
    }
    else {
        estado = "OK"
    }
    if (salida == "") {
        error += "Debe selecionar una fecha de salida <br>"
    }
    else {
        estado = "OK"
    }

    imprimirError.innerHTML = error;

});






