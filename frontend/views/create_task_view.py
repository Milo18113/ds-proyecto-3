import streamlit as st
from api_client import ApiClient


def render_create_task():
    st.subheader("Crear tarea")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)

    # Cargar incidentes para el dropdown
    try:
        incidents_resp = client.get_incidents()
        if incidents_resp.status_code != 200:
            st.error("No se pudieron cargar los incidentes.")
            return
        incidents = incidents_resp.json()
    except Exception as e:
        st.error(f"Error cargando incidentes: {e}")
        return

    if not incidents:
        st.info("No hay incidentes disponibles para asociar una tarea.")
        return

    # Cargar usuarios para asignación
    try:
        users_resp = client.get_users()
        if users_resp.status_code != 200:
            st.error("No se pudieron cargar los usuarios.")
            return
        users = users_resp.json()
    except Exception as e:
        st.error(f"Error cargando usuarios: {e}")
        return

    incident_options = {f"{inc['title']} ({inc['id'][:8]}...)": inc["id"] for inc in incidents}
    user_options = {f"{u['name']} ({u['email']})": u["id"] for u in users}

    with st.form("create_task_form"):
        selected_incident = st.selectbox("Incidente asociado", list(incident_options.keys()))
        title = st.text_input("Título de la tarea")
        description = st.text_area("Descripción de la tarea")
        selected_user = st.selectbox("Asignar a", list(user_options.keys()))
        submitted = st.form_submit_button("Crear tarea")

    if submitted:
        if not title.strip() or not description.strip():
            st.warning("Título y descripción son obligatorios.")
            return

        payload = {
            "incident_id": incident_options[selected_incident],
            "title": title,
            "description": description,
            "assigned_to": user_options[selected_user],
        }

        try:
            response = client.create_task(payload)
            if response.status_code == 201:
                st.success("Tarea creada correctamente.")
                st.session_state.current_view = "Tareas"
                st.rerun()
            else:
                st.error(f"No se pudo crear la tarea: {response.text}")
        except Exception as e:
            st.error(f"Error conectando con la API: {e}")
