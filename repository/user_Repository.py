from model.user import User
from repository.connection_db import ConnectionDB

class UserRepository:

    def __init__(self):
        self.db = ConnectionDB()

    def create_user(self, user: User):
        conn = self.db.connect_db()
        if not conn:
            return {"error": "No se pudo conectar con la base de datos"}
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (identifier, name, email) VALUES (%s, %s, %s)",
                           (user.identifier, user.name, user.email))
            conn.commit()
            return {"message": "Usuario registrado correctamente"}
        except Exception as e:
            return {"error": f"Error al insertar usuario: {e}"}
        finally:
            conn.close()

    def get_all_users(self):
        conn = self.db.connect_db()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, identifier, name, email FROM users")
            users_data = cursor.fetchall()
            users = [User(id=row[0], identifier=row[1], name=row[2], email=row[3]) for row in users_data]
            return users
        finally:
            conn.close()