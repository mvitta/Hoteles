from flask import Flask, render_template, redirect, url_for, session, request
from flask import g
import os
from validaciones import isUsernameValid, isPasswordValid
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(34)
DATABASE = "registroUsuarios.db"


def conexionBaseDeDatos():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def cerrarConexion(exception):
    db = getattr(g, '_database', None)
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
        print(request.method)
        cedula = request.form.get('Cedula')
        _nombre = request.form.get('Nombre')
        _apellido = request.form.get('Apellido')
        _correo = request.form.get('Correo')
        _contra = generate_password_hash(request.form.get('Contra'))

        print(cedula, _nombre, _apellido, _correo, _contra)

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
    msgUser = ""
    msgPass = ""
    try:
        metodo = request.method
        print(metodo)
        if metodo == 'POST':
            us = request.form['usuario']
            co = request.form['contra']
            print("DATOS SIN CIFRAR", us, co)

            # estadoUser = True  # isUsernameValid(us)
            # estadoPass = True  # isPasswordValid(co)
            # if not estadoUser:
            #     msgUser = "Error de usuario"
            # if not estadoPass:
            #     msgPass = "La Contraseña debe tener al menos una minuscula, una mayuscula, un numero y 8 caracteres"
            # print(estadoUser, estadoPass)
            session.clear()
            if us == "admin" and co == "1234":

                print("CONTRASEÑA CIFRADA", co)
                session['admin'] = us
                return redirect(url_for('dashboardAdministrador'))
            elif us == "superadmin" and co == "1234":
                session['super'] = us
                return redirect(url_for('dashboardSuperAdministrador'))
            elif us == "user" and co == "1234":
                session['usuario'] = us
                return redirect(url_for('DashboardUsuariofinal'))
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


@app.route('/dashboardAdministrador/crearHabitacion')
def crearHabitacionAdmin():
    return render_template('CrearHabitacionAdmin.html')


@app.route('/dashboardAdministrador/editareliminar')
def EditarEliminarAdmin():
    return render_template('EditarEliminarAdmin.html')


# ----------- USUARIO FINAL --------------

@app.route('/DashboardUsuariofinal')
def DashboardUsuariofinal():
    if 'usuario' in session:
        return render_template('DashboardUsuariofinal.html')
    else:
        return "No tienes los permisos para entrar al UsuarioFinal, inicia session con tu cuenta"


@app.route('/DashboardUsuariofinal/buscarHabitacion')
def buscarHabitacion():
    return render_template('BuscarHabitacion.html')


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
