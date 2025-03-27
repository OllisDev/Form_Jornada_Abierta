from model.user import User
from repository.connection_db import ConnectionDB

class UserRepository:

    def __init__(self):
        self.db = ConnectionDB()

    def create_user(self, user: User, quota_id: int):
        conn = self.db.connect_db()
        if not conn:
            return {"error": "No se pudo conectar con la base de datos"}
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, quota_id) VALUES (%s, %s, %s)",
                           (user.name, user.email, quota_id))
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
            cursor.execute("SELECT id, name, email FROM users")
            users_data = cursor.fetchall()
            users = [User(id=row[0], name=row[1], email=row[2]) for row in users_data]
            return users
        finally:
            conn.close()

 
    def user_exists(self, id, email):
         # La consulta se ejecuta a través del cursor, no de la conexión directamente
        conn = self.db.connect_db()
        if not conn:
            return False  # Si no se puede conectar a la base de datos, retornamos False
        
        try:
            cursor = conn.cursor()  # Usamos cursor para ejecutar la consulta
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s OR email = %s", (id, email))
            result = cursor.fetchone()  # Usamos fetchone() para obtener una fila
            return result[0] > 0  # Verificamos si existe un registro
        except Exception as e:
            return False  # En caso de error, retornamos False
        finally:
            conn.close()