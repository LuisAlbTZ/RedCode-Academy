from datetime import datetime
from src.infrastructure.database.connection import db


# ==============================================================================
# MODELO PRINCIPAL DE USUARIO
# ==============================================================================
class Usuario(db.Model):
    '''
    Modelo principal para los Usuarios de la plataforma.
    Implementa el mixin UserMixin de Flask-Login para gestión de sesiones.
    '''
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Rol global / Permiso Administrador
    es_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Estado de la cuenta (Activo, Inactivo, Suspendido)
    estado_cuenta = db.Column(db.String(20), nullable=False, default='Activo')

    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, nombre, apellido, fecha_nacimiento, correo_electronico, 
                 password_hash, es_admin=False, estado_cuenta='Activo', **kwargs):
        
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.correo_electronico = correo_electronico
        self.password_hash = password_hash
        self.es_admin = es_admin
        self.estado_cuenta = estado_cuenta
        
        # Esto permite que SQLAlchemy asigne automáticamente 'id' o 'fecha_registro' si se envían
        super().__init__(**kwargs)

    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.estado_cuenta == 'Activo'

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"<Usuario {self.correo_electronico}>"

# ==============================================================================
# TABLA ASOCIATIVA Y DE RELACIÓN (USUARIOS Y CONVOCATORIAS)
# ==============================================================================
class UsuarioConvocatoria(db.Model):
    '''
    Modelo que almacena la relación entre usuarios y convocatorias.
    Permite asignar roles específicos a un usuario dentro de una convocatoria en particular,
    y manejar los estados de validación para las convocatorias privadas.
    '''
    __tablename__ = 'usuario_convocatoria'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    convocatoria_id = db.Column(db.Integer, db.ForeignKey('convocatoria.id'), nullable=False)

    # Rol del usuario en esta convocatoria específica: 'Aprendiz', 'Mentor' o 'Jurado'
    rol_en_convocatoria = db.Column(db.String(50), nullable=False)

    # Estado de validación, crucial para las convocatorias privadas donde el
    # Mentor debe validar a los participantes y al jurado
    estado_validacion = db.Column(db.String(20), default='Pendiente')  # Pendiente, Aprobado, Rechazado

    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones SQLAlchemy
    usuario = db.relationship('Usuario', backref=db.backref('convocatorias_asociadas', lazy=True))
    convocatoria = db.relationship('Convocatoria', backref=db.backref('usuarios_asociados', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Relacion Usuario:{self.usuario_id} - Convocatoria:{self.convocatoria_id} - Rol:{self.rol_en_convocatoria}>"

# ==============================================================================
# MODELO PRINCIPAL DE CONVOCATORIA
# ==============================================================================
class Convocatoria(db.Model):
    '''
    Modelo principal para las Convocatorias.
    Almacena toda la configuración, métricas y restricciones definidas por los Mentores.
    '''
    __tablename__ = 'convocatoria'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    # Lógica de Negocio: Públicas (Gratis) vs Privadas (Pago)
    visibilidad = db.Column(db.String(50), nullable=False, default='Pública')  # Pública, Privada
    costo = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)

    # Parámetros y Fechas de la convocatoria
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)

    # Reglas, Especificaciones y Métricas
    reglas = db.Column(db.Text, nullable=False)
    especificaciones = db.Column(db.Text, nullable=False)
    indicaciones = db.Column(db.Text, nullable=False)
    metricas_evaluacion = db.Column(db.Text, nullable=False)

    # Campos que a futuro podrían normalizarse en sus propias tablas relacionadas
    tecnologias_sugeridas = db.Column(db.Text, nullable=True)
    patrocinadores = db.Column(db.Text, nullable=True)

    # Configuraciones de Participación
    modalidad = db.Column(db.String(50), nullable=False, default='Individual')  # Individual, Equipo
    min_participantes = db.Column(db.Integer, default=1)
    max_participantes = db.Column(db.Integer, default=1)

    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Activa')  # Borrador, Activa, Finalizada

    # Relación con WorkGroups
    work_groups = db.relationship('WorkGroup', backref='convocatoria', lazy=True)

    def __repr__(self):
        return f"<Convocatoria {self.titulo} ({self.visibilidad})>"

# ==============================================================================
# MODELO DE PUBLICACIÓN / REPOSITORIO (WORK GROUP)
# ==============================================================================
class WorkGroup(db.Model):
    '''
    Modelo que actúa como una publicación tipo Reddit y un repositorio estilo GitHub.
    Permite a los usuarios subir texto, código, imágenes y recibir comentarios/clasificaciones.
    '''
    __tablename__ = 'work_group'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)

    # Contenidos principales de la publicación
    descripcion_texto = db.Column(db.Text, nullable=True)  # 1. Texto (Explicación, Markdown, etc.)
    contenido_codigo = db.Column(db.Text, nullable=True)   # 2. Código (Snippets o código principal)

    # Enlace a repositorio externo si aplica (GitHub)
    enlace_repositorio = db.Column(db.String(255), nullable=True)

    # Sistema de clasificación tipo Reddit (Upvotes / Puntuación)
    puntuacion = db.Column(db.Integer, default=0)

    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones (A qué convocatoria pertenece y quién lo publicó)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    convocatoria_id = db.Column(db.Integer, db.ForeignKey('convocatoria.id'), nullable=False)

    # Relaciones SQLAlchemy
    autor = db.relationship('Usuario', backref=db.backref('work_groups', lazy=True))
    comentarios = db.relationship('ComentarioWorkGroup', backref='work_group', lazy=True, cascade="all, delete-orphan")
    calificaciones = db.relationship('CalificacionWorkGroup', backref='work_group', lazy=True, cascade="all, delete-orphan")

    @property
    def promedio_calificacion(self):
        if not self.calificaciones:
            return 0
        return sum(c.calificacion for c in self.calificaciones) / len(self.calificaciones)

    def __repr__(self):
        return f"<WorkGroup {self.titulo} - Puntuación: {self.puntuacion}>"

# ==============================================================================
# MODELO DE COMENTARIOS (JURADO / MENTORES)
# ==============================================================================
class ComentarioWorkGroup(db.Model):
    '''
    Comentarios para las publicaciones de Work_Group.
    Permite a mentores y jurado dar feedback.
    '''
    __tablename__ = 'comentario_work_group'

    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)

    # Quién comenta (Mentor / Jurado / Otro usuario)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # A qué publicación (WorkGroup) pertenece el comentario
    work_group_id = db.Column(db.Integer, db.ForeignKey('work_group.id'), nullable=False)

    fecha_comentario = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el usuario que comenta
    autor = db.relationship('Usuario', backref=db.backref('comentarios', lazy=True))

    def __repr__(self):
        return f"<Comentario de Usuario {self.usuario_id} en WorkGroup {self.work_group_id}>"

# ==============================================================================
# MODELO DE CALIFICACIONES
# ==============================================================================
class CalificacionWorkGroup(db.Model):
    '''
    Calificaciones para las publicaciones de Work_Group.
    Permite a mentores y jurado dar feedback cuantitativo.
    '''
    __tablename__ = 'calificacion_work_group'

    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.Integer, nullable=False)  # Ej: 1-10

    # Quién califica (Mentor / Jurado)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # A qué publicación (WorkGroup) pertenece la calificación
    work_group_id = db.Column(db.Integer, db.ForeignKey('work_group.id'), nullable=False)

    fecha_calificacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el usuario que califica
    calificador = db.relationship('Usuario', backref=db.backref('calificaciones_dadas', lazy=True))

    def __repr__(self):
        return f"<Calificación de Usuario {self.usuario_id} en WorkGroup {self.work_group_id}>"
