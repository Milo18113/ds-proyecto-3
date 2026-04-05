import streamlit as st
import pandas as pd
from api_client import ApiClient


def render_incidents():
    st.subheader("Lista de incidentes")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)

    try:
        response = client.get_incidents()

        if response.status_code != 200:
            st.error(f"No se pudieron cargar los incidentes: {response.text}")
            return

        incidents = response.json()

        if not incidents:
            st.info("No hay incidentes registrados.")
            return

        df = pd.DataFrame(incidents)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error al consultar incidentes: {e}")