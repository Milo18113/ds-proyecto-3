from passlib.context import CryptContext

# bcrypt como algoritmo principal, con soporte a versiones deprecadas
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hashea una contraseña en texto plano usando bcrypt.
    Llamar al crear un usuario nuevo.
    """
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.
    Llamar en el flujo de login antes de generar el token.
    """
    return _pwd_context.verify(plain_password, hashed_password)