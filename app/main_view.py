import streamlit as st
from repository.quota_repository import QuotaRepository

def generate_url_google_forms():
    return "https://docs.google.com/forms/d/e/1FAIpQLScRVk3vVLSt0ZUXLQ9T8NWBW_ABaO7_eFP4GemOZLuJguroBw/viewform?usp=header"

def main():
    st.set_page_config(page_title="Registro de usuarios para la jornada abierta", page_icon="resources/valle_del_miro.ico")
    st.title("Registro de usuarios para la jornada abierta 📋")

    quota_repo = QuotaRepository()

    # Inicializar el estado de los cupos solo si no está definido
    if "remaining_slots" not in st.session_state:
        st.session_state["remaining_slots"] = max(quota_repo.get_remaining_slots(), 0)  # Asegurar que no sea negativo

    # Controlar si el usuario ya gastó su cupo
    if "button_clicked" not in st.session_state:
        st.session_state["button_clicked"] = False

    st.metric("Cupos disponibles", st.session_state["remaining_slots"])

    # Función para manejar la reducción de cupo
    def handle_click():
        if st.session_state["button_clicked"]:
            st.error("No puedes gastar más de un cupo.")
        else:
            result = quota_repo.decrement_slot()
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state["button_clicked"] = True
                st.session_state["remaining_slots"] -= 1  # Restar sin recargar de la BD
                st.success("Redirigiendo al formulario...")
                form_url = generate_url_google_forms()
                st.markdown(f"[Rellenar formulario de Google Forms](<{form_url}>)", unsafe_allow_html=True)

    if st.session_state["remaining_slots"] > 0:
        st.button("Ir al formulario de Google Forms", on_click=handle_click)
    else:
        st.error("No hay cupos disponibles.")