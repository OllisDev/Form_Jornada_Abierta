from repository.user_Repository import UserRepository
from repository.quota_repository import QuotaRepository
from model.user import User


class UserController:
    def register_user(self, user: User):
        remaining = QuotaRepository.get_remaining_slots()

        if remaining <= 0:
            return {"error": "No hay mas slots disponibles"}
        
        success = UserRepository.create_user(user)

        if success:
            QuotaRepository.decrement_slot(self)
            return {"message": "Usuario registrado correctamente", "remaining": remaining - 1}
        else:
            return {"error": "Identificador ya existe"}