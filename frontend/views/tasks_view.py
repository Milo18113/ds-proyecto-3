import streamlit as st
import pandas as pd
from api_client import ApiClient

TASK_STATUSES = ["OPEN", "IN_PROGRESS", "DONE"]


def render_tasks():
    st.subheader("Tareas")

    token = st.session_state.get("token")
    if not token:
        st.error("No hay sesión activa.")
        return

    client = ApiClient(token=token)

    try:
        response = client.get_tasks()

        if response.status_code != 200:
            st.error(f"No se pudieron cargar las tareas: {response.text}")
            return

        tasks = response.json()

        if not tasks:
            st.info("No hay tareas asignadas.")
            return

        df = pd.DataFrame(tasks)
        st.dataframe(df, use_container_width=True)

        st.markdown("### Actualizar estado de tarea")

        task_options = {f"{t['title']} ({t['id']})": t["id"] for t in tasks}
        selected_task_label = st.selectbox(
            "Selecciona una tarea",
            list(task_options.keys()),
        )
        new_status = st.selectbox("Nuevo estado", TASK_STATUSES)

        if st.button("Actualizar tarea"):
            task_id = task_options[selected_task_label]
            update_response = client.update_task_status(
                task_id,
                {"status": new_status},
            )

            if update_response.status_code == 200:
                st.success("Tarea actualizada correctamente.")
                st.rerun()
            else:
                st.error(f"No se pudo actualizar la tarea: {update_response.text}")

    except Exception as e:
        st.error(f"Error al consultar tareas: {e}")