class Producto:
    def __init__(self, codigo, nombre, precio, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    @staticmethod
    def validar_texto(valor, campo):
        # Reutiliza una validacion basica para datos obligatorios.
        if not valor or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return str(valor).strip()

    @staticmethod
    def validar_precio(valor):
        # Verifica que el precio sea un numero valido y no negativo.
        try:
            precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El campo precio debe ser un numero.")

        if precio < 0:
            raise ValueError("El campo precio no puede ser negativo.")

        return precio

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = self.validar_texto(valor, "codigo")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = self.validar_precio(valor)

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = self.validar_texto(valor, "categoria")
