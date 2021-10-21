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


def buscarCredencialesUsuario(correo):
    conexion = conexionBaseDeDatos()
    cur = conexion.cursor()
    sql = "SELECT correo, contra FROM usuarios WHERE correo=?"
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
    sql = "SELECT correo, contra FROM superadministrador WHERE correo=?"
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
    # metodo = request.method
    # msgUser = request.args.get('msgUser')
    # msgPass = request.args.get('msgPass')
    # stdUser = request.args.get('stdUser')
    # stdPass = request.args.get('stdPass')
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():

    metodo = request.method
    print(metodo)
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
            return render_template('registro.html')

    elif metodo == "GET":
        return render_template('registro.html')


@app.route('/hacerlogin', methods=['POST'])
def hacerlogin():
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
                    if check_password_hash(creden[1], co):
                        session.clear()
                        session['usuario'] = us
                        return redirect(url_for('DashboardUsuariofinal'))
            elif valida == "@admin.com":
                creden = buscarCredencialesAdmin(us)
                if creden is None:
                    return "error en la contrasena o usuario"
                else:
                    if check_password_hash(creden[2], co):
                        session.clear()
                        session['admin'] = us
                        session['id'] = creden[0]
                        return redirect(url_for('dashboardAdministrador'))
            elif valida == "@superadmin.com":
                creden = buscarCredencialesSuperAdmin(us)
                if creden is None:
                    return "error en la contrasena o usuario"
                else:
                    if check_password_hash(creden[1], co):
                        session.clear()
                        session['super'] = us
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
        print(habitacion, tipoHabitacion, sabanas, numeroCamas, servicios)
        # idAdmin = session['id']
        # print(idAdmin)
        conexion = conexionBaseDeDatos()
        cur = conexion.cursor()
        sql = "INSERT INTO habitaciones (id_administrador, tipo_habitacion, tipo_cama, sabanas, numero_camas, servicios) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(
            sql, [1, habitacion, tipoHabitacion, sabanas, numeroCamas, servicios])
        conexion.commit()
        cur.close()

        return redirect(url_for('crearHabitacionAdmin'))
    else:
        return render_template('CrearHabitacionAdmin.html')


@app.route('/dashboardAdministrador/editareliminar', methods=['GET', 'POST'])
def EditarEliminarAdmin():
    metodo = request.method
    if metodo == "POST":
        pass
    if metodo == "GET":
        datos = listaDeHabitaciones()
        return render_template('EditarEliminarAdmin.html', datos=datos, filas=numeroDeRegistro())


# ----------- USUARIO FINAL --------------

@app.route('/DashboardUsuariofinal')
def DashboardUsuariofinal():
    if 'usuario' in session:
        return render_template('DashboardUsuariofinal.html')
    else:
        return "No tienes los permisos para entrar al UsuarioFinal, inicia session con tu cuenta"


@app.route('/DashboardUsuariofinal/buscarHabitacion')
def buscarHabitacion():
    datos = listaDeHabitaciones()
    return render_template('BuscarHabitacion.html', datos=datos, filas=numeroDeRegistro())


@app.route('/DashboardUsuariofinal/reserva', methods=['GET', 'POST'])
def reserva():
    return render_template('reserva.html')


@app.route('/DashboardUsuariofinal/buscarReserva')
def buscarReserva():
    return render_template('BuscarReservaUsuariofinal.html')


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


@app.route('/dashboardSuperAdministrador/crearHabitacion')
def crearHabitacionSuper():
    return render_template('CrearHabitacionSuperAdmin.html')


@app.route('/dashboardSuperAdministrador/editareliminar')
def EditarEliminarSuper():
    return render_template('EditarEliminarSuperAdmin.html')


@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))


def main():
    if __name__ == "__main__":
        app.run(debug=True, port=4000)


main()
