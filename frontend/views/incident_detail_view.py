import streamlit as st
from api_client import ApiClient

INCIDENT_STATUSES = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"]


def render_incident_detail():
    st.subheader("Detalle de incidente")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)
    role = (st.session_state.get("user") or {}).get("role", "").upper()
    incident_id = st.session_state.get("selected_incident_id")

    if not incident_id:
        st.warning("No se seleccionó ningún incidente.")
        return

    try:
        response = client.get_incident_detail(incident_id)
        if response.status_code != 200:
            st.error(f"No se pudo cargar el incidente: {response.text}")
            return

        incident = response.json()
    except Exception as e:
        st.error(f"Error al consultar detalle: {e}")
        return

    # ── Información del incidente ─────────────────────────────────────

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Título:** {incident['title']}")
        st.markdown(f"**Severidad:** {incident['severity']}")
        st.markdown(f"**Estado:** {incident['status']}")
    with col2:
        st.markdown(f"**Creado por:** {incident['created_by']}")
        st.markdown(f"**Asignado a:** {incident.get('assigned_to') or 'Sin asignar'}")
        st.markdown(f"**Fecha de creación:** {incident['created_at']}")

    st.markdown(f"**Descripción:** {incident['description']}")

    # ── Tareas asociadas ──────────────────────────────────────────────

    st.markdown("---")
    st.markdown("### Tareas asociadas")

    tasks = incident.get("tasks", [])
    if tasks:
        for t in tasks:
            with st.expander(f"{t['title']} — {t['status']}"):
                st.write(f"**Descripción:** {t['description']}")
                st.write(f"**Asignado a:** {t['assigned_to']}")
                st.write(f"**Creada:** {t['created_at']}")
    else:
        st.info("No hay tareas asociadas a este incidente.")

    # ── Acciones de Supervisor / Admin ────────────────────────────────

    if role in ("SUPERVISOR", "ADMIN"):
        st.markdown("---")

        col_assign, col_status = st.columns(2)

        # Asignar incidente
        with col_assign:
            st.markdown("### Asignar incidente")
            try:
                users_resp = client.get_users()
                if users_resp.status_code == 200:
                    users = users_resp.json()
                    user_options = {f"{u['name']} ({u['email']})": u["id"] for u in users}
                    selected_user = st.selectbox(
                        "Asignar a",
                        list(user_options.keys()),
                        key="assign_user_select",
                    )
                    if st.button("Asignar"):
                        user_id = user_options[selected_user]
                        resp = client.assign_incident(incident_id, {"assigned_to": user_id})
                        if resp.status_code == 200:
                            st.success("Incidente asignado correctamente.")
                            st.rerun()
                        else:
                            st.error(f"Error al asignar: {resp.text}")
                else:
                    st.warning("No se pudieron cargar los usuarios.")
            except Exception as e:
                st.error(f"Error cargando usuarios: {e}")

        # Cambiar estado
        with col_status:
            st.markdown("### Cambiar estado")
            new_status = st.selectbox(
                "Nuevo estado",
                INCIDENT_STATUSES,
                key="change_status_select",
            )
            if st.button("Cambiar estado"):
                resp = client.change_incident_status(incident_id, {"status": new_status})
                if resp.status_code == 200:
                    st.success("Estado actualizado correctamente.")
                    st.rerun()
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"Error al cambiar estado: {detail}")

    # ── Botón volver ──────────────────────────────────────────────────

    if st.button("← Volver a incidentes"):
        st.session_state.selected_incident_id = None
        st.session_state.current_view = "Incidentes"
        st.rerun()
