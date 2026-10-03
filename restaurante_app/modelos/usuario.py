class Usuario:
    # Semana 16: roles basicos para diferenciar los tipos de usuario.
    ROL_ADMINISTRADOR = "Administrador"
    ROL_EMPLEADO = "Empleado"
    ROL_CLIENTE = "Cliente"
    ROLES = (ROL_ADMINISTRADOR, ROL_EMPLEADO, ROL_CLIENTE)

    def __init__(self, identificador, nombre, usuario, contrasena, rol=ROL_EMPLEADO):
        self.identificador = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def validar_texto(valor, campo):
        # Reutiliza una validacion basica para datos obligatorios.
        if not valor or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return str(valor).strip()

    @classmethod
    def validar_rol(cls, valor):
        # Acepta unicamente los roles definidos y devuelve su forma canonica.
        texto = cls.validar_texto(valor, "rol")

        for rol in cls.ROLES:
            if rol.lower() == texto.lower():
                return rol

        raise ValueError(f"El rol {texto} no es valido.")

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = self.validar_texto(valor, "contrasena")

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        self._rol = self.validar_rol(valor)
