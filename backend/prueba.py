from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
nueva_password = "prueba"  # Cambiar por una contraseña segura
hashed_password = bcrypt.generate_password_hash(nueva_password).decode('utf-8')

print(hashed_password)
