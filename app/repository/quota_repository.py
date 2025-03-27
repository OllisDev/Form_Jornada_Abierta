from model.quota import Quota
from repository.connection_db import ConnectionDB

class QuotaRepository():

    def __init__(self):
        self.db = ConnectionDB()

    def get_remaining_slots(self):
        conn = self.db.connect_db()
        if not conn:
            return -1
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT remaining FROM quota WHERE id=1")
            remaining = cursor.fetchone()

            if remaining is None:
                return 0
            
            return int(remaining[0])
        
        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            return -1
        finally:
            conn.close()

    def decrement_slot(self):
        conn = self.db.connect_db()
        if not conn:
            return {"error": "No se pudo conectar con la base de datos"}
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE quota SET remaining = remaining -1 WHERE id=1")
            conn.commit()

            if cursor.rowcount == 0:
                return {"error": "No se pudo actualizar el campo, ningún registro afectado."}
        
            return {"message": "Se ha actualizado el campo correctamente"}
        except Exception as e:
            return {"error": f"Error al actualizar el campo en la base de datos: {e}"}
        finally:
            conn.close()