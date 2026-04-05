import streamlit as st
from views.login_view import render_login
from views.incidents_view import render_incidents
from views.create_incident_view import render_create_incident
from views.tasks_view import render_tasks
from views.notifications_view import render_notifications

st.set_page_config(page_title="OpsCenter", page_icon="🚨", layout="wide")


def init_session():
    defaults = {
        "logged_in": False,
        "token": None,
        "user": None,
        "current_view": "Incidentes",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_view = "Incidentes"
    st.rerun()


def get_menu_for_role(role):
    role = (role or "").upper()

    if role == "ADMIN":
        return ["Incidentes", "Crear incidente", "Tareas", "Notificaciones"]
    if role == "SUPERVISOR":
        return ["Incidentes", "Crear incidente", "Tareas", "Notificaciones"]
    return ["Incidentes", "Crear incidente", "Tareas", "Notificaciones"]


def render_sidebar():
    user = st.session_state.user or {}
    role = user.get("role", "UNKNOWN")
    name = (
        user.get("name")
        or user.get("full_name")
        or user.get("email")
        or user.get("user_id", "Usuario")
    )

    st.sidebar.title("OpsCenter")
    st.sidebar.write(f"**Usuario:** {name}")
    st.sidebar.write(f"**Rol:** {role}")

    menu_options = get_menu_for_role(role)
    selected = st.sidebar.radio("Navegación", menu_options)
    st.session_state.current_view = selected

    if st.sidebar.button("Cerrar sesión"):
        logout()


def render_home():
    user = st.session_state.user or {}
    role = user.get("role", "UNKNOWN")
    current_view = st.session_state.current_view

    st.title(current_view)
    st.write(f"Bienvenido. Tu rol actual es: **{role}**")

    if current_view == "Incidentes":
        render_incidents()
    elif current_view == "Crear incidente":
        render_create_incident()
    elif current_view == "Tareas":
        render_tasks()
    elif current_view == "Notificaciones":
        render_notifications()


def main():
    init_session()

    if not st.session_state.logged_in:
        render_login()
    else:
        render_sidebar()
        render_home()


if __name__ == "__main__":
    main()