from repository.user_Repository import UserRepository
from repository.quota_repository import QuotaRepository
from model.user import User

class UserController:
    def register_user(self, user: User):
        quota_repo = QuotaRepository()
        remaining = quota_repo.get_remaining_slots()

        if remaining <= 0:
            return {"error": "No hay mas slots disponibles"}
        
        user_repo = UserRepository()
        if user_repo.user_exists(user.id, user.email):
            return {"error", "El usuario ya existe."}
        
        quota_id = 1
        success = user_repo.create_user(user, quota_id)

        if success:
            quota_repo.decrement_slot()

            updated_remaining = quota_repo.get_remaining_slots()
            return {"message": "Usuario registrado correctamente", "remaining": updated_remaining}
        else:
            return {"error": "Identificador ya existe"} 