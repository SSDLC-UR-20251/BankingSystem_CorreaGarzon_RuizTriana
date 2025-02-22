from _datetime import datetime
import time
from app.validation import *
from app.reading import *
from flask import request, jsonify, redirect, url_for, render_template, session, make_response
from app import app

app.secret_key = 'your_secret_key'

MAX_ATTEMPTS = 3  # Máximo de intentos permitidos
LOCK_TIME = 5 * 60  # Tiempo de bloqueo en segundos (5 minutos)
failed_attempts = {}  # Diccionario para almacenar intentos fallidos


@app.route('/api/users', methods=['POST'])
def create_record():
    data = request.form
    email = data.get('email')
    username = data.get('username')
    nombre = data.get('nombre')
    apellido = data.get('Apellidos')
    password = data.get('password')
    dni = data.get('dni')
    dob = data.get('dob')
    errores = []
    print(data)
    # Validaciones
    if not validate_email(email):
        errores.append("Email inválido")
    if not validate_pswd(password):
        errores.append("Contraseña inválida")
    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida")
    if not validate_dni(dni):
        errores.append("DNI inválido")
    if not validate_user(username):
        errores.append("Usuario inválido")
    if not validate_name(nombre):
        errores.append("Nombre inválido")
    if not validate_name(apellido):
        errores.append("Apellido inválido")

    if errores:
        return render_template('form.html', error=errores)

    email = normalize_input(email)
    db = read_db("db.txt")
    db[email] = {
        'nombre': normalize_input(nombre),
        'apellido': normalize_input(apellido),
        'username': normalize_input(username),
        'password': normalize_input(password),
        "dni": dni,
        'dob': normalize_input(dob),
        "role": "admin"
    }

    write_db("db.txt", db)
    return redirect("/login")


# Endpoint para el login
@app.route('/api/login', methods=['POST'])
def api_login():
    email = normalize_input(request.form['email'])
    password = normalize_input(request.form['password'])

    if email in failed_attempts:
        user_data = failed_attempts[email]
        if user_data["intentos"] >= MAX_ATTEMPTS:
            # Verificar si el tiempo de bloqueo ha pasado
            if time.time() - user_data["tiempoBloqueo"] < LOCK_TIME:
                remaining_time = LOCK_TIME - (time.time() - user_data["tiempoBloqueo"])
                error = f"Cuenta bloqueada. Intenta nuevamente en {int(remaining_time / 60)} minutos."
                return render_template('login.html', error=error)
            else:
                # Resetear el contador de intentos después del bloqueo
                failed_attempts[email] = {"intentos": 0, "tiempoBloqueo": 0}

    db = read_db("db.txt")
    if email not in db:
        error = "Credenciales inválidas"
        return render_template('login.html', error=error)

    password_db = db.get(email)["password"]

    if password_db == password :
        failed_attempts[email] = {"intentos": 0, "tiempoBloqueo": 0}
        session['role'] = "admin"
        return redirect(url_for('customer_menu'))
    else:
        if email in failed_attempts:
            failed_attempts[email]["intentos"] += 1
        else:
            failed_attempts[email] = {"intentos": 1, "tiempoBloqueo": 0}

        if failed_attempts[email]["intentos"] >= MAX_ATTEMPTS:
            failed_attempts[email]["tiempoBloqueo"] = time.time()
            error = "Demasiados intentos fallidos. La cuenta está bloqueada temporalmente."
        else:
            error = "Credenciales inválidas"

        return render_template('login.html', error=error)


# Página principal del menú del cliente
@app.route('/customer_menu')
def customer_menu():

    db = read_db("db.txt")

    transactions = read_db("transaction.txt")
    current_balance = 100
    last_transactions = []
    message = request.args.get('message', '')
    error = request.args.get('error', 'false').lower() == 'true'
    return render_template('customer_menu.html',
                           message=message,
                           nombre="",
                           balance=current_balance,
                           last_transactions=last_transactions,
                           error=error,)


# Endpoint para leer un registro
@app.route('/records', methods=['GET'])
def read_record():
    db = read_db("db.txt")
    role = session.get('role')
    if role == 'admin':
        message = request.args.get('message', '')
        return render_template('records.html', users=db,role=role, message=message)
    else:
        user_data = db.get(session.get('email'))
        return render_template('user.html', users={session.get('email'): user_data}, role=role)
    


@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    # Leer la base de datos de usuarios
    db = read_db("db.txt")

    username = request.form['username']
    dni = request.form['dni']
    dob = request.form['dob']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    errores = []

    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida")
    if not validate_dni(dni):
        errores.append("DNI inválido")
    if not validate_user(username):
        errores.append("Usuario inválido")
    if not validate_name(nombre):
        errores.append("Nombre inválido")
    if not validate_name(apellido):
        errores.append("Apellido inválido")

    if errores:
        return render_template('edit_user.html',
                               user_data=db[email],
                               email=email,
                               error=errores)


    db[email]['username'] = normalize_input(username)
    db[email]['nombre'] = normalize_input(nombre)
    db[email]['apellido'] = normalize_input(apellido)
    db[email]['dni'] = dni
    db[email]['dob'] = normalize_input(dob)


    write_db("db.txt", db)
    

    # Redirigir al usuario a la página de records con un mensaje de éxito
    return redirect(url_for('read_record', message="Información actualizada correctamente"))


@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    role = session.get('role')
    if role != 'admin':
        return redirect(url_for('read_record', error=True))

    db = read_db("db.txt")
    
    if email in db:
        del db[email]
        write_db("db.txt", db)
        return redirect(url_for('read_record', message="Usuario eliminado correctamente"))
    else:
        return redirect(url_for('read_record', error=True))
