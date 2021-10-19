const form = document.getElementById("formulario");
const errorCedula = document.getElementById("msgCedula");
const errorNombre = document.getElementById("msgNombre");
const errorApellido = document.getElementById("msgApellido");
const errorCorreo = document.getElementById("msgCorreo");
const errorContra1 = document.getElementById("msgPass1");
const errorContra2 = document.getElementById("msgPass2");

function validarCedula(valor) {
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

function validarContra1(valor) {
    if (valor.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$/)) {
        return true;
    }
    else {
        return false;
    }
}

function validarContra2(valor) {
    if (valor.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$/)) {
        return true;
    }
    else {
        return false;
    }
}

form.addEventListener('submit', e => {
    e.preventDefault();
    let estado = "";
    // datos
    let datos = document.getElementsByClassName("datosRegistro");
    let cedula = datos[0].value;
    let nombre = datos[1].value;
    let apellido = datos[2].value;
    let correo = datos[3].value;
    let contra1 = datos[4].value;
    let contra2 = datos[5].value;

    console.log([cedula, nombre, apellido, correo, contra1, contra2, terminos])
    // reinicio de errores
    errorCedula.innerHTML = "";
    errorNombre.innerHTML = "";
    errorApellido.innerHTML = "";
    errorCorreo.innerHTML = "";
    errorContra1.innerHTML = "";
    errorContra2.innerHTML = "";
    // validaciones
    if (!validarCedula(cedula)) {
        errorCedula.innerHTML = "La cedula no es valida";
    }
    else {
        estado += "OK";
    }
    if (!validarNombre(nombre)) {
        errorNombre.innerHTML = "El nombre no es valido";
    }
    else {
        estado += "OK";
    }
    if (!validarApellido(apellido)) {
        errorApellido.innerHTML = "El apellido no es valido";
    }
    else {
        estado += "OK";
    }
    if (!validarCorreo(correo)) {
        errorCorreo.innerHTML = "El Correo no es valido";
    }
    else {
        estado += "OK";
    }
    if (!validarContra1(contra1)) {
        errorContra1.innerHTML = "La Contraseña no es valida";
    }
    else {
        estado += "OK";
    }
    if (!validarContra2(contra2)) {
        errorContra2.innerHTML = "La Contraseña no es valida";
    }
    else {
        estado += "OK";
    }

    if (estado == "OKOKOKOKOKOK") {
        document.getElementsByClassName('msgEnviado')[0].innerHTML = "Enviado";
    }
})





