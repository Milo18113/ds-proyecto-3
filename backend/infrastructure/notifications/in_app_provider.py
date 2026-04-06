class InAppProvider:
    """
    Provider concreto para notificaciones in-app.
    """

    def send(self, recipient: str, message: str) -> None:
        print(f"[IN_APP] User={recipient}\n{message}")