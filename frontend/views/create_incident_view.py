import streamlit as st
from api_client import ApiClient


def render_create_incident():
    st.subheader("Crear incidente")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)

    with st.form("create_incident_form"):
        title = st.text_input("Título")
        description = st.text_area("Descripción")
        severity = st.selectbox("Severidad", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        submitted = st.form_submit_button("Crear incidente")

    if submitted:
        if not title.strip() or not description.strip():
            st.warning("Título y descripción son obligatorios.")
            return

        payload = {
            "title": title,
            "description": description,
            "severity": severity,
        }

        try:
            response = client.create_incident(payload)

            if response.status_code == 201:
                st.success("Incidente creado correctamente.")
                st.session_state.current_view = "Incidentes"
                st.rerun()
            else:
                st.error(f"No se pudo crear el incidente: {response.text}")

        except Exception as e:
            st.error(f"Error conectando con la API: {e}")