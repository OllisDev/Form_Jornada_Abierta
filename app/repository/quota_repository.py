from model.quota import Quota
from repository.connection_db import ConnectionDB

class QuotaRepository():

    def __init__(self):
        self.db = ConnectionDB()

    def get_remaining_slots(self):
        conn = self.db.connect_db()
        if not conn:
            return "Error de conexión a la base de datos"
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT remaining FROM quota WHERE id=1")
            remaining = cursor.fetchone()[0]
            return remaining
        except Exception as e:
            return f"Error al realizar la consulta: {e}"
        finally:
            conn.close()

    def decrement_slot(self, quota: Quota):
        conn = self.db.connect_db()
        if not conn:
            return {"error": "No se pudo conectar con la base de datos"}
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE quota SET remaining = remaining -1 WHERE id=1",
                           (quota.remaining))
            conn.commit()
            return{"message": "Se ha actualizado el campo correctamente"}
        except Exception as e:
            return {"error": f"Error al actualizar el campo en la base de datos: {e}"}
        finally:
            conn.close()