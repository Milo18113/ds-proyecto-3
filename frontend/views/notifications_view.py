import streamlit as st
import pandas as pd
from api_client import ApiClient


def render_notifications():
    st.subheader("Notificaciones")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)

    try:
        response = client.get_notifications()

        if response.status_code != 200:
            st.error(f"No se pudieron cargar las notificaciones: {response.text}")
            return

        notifications = response.json()

        if not notifications:
            st.info("No hay notificaciones registradas.")
            return

        df = pd.DataFrame(notifications)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error al consultar notificaciones: {e}")