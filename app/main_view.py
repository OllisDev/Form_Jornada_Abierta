import streamlit as st
from controller.user_controller import UserController
from repository.quota_repository import QuotaRepository
from repository.user_Repository import UserRepository
from model.user import User

def generate_url_google_forms(name, email):
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLScRVk3vVLSt0ZUXLQ9T8NWBW_ABaO7_eFP4GemOZLuJguroBw/viewform?usp=header"
    name_id = "entry.123456789"
    email_id = "entry.987654321"

    return f"{base_url}&{name_id}={name.replace(' ', '%20')}&{email_id}={email}"

def main():
    st.set_page_config(page_title="Registro de usuarios para la jornada abierta", page_icon="resources/valle_del_miro.ico")
    st.title("Registro de usuarios para la jornada abierta 📋")

    user_repo = UserRepository()

    query_params = st.query_params


    
    if 'name' in query_params and 'email' in query_params:
        name = query_params['name'][0] if query_params['name'] else None
        email = query_params['email'][0] if query_params['email'] else None
        
        if name and email:
            st.info(f"Registro recibido de Google Forms: {name} ({email})")

            user = User(None, name, email)

            # Verificar si el usuario ya existe
            if user_repo.user_exists(user.id, user.email):  # Pasamos el ID y el email
                st.error("El usuario ya existe.")
            else:
                result = UserController().register_user(user)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    st.metric("Cupos disponibles: ", result["remaining"])
                    
    st.subheader("Registro a través de Google Forms")
    name_gf = st.text_input("Nombre (para Google Forms)")
    email_gf = st.text_input("Correo electrónico (para Google Forms)")

    if st.button("Ir al Formulario de Google Forms"):
        if name_gf and email_gf:
            user = User(None, name_gf, email_gf)

            if user_repo.user_exists(user.id, user.email):
                st.error("El usuario ya existe.")
            else:
                result = UserController().register_user(user)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    st.metric("Cupos disponibles: ", result["remaining"])
                    
                    # Generar URL y mostrar enlace
                    form_url = generate_url_google_forms(name_gf, email_gf)
                    st.markdown(f"[Rellenar Formulario de Google Forms](<{form_url}>)", unsafe_allow_html=True)
        else:
            st.warning("Por favor ingrese un nombre y un correo electrónico.")

