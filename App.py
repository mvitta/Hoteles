from flask import Flask, render_template, redirect, url_for, request
import os
from werkzeug.exceptions import RequestedRangeNotSatisfiable

app = Flask(__name__)
app.secret_key = os.urandom(34)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/hacerlogin', methods=['POST'])
def hacerlogin():
    print(request.method)
    try:
        if request.method == 'POST':
            us = request.form['usuario']
            co = int(request.form['contra'])
            print(us, " - ", co)
            if us == "admin" and co == 1234:
                return redirect(url_for('dashboardAdministrador'))
            elif us == "superadmin" and co == 4321:
                return redirect(url_for('dashboardSuperAdministrador'))
            elif us == "user" and co == 12345678:
                return redirect(url_for('DashboardUsuariofinal'))
            else:
                return redirect(url_for('login'))
    except:
        return redirect(url_for('index'))

# ----------- ADMINISTRADOR --------------


@app.route('/dashboardAdministrador')
def dashboardAdministrador():
    return render_template('DashboardAdministrador.html')


@app.route('/dashboardAdministrador/crearHabitacion')
def crearHabitacionAdmin():
    return render_template('CrearHabitacionAdmin.html')


@app.route('/dashboardAdministrador/editareliminar')
def EditarEliminarAdmin():
    return render_template('EditarEliminarAdmin.html')


# ----------- USUARIO FINAL --------------

@app.route('/DashboardUsuariofinal')
def DashboardUsuariofinal():
    return render_template('DashboardUsuariofinal.html')


@app.route('/DashboardUsuariofinal/buscarHabitacion')
def buscarHabitacion():
    return render_template('BuscarHabitacion.html')


@app.route('/DashboardUsuariofinal/reserva')
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
    return render_template('dashboardSuperAdministrador.html')


@app.route('/dashboardSuperAdministrador/crearHabitacion')
def crearHabitacionSuper():
    return render_template('CrearHabitacionSuperAdmin.html')


@app.route('/dashboardSuperAdministrador/editareliminar')
def EditarEliminarSuper():
    return render_template('EditarEliminarSuperAdmin.html')


def main():
    if __name__ == "__main__":
        app.run(debug=True, port=4000)


main()
