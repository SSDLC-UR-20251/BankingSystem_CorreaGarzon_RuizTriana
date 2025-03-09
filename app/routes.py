from flask import render_template, redirect, url_for,request, session
from app import app
from app.encryption import decrypt_aes, ofuscar_dni, AES_KEY
from app.reading import read_db

# app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/deposit', methods=['GET'])
def deposit():
     if 'email' not in session:
        return redirect(url_for('login'))
     return render_template('deposit.html', darkmode=request.cookies.get('darkmode', 'light'))

@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('form.html')


@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@app.route('/edit_user/<email>', methods=['GET'])
def edit_user(email):
    if 'email' not in session:
        return redirect(url_for('login'))
    db = read_db("db.txt")

    if email not in db:
        return redirect(url_for('records', message="Usuario no encontrado"))

    user_info = db[email]
    dni_descifrado = decrypt_aes(user_info["dni"],user_info["nonce"], AES_KEY)  # Descifrar DNI correctamente
    user_info['dni'] = dni_descifrado

    return render_template('edit_user.html', user_data=user_info, email=email)


# Formulario de retiro
@app.route('/withdraw', methods=['GET'])
def withdraw():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session.get('email')
    print(email)
    transactions = read_db("transaction.txt")
    current_balance = sum(float(t['balance']) for t in transactions.get(email, []))
    return (render_template('withdraw.html', balance=current_balance,darkmode=request.cookies.get('darkmode', 'light')))
