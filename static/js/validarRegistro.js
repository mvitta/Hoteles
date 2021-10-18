function eventoBoton() {
    let datos = document.getElementsByClassName("datosRegistro");

    let cedula = datos[0].value;
    let nombre = datos[1].value;
    let apellido = datos[2].value;
    let correo = datos[3].value;
    let contra1 = datos[4].value;
    let contra2 = datos[5].value;
    if (!validarCedula(cedula)) {
        document.getElementById("msgCedula").innerHTML = "Cedula no es valida";
    }

}

function validarCedula(valor) {
    if (valor.match(/^[0-9]+$/)) {
        return true;
    } else {
        return false;
    }
}


