from _datetime import datetime
import time
from app.validation import *
from app.reading import *
from flask import request, jsonify, redirect, url_for, render_template, session, make_response
from app import app


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
    }

    write_db("db.txt", db)
    return redirect("/login")



# Endpoint para el login
@app.route('/api/login', methods=['POST'])
def api_login():
    email = normalize_input(request.form['email'])
    password = normalize_input(request.form['password'])

    db = read_db("db.txt")
    if email not in db:
        error = "Credenciales inválidas"
        return render_template('login.html', error=error)

    password_db = db.get(email)["password"]

    if password_db == password :
        return redirect(url_for('customer_menu'))
    else:
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
    return render_template('records.html', users=db)



# VULNERABILIDAD: Uso incorrecto de \b dentro de clase de caracteres
import re
matcher = re.compile(r"\b[\t\b]")

def match_data(data):
    return bool(matcher.match(data))


# VULNERABILIDAD: NoSQL Injection
from flask_pymongo import PyMongo
import json

mongo = PyMongo(app)

@app.route("/insecure_query")
def home_page():
    unsanitized_search = request.args['search']
    json_search = json.loads(unsanitized_search)
    result = mongo.db.user.find({'name': json_search})
    return str(result)

# --- Vulnerabilidad 3: Conflicting attributes in base classes ---
import threading

class TCPServer(object):
    
    def process_request(self, request, client_address):
        self.do_work(request, client_address)
        self.shutdown_request(request)

    def do_work(self, request, client_address):
        print("Doing work in TCPServer")

    def shutdown_request(self, request):
        print("Shutting down request")


class ThreadingMixIn:
    """Mix-in class to handle each request in a new thread."""

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        t = threading.Thread(target=self.do_work, args=(request, client_address))
        t.daemon = self.daemon_threads
        t.start()

    @property
    def daemon_threads(self):
        return True


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass


# Ejecución simulada para asegurar que se tome en cuenta en el análisis
def run_conflicting_example():
    server = ThreadingTCPServer()
    server.process_request("sample_request", "127.0.0.1")
