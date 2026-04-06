class EmailProvider:
    """
    Provider concreto para envío por email.
    Aquí luego podrían integrar un proveedor real.
    """

    def send(self, recipient: str, message: str) -> None:
        print(f"[EMAIL] To={recipient}\n{message}")