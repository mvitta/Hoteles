from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, redirect, url_for, session, request
from flask import g
import os
from validaciones import isUsernameValid, isPasswordValid
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(34)
DATABASE_USUARIO = "hotel.db"
claveUsuario = None
claveAdmin = None
claveSuper = None
Habitaciones = None
idHab = None
idParaReservas = None
valida = None


def conexionBaseDeDatos():
    db = getattr(g, '_database_USUARIO', None)
    if db is None:
        db = g._database_USUARIO = sqlite3.connect(DATABASE_USUARIO)
    return db


def usuarioExiste(cedula):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT * FROM usuarios WHERE cedula=?"
    cur.execute(sql, [cedula])
    conexion.commit()
    info = cur.fetchone()
    cur.close()
    if info != None:
        return True
    return False


def correoExiste(correo):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT * FROM usuarios WHERE correo=?"
    cur.execute(sql, [correo])
    conexion.commit()
    info = cur.fetchone()
    cur.close()
    if info != None:
        return True
    return False


def eliminarRegistro(idHabitacion):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "DELETE FROM habitaciones WHERE id_habitacion=?"
    cur.execute(sql, [idHabitacion])
    conexion.commit()
    cur.close()


def editarRegistro(idHabitacion, tipoHab, tipoCama, tipoSabana, numeroCamas, servicios):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "UPDATE habitaciones SET tipo_habitacion=?, tipo_Cama=?, sabanas=?, numero_camas=?, servicios=? WHERE id_habitacion=?"
    cur.execute(sql, [tipoHab, tipoCama, tipoSabana,
                numeroCamas, servicios, idHabitacion])
    conexion.commit()
    cur.close()


def buscarCredencialesUsuario(correo):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT id_usuario, correo, contra FROM usuarios WHERE correo=?"
    cur.execute(sql, [correo])
    conexion.commit()
    infoUser = cur.fetchone()
    cur.close()
    return infoUser


def buscarCredencialesAdmin(correo):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT id_administrador, correo, contra FROM administrador WHERE correo=?"
    cur.execute(sql, [correo])
    conexion.commit()
    infoAdmin = cur.fetchone()
    cur.close()
    return infoAdmin


def buscarCredencialesSuperAdmin(correo):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT id_superadministrador, correo, contra FROM superadministrador WHERE correo=?"
    cur.execute(sql, [correo])
    conexion.commit()
    infoSuperAdmin = cur.fetchone()
    cur.close()
    return infoSuperAdmin


def listaDeHabitaciones():
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql1 = "SELECT * FROM habitaciones"
    cur.execute(sql1)
    conexion.commit()
    infoHabitaciones = cur.fetchall()
    cur.close()
    return infoHabitaciones


def numeroDeRegistro():
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql2 = "SELECT count(*) FROM habitaciones"
    cur.execute(sql2)
    conexion.commit()
    filas = cur.fetchone()
    cur.close()
    return filas


def obetenerIdHabitaciones():
    idHabitaciones = []
    for i in Habitaciones:
        idHabitaciones.append(i[0])
    return idHabitaciones


@app.teardown_appcontext
def cerrarConexion(exception):
    db = getattr(g, '_database_USUARIO', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    metodo = request.method
    if metodo == "POST":
        cedula = request.form.get('Cedula')
        _nombre = request.form.get('Nombre')
        _apellido = request.form.get('Apellido')
        _correo = request.form.get('Correo')
        _contra = generate_password_hash(request.form.get('Contra'))
        usuarioBD = usuarioExiste(cedula)
        correoBD = correoExiste(_correo)
        if usuarioBD and correoBD:
            return "El Usuario Existe y el correo ya se encuentra registrado"
        elif usuarioBD:
            return "ya hay un usuario con ese numer de cedula"
        elif correoBD:
            return "el correo ya se encuentra registrado"
        else:
            # realiza la conexion eh ingresa la informacion si todo esta correcto
            conexion = conexionBaseDeDatos()
            cur = conexion.cursor()
            sql = "INSERT OR IGNORE INTO usuarios (cedula, nombre, apellido, correo, contra) VALUES (?, ?, ?, ?, ?)"
            cur.execute(sql, [cedula, _nombre, _apellido, _correo, _contra])
            conexion.commit()
            cur.close()
            return redirect(url_for('login'))

    elif metodo == "GET":
        return render_template('registro.html')


@app.route('/hacerlogin', methods=['POST'])
def hacerlogin():
    global claveAdmin, Habitaciones, idHab, claveSuper, claveUsuario, valida
    try:
        metodo = request.method
        if metodo == 'POST':
            us = request.form['usuario']
            co = request.form['contra']
            pos = us.find("@")
            valida = us[pos:len(us)]
            if valida == "@cuc.com":
                creden = buscarCredencialesUsuario(us)
                if creden is None:
                    return "error en la contrasena o usuario"
                else:
                    if check_password_hash(creden[2], co):
                        session.clear()
                        session['usuario'] = us
                        claveUsuario = creden[0]
                        Habitaciones = listaDeHabitaciones()
                        idHab = obetenerIdHabitaciones()
                        return redirect(url_for('DashboardUsuariofinal'))
            elif valida == "@admin.com":
                creden = buscarCredencialesAdmin(us)
                if creden is None:
                    return "error en la contrasena o usuario"
                else:
                    if check_password_hash(creden[2], co):
                        session.clear()
                        session['admin'] = us
                        claveAdmin = creden[0]
                        Habitaciones = listaDeHabitaciones()
                        idHab = obetenerIdHabitaciones()
                        return redirect(url_for('dashboardAdministrador'))
            elif valida == "@superadmin.com":
                creden = buscarCredencialesSuperAdmin(us)
                print(creden)
                if creden is None:
                    return "error en la contrasena o usuario"
                else:
                    if check_password_hash(creden[2], co):
                        session.clear()
                        session['super'] = us
                        claveSuper = creden[0]
                        Habitaciones = listaDeHabitaciones()
                        idHab = obetenerIdHabitaciones()
                        return redirect(url_for('dashboardSuperAdministrador'))
            else:
                return "El correo no es valido para iniciar sersion"
        else:
            return "bad request"

    except Exception as error:
        print("Error de exception: ", error)
        return redirect(url_for('index'))
    return "no ejecuto ninguna codicion anterior"

# ----------- ADMINISTRADOR --------------


@app.route('/dashboardAdministrador')
def dashboardAdministrador():
    if 'admin' in session:
        return render_template('DashboardAdministrador.html')
    else:
        return "No tienes los permisos para entrar al Administrador, inicia session con tu cuenta"


@app.route('/dashboardAdministrador/registroUsuariosAdmin')
def registroUsuariosAdmin():
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT id_usuario, cedula, nombre, apellido, correo FROM usuarios"
    cur.execute(sql)
    conexion.commit()
    infoUsuarios = cur.fetchall()
    cur.close()
    print(infoUsuarios)
    return render_template("registroUsuariosAdmin.html", infoUsuarios=infoUsuarios)


@app.route('/dashboardAdministrador/crearHabitacion', methods=['GET', 'POST'])
def crearHabitacionAdmin():
    metodo = request.method
    print(metodo)
    if metodo == 'POST':
        habitacion = request.form.get('habitacion')
        tipoHabitacion = request.form.get('tipoHabitacion')
        sabanas = request.form.get('sabanas')
        numeroCamas = request.form.get('numeroCamas')
        servicios = request.form.get('servicios')
        conexion = conexionBaseDeDatos()
        cur = conexion.cursor()
        sql = "INSERT INTO habitaciones (id_administrador, tipo_habitacion, tipo_cama, sabanas, numero_camas, servicios) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(
            sql, [claveAdmin, habitacion, tipoHabitacion, sabanas, numeroCamas, servicios])
        conexion.commit()
        cur.close()
        return redirect(url_for('crearHabitacionAdmin'))
    else:
        return render_template('CrearHabitacionAdmin.html')


@app.route('/dashboardAdministrador/editareliminar', methods=['GET', 'POST'])
def EditarEliminarAdmin():
    global Habitaciones, idHab
    seccionEditar = False
    metodo = request.method
    valorSelect = request.form.get('_idHabi')
    if metodo == "POST":
        if request.form.get('btn') == "Ir a editar":
            seccionEditar = True
        elif request.form.get('btn') == "Eliminar":
            eliminarRegistro(valorSelect)
            Habitaciones = listaDeHabitaciones()
            idHab = obetenerIdHabitaciones()
        elif request.form.get('btn') == "editar":
            editarHabitacion = request.form.get('habitacion')
            editarTipoHabitacion = request.form.get('tipoHabitacion')
            editarSabanas = request.form.get('sabanas')
            editarNumeroCamas = request.form.get('numeroCamas')
            editarServicios = request.form.get('servicios')
            editarRegistro(valorSelect, editarHabitacion, editarTipoHabitacion,
                           editarSabanas, editarNumeroCamas, editarServicios)
            Habitaciones = listaDeHabitaciones()
            idHab = obetenerIdHabitaciones()
        else:
            print("NO ENTRO A NINGUN BLOQUE")
        return render_template('EditarEliminarAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)
    if metodo == "GET":
        return render_template('EditarEliminarAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)
    return render_template('EditarEliminarAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)


# ----------- USUARIO FINAL --------------


@app.route('/DashboardUsuariofinal')
def DashboardUsuariofinal():
    if 'usuario' in session:
        return render_template('DashboardUsuariofinal.html')
    else:
        return "No tienes los permisos para entrar al UsuarioFinal, inicia session con tu cuenta"


@app.route('/DashboardUsuariofinal/buscarHabitacion', methods=['GET', 'POST'])
def buscarHabitacion():
    global idParaReservas
    if request.method == 'POST':
        idParaReservas = request.form.get('idHabiBuscar')
        return redirect(url_for('reserva'))
    return render_template('BuscarHabitacion.html', datos=Habitaciones, idHab=idHab, filas=numeroDeRegistro(), soy=valida)


@app.route('/DashboardUsuariofinal/buscarHabitacion/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('email')
        telefono = request.form.get('telefono')
        llegada = request.form.get('llegada')
        salida = request.form.get('salida')
        permanencia = request.form.get('permanencia')
        personas = request.form.get('personas')
        conexion = conexionBaseDeDatos()
        cur = conexion.cursor()
        sql = "INSERT OR IGNORE INTO reservas (id_usuario, id_habitacion, nombre, apellido, correo, telefono, horaLlegada, horaSalida, dias, personas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sql, [claveUsuario, idParaReservas, nombre, apellido,
                    correo, telefono, llegada, salida, permanencia, personas])
        conexion.commit()
        cur.close()
        return render_template('reserva.html')

    return render_template('reserva.html')


@app.route('/DashboardUsuariofinal/buscarReserva')
def buscarReserva():
    tieneReserva = None
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT * FROM reservas WHERE id_usuario=?"
    cur.execute(sql, [claveUsuario])
    conexion.commit()
    infoReserva = cur.fetchone()
    cur.close()

    if infoReserva != None:
        tieneReserva = True
    print(infoReserva)
    return render_template('BuscarReservaUsuariofinal.html', tieneReserva=tieneReserva, infoReserva=infoReserva)


@app.route('/DashboardUsuariofinal/comentario')
def comentario():
    return render_template('comentarios.html')

# ----------- SUPER ADMINISTRADOR --------------


@app.route('/dashboardSuperAdministrador')
def dashboardSuperAdministrador():
    if 'super' in session:
        return render_template('dashboardSuperAdministrador.html')
    else:
        return "No tienes los permisos para entrar al SuperAdmin, inicia session con tu cuenta"


@app.route('/dashboardSuperAdministrador/registroUsuariosSuper')
def registroUsuariosSuper():
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT id_usuario, cedula, nombre, apellido, correo FROM usuarios"
    cur.execute(sql)
    conexion.commit()
    infoUsuarios = cur.fetchall()
    cur.close()
    print(infoUsuarios)
    return render_template("registroUsuariosSuper.html", infoUsuarios=infoUsuarios)


@app.route('/dashboardSuperAdministrador/crearHabitacion', methods=['GET', 'POST'])
def crearHabitacionSuper():
    metodo = request.method
    print(metodo)
    if metodo == 'POST':
        habitacion = request.form.get('habitacion')
        tipoHabitacion = request.form.get('tipoHabitacion')
        sabanas = request.form.get('sabanas')
        numeroCamas = request.form.get('numeroCamas')
        servicios = request.form.get('servicios')
        print(habitacion, tipoHabitacion, sabanas, numeroCamas, servicios)
        print(claveSuper)
        conexion = conexionBaseDeDatos()
        cur = conexion.cursor()
        sql = "INSERT INTO habitaciones (id_administrador, tipo_habitacion, tipo_cama, sabanas, numero_camas, servicios) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(
            sql, [claveSuper, habitacion, tipoHabitacion, sabanas, numeroCamas, servicios])
        conexion.commit()
        cur.close()
        return redirect(url_for('crearHabitacionSuper'))
    else:
        return render_template('CrearHabitacionSuperAdmin.html')


@app.route('/dashboardSuperAdministrador/editareliminar', methods=['GET', 'POST'])
def EditarEliminarSuper():
    global Habitaciones, idHab
    seccionEditar = False
    metodo = request.method
    valorSelect = request.form.get('_idHabi')
    print(metodo)
    print(valorSelect)
    if metodo == "POST":
        if request.form.get('btn') == "Ir a editar":
            seccionEditar = True
        elif request.form.get('btn') == "Eliminar":
            eliminarRegistro(valorSelect)
            Habitaciones = listaDeHabitaciones()
            idHab = obetenerIdHabitaciones()
        elif request.form.get('btn') == "editar":
            # solo ingresa aqui cuando se haga una nueva peticion post y no se presionen ninguno de los botones anteriores
            # cuando se habra esta seccion los botones ir a editar y eliminar deben bloquearse
            editarHabitacion = request.form.get('habitacion')
            editarTipoHabitacion = request.form.get('tipoHabitacion')
            editarSabanas = request.form.get('sabanas')
            editarNumeroCamas = request.form.get('numeroCamas')
            editarServicios = request.form.get('servicios')
            editarRegistro(valorSelect, editarHabitacion, editarTipoHabitacion,
                           editarSabanas, editarNumeroCamas, editarServicios)
            Habitaciones = listaDeHabitaciones()
            idHab = obetenerIdHabitaciones()
        else:
            print("NO ENTRO A NINGUN BLOQUE")
        return render_template('EditarEliminarSuperAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)
    if metodo == "GET":
        return render_template('EditarEliminarSuperAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)
    return render_template('EditarEliminarSuperAdmin.html', datos=Habitaciones, idHab=idHab, editar=seccionEditar)


@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))


def main():
    if __name__ == "__main__":
        app.run(debug=True, port=4000)


main()
