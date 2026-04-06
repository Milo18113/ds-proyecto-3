import os
from datetime import datetime, timedelta

from jose import JWTError, jwt

from backend.domain.enums.role import Role

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY no está definida. Configúrala en el entorno o en el archivo .env "
        "(copia .env.example a .env)."
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(user_id: str, role: Role) -> str:
    """
    Genera un JWT firmado con el ID y rol del usuario.
    El token expira según ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    payload = {
        "sub": user_id,
        "role": role.value,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodifica y valida un JWT.
    Retorna el payload si el token es válido.
    Lanza TokenExpiredError o InvalidTokenError si no lo es.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise InvalidTokenError(f"Token inválido o expirado: {e}")


def extract_user_id(token: str) -> str:
    """Extrae el user_id del campo 'sub' del token."""
    return decode_access_token(token)["sub"]


def extract_role(token: str) -> Role:
    """Extrae el rol del usuario desde el token."""
    raw_role = decode_access_token(token)["role"]
    return Role(raw_role)


class InvalidTokenError(Exception):
    """Excepción de dominio para tokens inválidos o expirados."""
    pass