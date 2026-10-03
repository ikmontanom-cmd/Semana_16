import tkinter as tk
from tkinter import messagebox, ttk

from ui.iconos import iconos


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f7fafc")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        # Contenedores y componentes que se reutilizan en la vista.
        self.contenido = None
        self.etiqueta_estado = None
        self.etiqueta_mensaje = None
        self.tabla_productos = None
        self.variables_formulario = {}

        # Semana 15: componentes de la seccion de ventas.
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.etiqueta_mensaje_venta = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        # Semana 16: componentes de la gestion de usuarios con eventos.
        self.tabla_usuarios = None
        self.rol_combo = None
        self.entrada_nombre_usuario = None
        self.etiqueta_mensaje_usuario = None
        self.variables_usuario = {}
        self.widgets_usuario = []

        self.definir_estilos()
        self.construir_interfaz()

    # ------------------------------------------------------------------ estilos
    def definir_estilos(self):
        # Define colores y estilos reutilizables de esta vista.
        self.color_fondo = "#f7fafc"
        self.color_encabezado = "#7c2d12"
        self.color_texto = "#243447"
        self.color_secundario = "#ffedd5"
        self.color_resaltado = "#ea580c"

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "MenuApp.TButton",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuApp.TButton", background=[("active", "#fed7aa")])

        estilo.configure(
            "CerrarSesion.TButton",
            background="#e11d48",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("CerrarSesion.TButton", background=[("active", "#be123c")])

        # Estilos de los botones de accion del formulario de productos.
        acciones = {
            "Registrar.TButton": ("#16a34a", "#15803d"),
            "Consultar.TButton": ("#0284c7", "#0369a1"),
            "Actualizar.TButton": ("#ea580c", "#c2410c"),
            "Eliminar.TButton": ("#e11d48", "#be123c"),
            "Limpiar.TButton": ("#64748b", "#475569"),
        }

        for nombre, (color, color_activo) in acciones.items():
            estilo.configure(
                nombre,
                background=color,
                foreground="#ffffff",
                font=("Arial", 10, "bold"),
                padding=(10, 7),
                borderwidth=0,
            )
            estilo.map(nombre, background=[("active", color_activo)])

        estilo.configure(
            "Tabla.Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.color_texto,
            rowheight=26,
            font=("Arial", 10),
            borderwidth=0,
        )
        estilo.configure(
            "Tabla.Treeview.Heading",
            background=self.color_encabezado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(6, 6),
        )
        estilo.map(
            "Tabla.Treeview",
            background=[("selected", self.color_resaltado)],
            foreground=[("selected", "#ffffff")],
        )

    # -------------------------------------------------------------- estructura
    def construir_interfaz(self):
        # Construye los contenedores principales de la pantalla.
        self.crear_encabezado()
        self.crear_barra_navegacion()
        self.crear_barra_estado()

        self.contenido = tk.Frame(self, bg=self.color_fondo, padx=24, pady=20)
        self.contenido.pack(fill="both", expand=True)

        self.mostrar_inicio()

    def crear_encabezado(self):
        # Contenedor superior con el logotipo y el usuario conectado.
        encabezado = tk.Frame(self, bg=self.color_encabezado, padx=28, pady=16)
        encabezado.pack(fill="x")

        logo = iconos.obtener("logo")
        if logo is not None:
            tk.Label(encabezado, image=logo, bg=self.color_encabezado).pack(
                side="left", padx=(0, 16)
            )

        textos = tk.Frame(encabezado, bg=self.color_encabezado)
        textos.pack(side="left", fill="x", expand=True)

        tk.Label(
            textos,
            text="RESTAURANTE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 19, "bold"),
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=f"Bienvenido, {self.usuario_actual.nombre}  |  Rol: {self.usuario_actual.rol}",
            bg=self.color_encabezado,
            fg="#ffedd5",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(4, 0))

    def crear_barra_navegacion(self):
        # Contenedor de navegacion entre las secciones del sistema.
        barra = tk.Frame(self, bg=self.color_secundario, padx=18, pady=10)
        barra.pack(fill="x")

        self.crear_boton_menu(barra, "Inicio", self.mostrar_inicio, "inicio")
        self.crear_boton_menu(barra, "Productos", self.mostrar_productos, "productos")
        # Semana 16: solo el administrador ve la gestion de usuarios.
        if self.restaurante_servicio.es_administrador(self.usuario_actual):
            self.crear_boton_menu(barra, "Usuarios", self.mostrar_usuarios, "usuarios")
        self.crear_boton_menu(barra, "Ventas", self.mostrar_ventas, "ventas")

        ttk.Button(
            barra,
            text=" Cerrar sesion",
            image=iconos.obtener("salir"),
            compound="left",
            command=self.cerrar_sesion,
            style="CerrarSesion.TButton",
        ).pack(side="right")

    def crear_boton_menu(self, contenedor, texto, comando, nombre_icono=None):
        # Agrega una opcion visual con icono en la barra superior.
        ttk.Button(
            contenedor,
            text=f" {texto}",
            image=iconos.obtener(nombre_icono) if nombre_icono else "",
            compound="left",
            command=comando,
            style="MenuApp.TButton",
        ).pack(side="left", padx=(0, 6))

    def crear_barra_estado(self):
        # Contenedor inferior con el resumen general del sistema.
        barra_estado = tk.Frame(self, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            text="",
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")

        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        # Refresca los contadores despues de cada operacion.
        if self.etiqueta_estado is None:
            return

        self.etiqueta_estado.config(
            text=(
                f"Productos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: {self.restaurante_servicio.cantidad_ventas()} | "
                "Datos JSON locales"
            )
        )

    def limpiar_contenido(self):
        # Limpia el area central antes de mostrar una nueva seccion.
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

        self.tabla_productos = None
        self.etiqueta_mensaje = None
        self.variables_formulario = {}

        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.etiqueta_mensaje_venta = None

        self.tabla_usuarios = None
        self.rol_combo = None
        self.entrada_nombre_usuario = None
        self.etiqueta_mensaje_usuario = None
        self.variables_usuario = {}
        self.widgets_usuario = []

    def crear_titulo_seccion(self, texto, nombre_icono=None):
        # Presenta el titulo de la seccion seleccionada con su icono.
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=f"  {texto}",
            image=iconos.obtener(nombre_icono) if nombre_icono else "",
            compound="left",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 14))

    # ------------------------------------------------------------------ inicio
    def mostrar_inicio(self):
        # Muestra el estado inicial de la interfaz principal.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Panel principal", "inicio")

        tarjetas = tk.Frame(self.contenido, bg=self.color_fondo)
        tarjetas.pack(fill="x")

        self.crear_tarjeta(
            tarjetas,
            "Productos",
            self.restaurante_servicio.cantidad_productos(),
            "productos",
        )
        self.crear_tarjeta(
            tarjetas,
            "Usuarios",
            self.restaurante_servicio.cantidad_usuarios(),
            "usuarios",
        )
        self.crear_tarjeta(
            tarjetas,
            "Ventas",
            self.restaurante_servicio.cantidad_ventas(),
            "ventas",
        )

        tk.Label(
            self.contenido,
            text=(
                "Seleccione una opcion de la barra superior. En la seccion Productos "
                "puede registrar, consultar, actualizar y eliminar registros. En la "
                "seccion Ventas puede relacionar un usuario con un producto. El "
                "administrador tambien gestiona los usuarios desde la seccion Usuarios."
            ),
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 11),
            wraplength=640,
            justify="left",
        ).pack(anchor="w", pady=(18, 0))

    def crear_tarjeta(self, contenedor, titulo, valor, nombre_icono):
        # Tarjeta informativa construida con un contenedor propio.
        tarjeta = tk.Frame(contenedor, bg="#ffffff", padx=18, pady=14)
        tarjeta.pack(side="left", padx=(0, 14))

        icono = iconos.obtener(nombre_icono)
        if icono is not None:
            tk.Label(tarjeta, image=icono, bg="#ffffff").pack(side="left", padx=(0, 12))

        textos = tk.Frame(tarjeta, bg="#ffffff")
        textos.pack(side="left")

        tk.Label(
            textos,
            text=str(valor),
            bg="#ffffff",
            fg=self.color_resaltado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=titulo,
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10),
        ).pack(anchor="w")

    # --------------------------------------------------------------- productos
    def mostrar_productos(self):
        # Construye el formulario, las acciones y la tabla de productos.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de productos", "productos")

        self.crear_formulario_productos(self.contenido)
        self.crear_acciones_productos(self.contenido)
        self.crear_mensaje_productos(self.contenido)
        self.crear_tabla_productos(self.contenido)

        self.refrescar_tabla_productos()

    def crear_formulario_productos(self, contenedor):
        # Contenedor de captura de datos organizado con grid.
        formulario = tk.LabelFrame(
            contenedor,
            text=" Datos del producto ",
            bg="#ffffff",
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=16,
            pady=14,
            bd=1,
            relief="solid",
        )
        formulario.pack(fill="x")

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.variables_formulario = {
            "codigo": tk.StringVar(),
            "nombre": tk.StringVar(),
            "precio": tk.StringVar(),
            "categoria": tk.StringVar(),
        }

        self.crear_campo(formulario, "Codigo", "codigo", 0, 0)
        self.crear_campo(formulario, "Nombre", "nombre", 0, 2)
        self.crear_campo(formulario, "Precio", "precio", 1, 0)

        tk.Label(
            formulario,
            text="Categoria",
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=2, sticky="w", padx=(0, 10), pady=6)

        combo = ttk.Combobox(
            formulario,
            textvariable=self.variables_formulario["categoria"],
            values=self.restaurante_servicio.categorias_disponibles(),
            state="readonly",
            font=("Arial", 10),
        )
        combo.grid(row=1, column=3, sticky="ew", pady=6)

    def crear_campo(self, contenedor, etiqueta, clave, fila, columna, variables=None, **opciones):
        # Crea una etiqueta y su entrada dentro del formulario. Se reutiliza en
        # productos y en usuarios: "variables" indica que formulario alimenta.
        variables = self.variables_formulario if variables is None else variables
        tk.Label(
            contenedor,
            text=etiqueta,
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 10), pady=6)

        entrada = tk.Entry(
            contenedor,
            textvariable=variables[clave],
            font=("Arial", 10),
            relief="solid",
            bd=1,
            **opciones,
        )
        entrada.grid(row=fila, column=columna + 1, sticky="ew", pady=6, ipady=3)

        return entrada

    def crear_acciones_productos(self, contenedor):
        # Contenedor con los botones de accion mediante command=.
        acciones = tk.Frame(contenedor, bg=self.color_fondo, pady=12)
        acciones.pack(fill="x")

        botones = [
            ("Registrar", self.registrar_producto, "Registrar.TButton", "agregar"),
            ("Consultar", self.consultar_producto, "Consultar.TButton", "buscar"),
            ("Actualizar", self.actualizar_producto, "Actualizar.TButton", "actualizar"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "eliminar"),
            ("Limpiar", self.limpiar_formulario, "Limpiar.TButton", "limpiar"),
        ]

        for texto, comando, estilo, nombre_icono in botones:
            ttk.Button(
                acciones,
                text=f" {texto}",
                image=iconos.obtener(nombre_icono),
                compound="left",
                command=comando,
                style=estilo,
            ).pack(side="left", padx=(0, 8))

    def crear_mensaje_productos(self, contenedor):
        # Area donde se informa el resultado de cada operacion.
        self.etiqueta_mensaje = tk.Label(
            contenedor,
            text="Complete el formulario y utilice los botones de accion.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 10),
            anchor="w",
        )
        self.etiqueta_mensaje.pack(fill="x", pady=(0, 10))

    def crear_tabla_productos(self, contenedor):
        # Contenedor de visualizacion con tabla y barra de desplazamiento.
        marco_tabla = tk.LabelFrame(
            contenedor,
            text=" Productos registrados ",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "precio", "categoria")
        self.tabla_productos = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Tabla.Treeview",
            height=6,
        )

        titulos = {
            "codigo": ("Codigo", 90, "w"),
            "nombre": ("Nombre", 230, "w"),
            "precio": ("Precio", 90, "e"),
            "categoria": ("Categoria", 150, "w"),
        }

        for columna in columnas:
            titulo, ancho, alineacion = titulos[columna]
            self.tabla_productos.heading(columna, text=titulo)
            self.tabla_productos.column(columna, width=ancho, anchor=alineacion)

        barra_scroll = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=barra_scroll.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

    def refrescar_tabla_productos(self):
        # Vuelve a cargar la tabla con la informacion entregada por el servicio.
        if self.tabla_productos is None:
            return

        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria,
                ),
            )

        self.actualizar_barra_estado()

    # ---------------------------------------------------- acciones de productos
    def leer_formulario(self):
        # Obtiene los valores escritos por el usuario en el formulario.
        return {
            clave: variable.get().strip()
            for clave, variable in self.variables_formulario.items()
        }

    def escribir_formulario(self, producto):
        # Carga en el formulario los datos de un producto consultado.
        self.variables_formulario["codigo"].set(producto.codigo)
        self.variables_formulario["nombre"].set(producto.nombre)
        self.variables_formulario["precio"].set(f"{producto.precio:.2f}")
        self.variables_formulario["categoria"].set(producto.categoria)

    def limpiar_formulario(self):
        # Deja el formulario en blanco para un nuevo registro.
        for variable in self.variables_formulario.values():
            variable.set("")

        self.mostrar_mensaje("Formulario limpio.")

    def mostrar_mensaje(self, texto, es_error=False):
        # Informa el resultado de la operacion dentro de la misma pantalla.
        if self.etiqueta_mensaje is None:
            return

        self.etiqueta_mensaje.config(
            text=texto,
            fg="#b42318" if es_error else "#15803d",
        )

    def registrar_producto(self):
        # Solicita el registro al servicio y actualiza la interfaz.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.registrar_producto(
                datos["codigo"], datos["nombre"], datos["precio"], datos["categoria"]
            )
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.mostrar_mensaje(f"Producto {producto.codigo} registrado correctamente.")

    def consultar_producto(self):
        # Carga en el formulario el producto solicitado por su codigo.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.obtener_producto(datos["codigo"])
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.escribir_formulario(producto)
        self.mostrar_mensaje(f"Producto {producto.codigo} cargado en el formulario.")

    def actualizar_producto(self):
        # Solicita la actualizacion al servicio y refresca la tabla.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.actualizar_producto(
                datos["codigo"], datos["nombre"], datos["precio"], datos["categoria"]
            )
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.mostrar_mensaje(f"Producto {producto.codigo} actualizado correctamente.")

    def eliminar_producto(self):
        # Confirma la accion y delega la eliminacion al servicio.
        datos = self.leer_formulario()

        if not datos["codigo"]:
            self.mostrar_mensaje("Ingrese el codigo del producto.", es_error=True)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Desea eliminar el producto {datos['codigo']}?",
        )

        if not confirmar:
            return

        try:
            producto = self.restaurante_servicio.eliminar_producto(datos["codigo"])
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.mostrar_mensaje(f"Producto {producto.codigo} eliminado.")

    # ---------------------------------------------------------------- usuarios
    def mostrar_usuarios(self):
        # Semana 16: formulario + tabla de usuarios gestionados mediante eventos.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de usuarios", "usuarios")

        # Regla de acceso: solo el administrador entra a esta seccion.
        if not self.restaurante_servicio.es_administrador(self.usuario_actual):
            self.mostrar_acceso_restringido()
            return

        # Los botones se empaquetan primero abajo para reservar su espacio; el
        # resto se reparte en dos columnas: formulario a la izquierda, tabla a la derecha.
        self.crear_acciones_usuarios(self.contenido)

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)

        columna_formulario = tk.Frame(cuerpo, bg=self.color_fondo)
        columna_formulario.pack(side="left", fill="y", padx=(0, 16))

        columna_tabla = tk.Frame(cuerpo, bg=self.color_fondo)
        columna_tabla.pack(side="left", fill="both", expand=True)

        self.crear_formulario_usuarios(columna_formulario)
        self.crear_mensaje_usuarios(columna_tabla)
        self.crear_tabla_usuarios(columna_tabla)

        # Aqui se conectan los eventos con sus callbacks mediante bind().
        self.asociar_eventos_usuarios()

        self.refrescar_tabla_usuarios()

    def mostrar_acceso_restringido(self):
        # Mensaje para quien llegue a la seccion sin rol de administrador.
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=(
                f"Acceso restringido. Su rol es {self.usuario_actual.rol} y la gestion "
                "de usuarios esta reservada al Administrador."
            ),
            bg="#ffffff",
            fg="#b42318",
            font=("Arial", 11, "bold"),
            padx=18,
            pady=16,
            wraplength=640,
            justify="left",
        ).pack(anchor="w")

    def crear_formulario_usuarios(self, contenedor):
        # Contenedor de captura de datos organizado con grid.
        formulario = tk.LabelFrame(
            contenedor,
            text=" Datos del usuario ",
            bg="#ffffff",
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=16,
            pady=10,
            bd=1,
            relief="solid",
        )
        formulario.pack(fill="x")

        formulario.columnconfigure(1, weight=1)

        self.variables_usuario = {
            "identificador": tk.StringVar(),
            "nombre": tk.StringVar(),
            "usuario": tk.StringVar(),
            "contrasena": tk.StringVar(),
            "rol": tk.StringVar(),
        }

        # El identificador lo genera el servicio: aqui solo se muestra.
        entrada_id = self.crear_campo(
            formulario, "Identificador", "identificador", 0, 0,
            variables=self.variables_usuario,
            width=22,
            state="readonly",
            readonlybackground="#f1f5f9",
        )
        entrada_nombre = self.crear_campo(
            formulario, "Nombre", "nombre", 1, 0,
            variables=self.variables_usuario, width=22,
        )
        entrada_usuario = self.crear_campo(
            formulario, "Usuario", "usuario", 2, 0,
            variables=self.variables_usuario, width=22,
        )
        entrada_clave = self.crear_campo(
            formulario, "Contrasena", "contrasena", 3, 0,
            variables=self.variables_usuario, width=22,
            show="*",
        )

        tk.Label(
            formulario,
            text="Rol",
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=6)

        self.rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.variables_usuario["rol"],
            values=self.restaurante_servicio.roles_gestionables(),
            state="readonly",
            font=("Arial", 10),
        )
        self.rol_combo.grid(row=4, column=1, sticky="ew", pady=6)

        tk.Label(
            formulario,
            text="Al actualizar, contrasena vacia = se conserva.",
            bg="#ffffff",
            fg="#64748b",
            font=("Arial", 9, "italic"),
            justify="left",
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(4, 0))

        # Widgets que reciben los atajos de teclado (<Return> y <Escape>).
        self.widgets_usuario = [entrada_id, entrada_nombre, entrada_usuario, entrada_clave, self.rol_combo]
        self.entrada_nombre_usuario = entrada_nombre

    def crear_acciones_usuarios(self, contenedor):
        # Los botones usan command=: una accion directa sobre un widget.
        acciones = tk.Frame(contenedor, bg=self.color_fondo, pady=10)
        acciones.pack(side="bottom", fill="x")

        botones = [
            ("Registrar", self.registrar_usuario, "Registrar.TButton", "agregar"),
            ("Actualizar", self.actualizar_usuario, "Actualizar.TButton", "actualizar"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton", "eliminar"),
            ("Limpiar", self.limpiar_formulario_usuario, "Limpiar.TButton", "limpiar"),
        ]

        for texto, comando, estilo, nombre_icono in botones:
            ttk.Button(
                acciones,
                text=f" {texto}",
                image=iconos.obtener(nombre_icono),
                compound="left",
                command=comando,
                style=estilo,
            ).pack(side="left", padx=(0, 8))

        tk.Label(
            acciones,
            text="Atajos:  Enter = registrar  |  Esc = limpiar",
            bg=self.color_fondo,
            fg="#64748b",
            font=("Arial", 9, "italic"),
        ).pack(side="right")

    def crear_mensaje_usuarios(self, contenedor):
        # Area donde se informa el resultado de cada operacion.
        self.etiqueta_mensaje_usuario = tk.Label(
            contenedor,
            text="Registre un usuario nuevo o seleccione una fila de la tabla.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 10),
            anchor="nw",
            justify="left",
            wraplength=480,
            height=2,
        )
        self.etiqueta_mensaje_usuario.pack(fill="x", pady=(0, 6))

    def mostrar_mensaje_usuario(self, texto, es_error=False, neutro=False):
        # Informa el resultado de la operacion dentro de la misma pantalla.
        if self.etiqueta_mensaje_usuario is None:
            return

        if es_error:
            color = "#b42318"
        elif neutro:
            color = self.color_texto
        else:
            color = "#15803d"

        self.etiqueta_mensaje_usuario.config(text=texto, fg=color)

    def crear_tabla_usuarios(self, contenedor):
        # Tabla con barra de desplazamiento. No incluye la contrasena.
        marco_tabla = tk.LabelFrame(
            contenedor,
            text=" Usuarios registrados ",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("identificador", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Tabla.Treeview",
            selectmode="browse",
            height=8,
        )

        titulos = {
            "identificador": ("Identificador", 100),
            "nombre": ("Nombre", 170),
            "usuario": ("Usuario", 120),
            "rol": ("Rol", 100),
        }

        for columna in columnas:
            titulo, ancho = titulos[columna]
            self.tabla_usuarios.heading(columna, text=titulo)
            self.tabla_usuarios.column(columna, width=ancho, anchor="w")

        barra_scroll = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=self.tabla_usuarios.yview
        )
        self.tabla_usuarios.configure(yscrollcommand=barra_scroll.set)

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

    def refrescar_tabla_usuarios(self):
        # Vuelve a cargar la tabla con la informacion entregada por el servicio.
        if self.tabla_usuarios is None:
            return

        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        for usuario in self.restaurante_servicio.listar_usuarios():
            # iid = identificador: el callback recupera el objeto con ese dato
            # y asi la contrasena nunca se guarda en la tabla.
            self.tabla_usuarios.insert(
                "",
                "end",
                iid=usuario.identificador,
                values=(usuario.identificador, usuario.nombre, usuario.usuario, usuario.rol),
            )

        self.actualizar_barra_estado()

    # ------------------------------------------------- eventos de usuarios
    def asociar_eventos_usuarios(self):
        # bind(evento, callback): el callback recibe un objeto "evento" con
        # informacion del widget que lo origino (evento.widget).
        assert self.tabla_usuarios is not None
        assert self.rol_combo is not None

        # Evento virtual de ttk: se dispara al cambiar la fila seleccionada.
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)

        # Evento virtual de ttk: se dispara al elegir una opcion del Combobox.
        self.rol_combo.bind("<<ComboboxSelected>>", self.al_cambiar_rol)

        # Teclado: Enter confirma el registro desde cualquier campo del formulario.
        for widget in self.widgets_usuario:
            widget.bind("<Return>", self.al_presionar_enter)

        # Teclado: Escape limpia el formulario tambien desde la tabla.
        for widget in self.widgets_usuario + [self.tabla_usuarios]:
            widget.bind("<Escape>", self.al_presionar_escape)

    def al_seleccionar_usuario(self, evento):
        # <<TreeviewSelect>>: carga en el formulario el usuario de la fila elegida.
        seleccion = evento.widget.selection()

        # Al limpiar o refrescar la tabla tambien se emite el evento, sin fila.
        if not seleccion:
            return

        identificador = seleccion[0]
        usuario = self.restaurante_servicio.buscar_usuario_por_identificador(identificador)

        if usuario is None:
            self.mostrar_mensaje_usuario("El usuario seleccionado ya no existe.", es_error=True)
            self.refrescar_tabla_usuarios()
            return

        self.escribir_formulario_usuario(usuario)

        if self.restaurante_servicio.es_administrador(usuario):
            self.mostrar_mensaje_usuario(
                f"Cuenta administrativa {usuario.identificador}: puede cambiar nombre, "
                "usuario o contrasena, pero no el rol ni eliminarla.",
                neutro=True,
            )
        else:
            self.mostrar_mensaje_usuario(
                f"Usuario {usuario.identificador} cargado. Puede actualizarlo o eliminarlo.",
                neutro=True,
            )

    def al_cambiar_rol(self, evento):
        # <<ComboboxSelected>>: responde al cambio de rol explicando que significa.
        rol = self.variables_usuario["rol"].get()
        descripcion = self.restaurante_servicio.descripcion_rol(rol)

        # Quita el resaltado azul que deja el combo de solo lectura.
        evento.widget.selection_clear()

        self.mostrar_mensaje_usuario(f"Rol {rol}: {descripcion}", neutro=True)

    def al_presionar_enter(self, evento):
        # <Return>: atajo que reutiliza el mismo metodo del boton Registrar.
        self.registrar_usuario()

    def al_presionar_escape(self, evento):
        # <Escape>: atajo que reutiliza el mismo metodo del boton Limpiar.
        self.limpiar_formulario_usuario()

    # -------------------------------------------------- acciones de usuarios
    def leer_formulario_usuario(self):
        # Obtiene los valores escritos por el usuario en el formulario.
        return {
            clave: variable.get().strip()
            for clave, variable in self.variables_usuario.items()
        }

    def escribir_formulario_usuario(self, usuario):
        # Carga en el formulario los datos de un usuario. La contrasena no se
        # muestra: queda vacia y solo se cambia si el administrador escribe otra.
        self.variables_usuario["identificador"].set(usuario.identificador)
        self.variables_usuario["nombre"].set(usuario.nombre)
        self.variables_usuario["usuario"].set(usuario.usuario)
        self.variables_usuario["contrasena"].set("")
        self.variables_usuario["rol"].set(usuario.rol)

        # El rol del administrador no se cambia: el combo queda bloqueado.
        es_admin = self.restaurante_servicio.es_administrador(usuario)
        self.rol_combo.configure(state="disabled" if es_admin else "readonly")

    def limpiar_formulario_usuario(self, mostrar_texto=True):
        # Estado inicial: formulario vacio, sin fila seleccionada y foco en Nombre.
        for variable in self.variables_usuario.values():
            variable.set("")

        if self.rol_combo is not None:
            self.rol_combo.configure(state="readonly")

        if self.tabla_usuarios is not None:
            self.tabla_usuarios.selection_remove(*self.tabla_usuarios.selection())

        if self.entrada_nombre_usuario is not None:
            self.entrada_nombre_usuario.focus_set()

        if mostrar_texto:
            self.mostrar_mensaje_usuario(
                "Formulario limpio. Registre un usuario nuevo o seleccione una fila.",
                neutro=True,
            )

    def registrar_usuario(self):
        # Solicita el registro al servicio y actualiza la interfaz.
        datos = self.leer_formulario_usuario()

        try:
            usuario = self.restaurante_servicio.registrar_usuario(
                self.usuario_actual,
                datos["nombre"],
                datos["usuario"],
                datos["contrasena"],
                datos["rol"],
            )
        except ValueError as error:
            self.mostrar_mensaje_usuario(str(error), es_error=True)
            return

        self.refrescar_tabla_usuarios()
        self.limpiar_formulario_usuario(mostrar_texto=False)
        self.mostrar_mensaje_usuario(f"Usuario {usuario.identificador} registrado correctamente.")

    def actualizar_usuario(self):
        # Solicita la actualizacion al servicio y refresca la tabla.
        datos = self.leer_formulario_usuario()

        try:
            usuario = self.restaurante_servicio.actualizar_usuario(
                self.usuario_actual,
                datos["identificador"],
                datos["nombre"],
                datos["usuario"],
                datos["contrasena"],
                datos["rol"],
            )
        except ValueError as error:
            self.mostrar_mensaje_usuario(str(error), es_error=True)
            return

        self.refrescar_tabla_usuarios()
        self.limpiar_formulario_usuario(mostrar_texto=False)
        self.mostrar_mensaje_usuario(f"Usuario {usuario.identificador} actualizado correctamente.")

    def eliminar_usuario(self):
        # Confirma la accion y delega la eliminacion al servicio.
        datos = self.leer_formulario_usuario()

        if not datos["identificador"]:
            self.mostrar_mensaje_usuario("Seleccione un usuario de la tabla.", es_error=True)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Desea eliminar al usuario {datos['identificador']} ({datos['usuario']})?",
        )

        if not confirmar:
            return

        try:
            usuario = self.restaurante_servicio.eliminar_usuario(
                self.usuario_actual, datos["identificador"]
            )
        except ValueError as error:
            self.mostrar_mensaje_usuario(str(error), es_error=True)
            return

        self.refrescar_tabla_usuarios()
        self.limpiar_formulario_usuario(mostrar_texto=False)
        self.mostrar_mensaje_usuario(f"Usuario {usuario.identificador} eliminado.")

    # ------------------------------------------------------------------ ventas
    def mostrar_ventas(self):
        # Construye el formulario de seleccion, la accion y la tabla de ventas.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Registro de ventas", "ventas")

        self.crear_formulario_ventas(self.contenido)
        self.crear_mensaje_ventas(self.contenido)
        self.crear_tabla_ventas(self.contenido)

        self.refrescar_tabla_ventas()

    def crear_formulario_ventas(self, contenedor):
        # Contenedor de seleccion de usuario y producto para la venta.
        formulario = tk.LabelFrame(
            contenedor,
            text=" Relacionar usuario y producto ",
            bg="#ffffff",
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=16,
            pady=14,
            bd=1,
            relief="solid",
        )
        formulario.pack(fill="x")

        formulario.columnconfigure(1, weight=1)

        tk.Label(
            formulario,
            text="Usuario",
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)

        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            values=list(self.obtener_opciones_usuarios_venta().keys()),
            state="readonly",
            font=("Arial", 10),
        )
        self.usuario_venta_combo.grid(row=0, column=1, sticky="ew", pady=6)

        tk.Label(
            formulario,
            text="Producto",
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)

        self.producto_venta_combo = ttk.Combobox(
            formulario,
            values=list(self.obtener_opciones_productos_venta().keys()),
            state="readonly",
            font=("Arial", 10),
        )
        self.producto_venta_combo.grid(row=1, column=1, sticky="ew", pady=6)

        acciones = tk.Frame(formulario, bg="#ffffff")
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # El boton utiliza command= para ejecutar el callback de venta.
        ttk.Button(
            acciones,
            text=" Registrar venta",
            image=iconos.obtener("agregar"),
            compound="left",
            command=self.registrar_venta,
            style="Registrar.TButton",
        ).pack(side="left")

    def obtener_opciones_usuarios_venta(self):
        # Relaciona el texto mostrado en el combo con el identificador real.
        self.opciones_usuarios_venta = {
            f"{usuario.identificador} - {usuario.nombre}": usuario.identificador
            for usuario in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        # Relaciona el texto mostrado en el combo con el codigo real.
        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def crear_mensaje_ventas(self, contenedor):
        # Area donde se informa el resultado del registro de la venta.
        self.etiqueta_mensaje_venta = tk.Label(
            contenedor,
            text="Seleccione un usuario y un producto, luego registre la venta.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 10),
            anchor="w",
        )
        self.etiqueta_mensaje_venta.pack(fill="x", pady=(10, 10))

    def mostrar_mensaje_venta(self, texto, es_error=False):
        # Informa el resultado de la operacion dentro de la misma pantalla.
        if self.etiqueta_mensaje_venta is None:
            return

        self.etiqueta_mensaje_venta.config(
            text=texto,
            fg="#b42318" if es_error else "#15803d",
        )

    def crear_tabla_ventas(self, contenedor):
        # Contenedor de visualizacion con tabla y barra de desplazamiento.
        marco_tabla = tk.LabelFrame(
            contenedor,
            text=" Ventas registradas ",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("identificador", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Tabla.Treeview",
            height=6,
        )

        titulos = {
            "identificador": ("Venta", 80, "w"),
            "usuario": ("Usuario", 220, "w"),
            "producto": ("Producto", 220, "w"),
            "fecha": ("Fecha", 110, "w"),
        }

        for columna in columnas:
            titulo, ancho, alineacion = titulos[columna]
            self.tabla_ventas.heading(columna, text=titulo)
            self.tabla_ventas.column(columna, width=ancho, anchor=alineacion)

        barra_scroll = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=barra_scroll.set)

        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

    def refrescar_tabla_ventas(self):
        # Vuelve a cargar la tabla con la informacion entregada por el servicio.
        if self.tabla_ventas is None:
            return

        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario_por_identificador(venta.usuario_id)
            producto = self.restaurante_servicio.buscar_producto(venta.producto_codigo)

            texto_usuario = venta.usuario_id if usuario is None else f"{usuario.identificador} - {usuario.nombre}"
            texto_producto = venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"

            self.tabla_ventas.insert(
                "",
                "end",
                values=(venta.identificador, texto_usuario, texto_producto, venta.fecha),
            )

        self.actualizar_barra_estado()

    def registrar_venta(self):
        # Callback de venta: obtiene la seleccion de la interfaz, delega el
        # registro a RestauranteServicio y actualiza la vista con el resultado.
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        usuario_id = self.opciones_usuarios_venta.get(self.usuario_venta_combo.get(), "")
        producto_codigo = self.opciones_productos_venta.get(self.producto_venta_combo.get(), "")

        try:
            venta = self.restaurante_servicio.registrar_venta(usuario_id, producto_codigo)
        except ValueError as error:
            self.mostrar_mensaje_venta(str(error), es_error=True)
            return

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")
        self.refrescar_tabla_ventas()
        self.mostrar_mensaje_venta(f"Venta {venta.identificador} registrada correctamente.")

    # ------------------------------------------------------------------- otros
    def cerrar_sesion(self):
        # Regresa al login sin crear otra ventana ni otro mainloop.
        self.al_cerrar_sesion()
