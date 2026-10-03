from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    ARCHIVO_USUARIOS = "usuarios.json"
    ARCHIVO_PRODUCTOS = "productos.json"
    ARCHIVO_VENTAS = "ventas.json"
    CATEGORIAS = ["Entradas", "Platos fuertes", "Bebidas", "Postres"]

    # Semana 16: el administrador solo gestiona Empleados y Clientes.
    ROLES_GESTIONABLES = [Usuario.ROL_EMPLEADO, Usuario.ROL_CLIENTE]
    DESCRIPCION_ROLES = {
        Usuario.ROL_ADMINISTRADOR: "Administra el sistema y gestiona los usuarios.",
        Usuario.ROL_EMPLEADO: "Personal del restaurante: atiende pedidos y registra ventas.",
        Usuario.ROL_CLIENTE: "Persona que consume en el restaurante y puede iniciar sesion.",
    }

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json(self.ARCHIVO_USUARIOS)
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
                # Los registros antiguos sin rol se tratan como Empleado.
                datos.get("rol", Usuario.ROL_EMPLEADO),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("precio", 0),
                datos.get("categoria", ""),
            )
            for datos in productos_json
        ]

        # Semana 15: carga las ventas persistidas para mostrarlas en la interfaz.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        # Verifica si las credenciales coinciden con un usuario cargado.
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado

        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        # Entrega los usuarios cargados para mostrarlos en la interfaz.
        return self.usuarios

    def listar_productos(self):
        # Entrega los productos cargados para mostrarlos en la interfaz.
        return self.productos

    def listar_ventas(self):
        # Entrega las ventas cargadas para mostrarlas en la interfaz.
        return self.ventas

    def buscar_usuario_por_identificador(self, identificador):
        # Busca un usuario por su identificador y devuelve None si no existe.
        identificador = str(identificador).strip()

        for usuario in self.usuarios:
            if usuario.identificador == identificador:
                return usuario

        return None

    # ---------------------------------------------------------------- usuarios
    def es_administrador(self, usuario):
        # Indica si el usuario recibido tiene el rol Administrador.
        return usuario is not None and usuario.rol == Usuario.ROL_ADMINISTRADOR

    def exigir_administrador(self, solicitante):
        # Regla de acceso: la gestion de usuarios es solo para administradores.
        if not self.es_administrador(solicitante):
            raise ValueError("Solo el administrador puede gestionar usuarios.")

    def roles_gestionables(self):
        # Roles que el administrador puede asignar desde la interfaz.
        return list(self.ROLES_GESTIONABLES)

    def descripcion_rol(self, rol):
        # Texto breve que explica que representa cada rol.
        return self.DESCRIPCION_ROLES.get(rol, "")

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        # Busca por nombre de usuario sin distinguir mayusculas y minusculas.
        nombre_usuario = str(nombre_usuario).strip().lower()

        for usuario in self.usuarios:
            if usuario.usuario.lower() == nombre_usuario:
                return usuario

        return None

    def obtener_usuario(self, identificador):
        # Devuelve el usuario solicitado o informa que no existe.
        if not str(identificador).strip():
            raise ValueError("Seleccione un usuario de la tabla.")

        usuario = self.buscar_usuario_por_identificador(identificador)

        if usuario is None:
            raise ValueError(f"No existe un usuario con el identificador {identificador}.")

        return usuario

    def generar_identificador_usuario(self):
        # Toma el mayor numero usado (U001, U002...) para no repetir ids tras eliminar.
        mayor = 0

        for usuario in self.usuarios:
            numero = usuario.identificador[1:]
            if usuario.identificador.upper().startswith("U") and numero.isdigit():
                mayor = max(mayor, int(numero))

        return f"U{mayor + 1:03d}"

    def validar_rol_gestionable(self, rol):
        # Solo se permiten los roles Empleado y Cliente en el formulario.
        rol = Usuario.validar_rol(rol) if str(rol).strip() else ""

        if not rol:
            raise ValueError("Seleccione un rol para el usuario.")
        if rol not in self.ROLES_GESTIONABLES:
            raise ValueError("El administrador solo gestiona usuarios Empleado o Cliente.")

        return rol

    def validar_usuario_disponible(self, nombre_usuario, ignorar=None):
        # Evita dos cuentas con el mismo nombre de usuario.
        existente = self.buscar_usuario_por_nombre_usuario(nombre_usuario)

        if existente is not None and existente is not ignorar:
            raise ValueError(f"El usuario {existente.usuario} ya esta registrado.")

    def exigir_cuenta_gestionable(self, usuario):
        # Las cuentas administrativas solo se consultan, no se modifican aqui.
        if self.es_administrador(usuario):
            raise ValueError("Las cuentas administrativas no se gestionan desde esta pantalla.")

    def registrar_usuario(self, solicitante, nombre, usuario, contrasena, rol):
        # Valida los datos, crea el usuario y guarda los cambios.
        self.exigir_administrador(solicitante)
        rol = self.validar_rol_gestionable(rol)

        nuevo = Usuario(self.generar_identificador_usuario(), nombre, usuario, contrasena, rol)
        self.validar_usuario_disponible(nuevo.usuario)

        self.usuarios.append(nuevo)
        self.guardar_usuarios()

        return nuevo

    def actualizar_usuario(self, solicitante, identificador, nombre, usuario, contrasena, rol):
        # Modifica un usuario existente; si la contrasena llega vacia se conserva.
        self.exigir_administrador(solicitante)
        actual = self.obtener_usuario(identificador)

        if self.es_administrador(actual):
            # El administrador solo edita su propia cuenta y no puede cambiar su rol.
            if actual.identificador != solicitante.identificador:
                self.exigir_cuenta_gestionable(actual)
            if str(rol).strip().lower() != Usuario.ROL_ADMINISTRADOR.lower():
                raise ValueError("No puede cambiar el rol del administrador actual.")
            rol = Usuario.ROL_ADMINISTRADOR
        else:
            rol = self.validar_rol_gestionable(rol)

        # Se crea un candidato primero: si algun dato es invalido no se altera el original.
        candidato = Usuario(
            actual.identificador,
            nombre,
            usuario,
            contrasena if str(contrasena).strip() else actual.contrasena,
            rol,
        )
        self.validar_usuario_disponible(candidato.usuario, ignorar=actual)

        actual.nombre = candidato.nombre
        actual.usuario = candidato.usuario
        actual.contrasena = candidato.contrasena
        actual.rol = candidato.rol

        self.guardar_usuarios()

        return actual

    def eliminar_usuario(self, solicitante, identificador):
        # Quita un usuario de la lista y actualiza el archivo JSON.
        self.exigir_administrador(solicitante)
        usuario = self.obtener_usuario(identificador)

        if usuario.identificador == solicitante.identificador:
            raise ValueError("No puede eliminar la cuenta con la que inicio sesion.")

        self.exigir_cuenta_gestionable(usuario)

        self.usuarios.remove(usuario)
        self.guardar_usuarios()

        return usuario

    def guardar_usuarios(self):
        # Delega la escritura del archivo JSON al servicio de archivos.
        datos = [
            {
                "identificador": usuario.identificador,
                "nombre": usuario.nombre,
                "usuario": usuario.usuario,
                "contraseña": usuario.contrasena,
                "rol": usuario.rol,
            }
            for usuario in self.usuarios
        ]

        self.archivo_servicio.escribir_json(self.ARCHIVO_USUARIOS, datos)

    def categorias_disponibles(self):
        # Entrega las categorias permitidas para el formulario de productos.
        categorias = list(self.CATEGORIAS)

        for producto in self.productos:
            if producto.categoria not in categorias:
                categorias.append(producto.categoria)

        return categorias

    def buscar_producto(self, codigo):
        # Busca un producto por su codigo y devuelve None si no existe.
        codigo = str(codigo).strip().upper()

        for producto in self.productos:
            if producto.codigo.upper() == codigo:
                return producto

        return None

    def obtener_producto(self, codigo):
        # Devuelve el producto solicitado o informa que no existe.
        if not str(codigo).strip():
            raise ValueError("Ingrese el codigo del producto.")

        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError(f"No existe un producto con el codigo {codigo}.")

        return producto

    def registrar_producto(self, codigo, nombre, precio, categoria):
        # Valida los datos, crea el producto y guarda los cambios.
        producto = Producto(codigo, nombre, precio, categoria)

        if self.buscar_producto(producto.codigo) is not None:
            raise ValueError(f"El codigo {producto.codigo} ya esta registrado.")

        self.productos.append(producto)
        self.guardar_productos()

        return producto

    def actualizar_producto(self, codigo, nombre, precio, categoria):
        # Modifica los datos de un producto existente y persiste el cambio.
        producto = self.obtener_producto(codigo)

        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria

        self.guardar_productos()

        return producto

    def eliminar_producto(self, codigo):
        # Quita un producto de la lista y actualiza el archivo JSON.
        producto = self.obtener_producto(codigo)

        self.productos.remove(producto)
        self.guardar_productos()

        return producto

    def guardar_productos(self):
        # Delega la escritura del archivo JSON al servicio de archivos.
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "categoria": producto.categoria,
            }
            for producto in self.productos
        ]

        self.archivo_servicio.escribir_json(self.ARCHIVO_PRODUCTOS, datos)

    # ------------------------------------------------------------------ ventas
    def generar_identificador_venta(self):
        # Genera un identificador secuencial simple para la nueva venta.
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_id, producto_codigo):
        # Valida la seleccion, relaciona usuario y producto, y persiste la venta.
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario_por_identificador(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        if self.buscar_producto(producto_codigo) is None:
            raise ValueError("El producto seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )

        self.ventas.append(nueva_venta)
        self.guardar_ventas()

        return nueva_venta

    def guardar_ventas(self):
        # Delega la escritura del archivo JSON al servicio de archivos.
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_codigo": venta.producto_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]

        self.archivo_servicio.escribir_json(self.ARCHIVO_VENTAS, datos)
