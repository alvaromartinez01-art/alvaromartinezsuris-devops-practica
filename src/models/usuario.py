import uuid


class Usuario:
    def __init__(self, nombre: str, email: str):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email

    def is_admin(self) -> bool:
        # por defecto un usuario normal no es admin
        return False

    def __str__(self):
        return f"[{self.id}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    def __init__(self, nombre: str, email: str, direccion: str):
        super().__init__(nombre, email)
        self.direccion = direccion

    def __str__(self):
        return f"{super().__str__()} | Direccion: {self.direccion}"


class Administrador(Usuario):
    def is_admin(self) -> bool:
        # los administradores si tienen permisos
        return True

    def __str__(self):
        return f"{super().__str__()} | Rol: Administrador"
