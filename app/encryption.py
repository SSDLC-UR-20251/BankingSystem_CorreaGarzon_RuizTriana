from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def hash_with_salt(texto):
    texto_bytes = texto.encode()
    salt = get_random_bytes(16)
    texto_salt = texto_bytes + salt
    hash = SHA256.new(texto_salt)
    return hash.hexdigest(), salt.hex()


def compare_hashes(texto, stored_hash, salt):
    texto_bytes = texto.encode()
    salt = bytes.fromhex(salt)
    texto_salt = texto_bytes + salt
    computed_hash = SHA256.new(texto_salt).hexdigest()  # Usar otro nombre para el hash calculado
    return computed_hash == stored_hash  # Comparar con el hash almacenado



def decrypt_aes(texto_cifrado_str, nonce_str, clave):
    texto_cifrado_bytes = bytes.fromhex(texto_cifrado_str)
    nonce_bytes = bytes.fromhex(nonce_str)
    cipher = AES.new(clave, AES.MODE_EAX, nonce=nonce_bytes)
    texto_bytes = cipher.decrypt(texto_cifrado_bytes)
    texto = texto_bytes.decode()
    return texto


def encrypt_aes(texto, clave):
    # Convertir el texto a bytes
    texto_bytes = texto.encode()


    # Crear un objeto AES con la clave proporcionada
    cipher = AES.new(clave, AES.MODE_EAX)

    # Cifrar el texto
    nonce = cipher.nonce
    texto_cifrado, tag = cipher.encrypt_and_digest(texto_bytes)

    # Convertir el texto cifrado en bytes a una cadena de texto
    texto_cifrado_str = texto_cifrado.hex()

    # Devolver el texto cifrado y el nonce
    return texto_cifrado_str, nonce.hex()
