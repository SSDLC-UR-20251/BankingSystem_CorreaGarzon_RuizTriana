from _datetime import datetime
import re

import unicodedata


def normalize_input(data):
    return data


# valido el email
def validate_email(email):
    email = normalize_input(email)
    patron = r'^[A-Za-z0-9._%+-]+@urosario\.edu\.co$'
    return bool(re.fullmatch(patron, email))


# valido la edad
def validate_dob(dob):
    try:
        fecha = datetime.strptime(dob, "%Y-%m-%d")
        edad_minima = 16
        fecha_limite = datetime.now().replace(year=datetime.now().year - edad_minima)
        return fecha <= fecha_limite
    except ValueError:
        return False


# valido el usuario
def validate_user(user):
    patron = r'^[A-Za-z]+(?:\.[A-Za-z]+)*$'
    return bool(re.fullmatch(patron, user))


# valido el dni
def validate_dni(dni):
    patron = r'^1\d{9}$' 
    return bool(re.fullmatch(patron, dni))


# valido la contraseña
def validate_pswd(pswd):
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#*@\$%&\-!+=?])[A-Za-z\d#*@\$%&\-!+=?]{8,35}$'
    return bool(re.fullmatch(patron, pswd))



def validate_name(name):
    return True
