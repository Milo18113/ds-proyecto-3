import streamlit as st
from api_client import ApiClient


def try_login(email, password):
    client = ApiClient()
    login_response = client.login(email, password)

    if login_response.status_code != 200:
        try:
            detail = login_response.json()
        except Exception:
            detail = login_response.text
        return False, f"Login falló: {detail}"

    login_data = login_response.json()

    token = (
        login_data.get("access_token")
        or login_data.get("token")
        or login_data.get("jwt")
    )

    if not token:
        return False, "La respuesta del login no incluyó token."

    auth_client = ApiClient(token=token)
    me_response = auth_client.me()

    if me_response.status_code != 200:
        try:
            detail = me_response.json()
        except Exception:
            detail = me_response.text
        return False, f"Login exitoso pero /me falló: {detail}"

    user_data = me_response.json()

    st.session_state.logged_in = True
    st.session_state.token = token
    st.session_state.user = user_data

    return True, "Login exitoso"


def render_login():
    st.title("OpsCenter")
    st.subheader("Iniciar sesión")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Ingresar")

    if submitted:
        if not email or not password:
            st.warning("Debes completar email y password.")
            return

        with st.spinner("Autenticando..."):
            try:
                ok, message = try_login(email, password)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Error conectando con la API: {e}")

    st.markdown("### Usuarios de prueba")
    st.code(
        "admin@opscenter.com / admin123\n"
        "supervisor@opscenter.com / super123\n"
        "operator@opscenter.com / oper123"
    )