import streamlit as st
from controller.user_controller import UserController
from repository.quota_repository import QuotaRepository
from repository.user_Repository import UserRepository

def main():
    st.set_page_config(page_title="Registro de usuarios para la jornada abierta", page_icon="resources/valle_del_miro.ico")
    st.title("Registro de usuarios para la jornada abierta 📋")

    quota_repo = QuotaRepository()

    remaining = quota_repo.get_remaining_slots()
    st.metric("Cupos disponibles: ", remaining)

    user_repo = UserRepository()

    st.subheader("Usuarios registrados")
    users = user_repo.get_all_users()
    st.table([{"ID": user.get_id(), "Identificador": user.get_identifier(), "Nombre": user.get_name(), "Correo": user.get_email()} for user in users])

    st.write("Formulario de registro...")

    st.subheader("Registro manual")
    with st.form("register_form"):
        identifier = st.text_input("Identificador")
        name = st.text_input("Nombre")
        email = st.text_input("Correo electrónico")
        submit = st.form_submit_button("Registrar Usuario")

        if submit:
            result = UserController.register_user(identifier, name, email)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])


