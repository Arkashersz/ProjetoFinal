import secrets
import string

# Tamanho da chave secreta (aumente para aumentar a segurança)
key_length = 32

# Caracteres possíveis para a chave secreta
charset = string.ascii_letters + string.digits + string.punctuation

# Gere a chave secreta
secret_key = ''.join(secrets.choice(charset) for _ in range(key_length))

print("Sua chave secreta gerada:", secret_key)