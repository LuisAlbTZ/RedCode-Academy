-- SQL Schema for RedCode Academy

CREATE DATABASE IF NOT EXISTS redcode_academy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE redcode_academy;

-- Table: usuario
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE,
    estado_cuenta VARCHAR(20) NOT NULL DEFAULT 'Activo',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Table: convocatoria
CREATE TABLE convocatoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    visibilidad VARCHAR(50) NOT NULL DEFAULT 'Pública',
    costo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    reglas TEXT NOT NULL,
    especificaciones TEXT NOT NULL,
    indicaciones TEXT NOT NULL,
    metricas_evaluacion TEXT NOT NULL,
    tecnologias_sugeridas TEXT,
    patrocinadores TEXT,
    modalidad VARCHAR(50) NOT NULL DEFAULT 'Individual',
    min_participantes INT NOT NULL DEFAULT 1,
    max_participantes INT NOT NULL DEFAULT 1,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) NOT NULL DEFAULT 'Activa'
) ENGINE=InnoDB;

-- Table: usuario_convocatoria (association)
CREATE TABLE usuario_convocatoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    convocatoria_id INT NOT NULL,
    rol_en_convocatoria VARCHAR(50) NOT NULL,
    estado_validacion VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_uc_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_uc_convocatoria FOREIGN KEY (convocatoria_id) REFERENCES convocatoria(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table: work_group
CREATE TABLE work_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion_texto TEXT,
    contenido_codigo TEXT,
    enlace_repositorio VARCHAR(255),
    puntuacion INT NOT NULL DEFAULT 0,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_id INT NOT NULL,
    convocatoria_id INT NOT NULL,
    CONSTRAINT fk_wg_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_wg_convocatoria FOREIGN KEY (convocatoria_id) REFERENCES convocatoria(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table: comentario_work_group
CREATE TABLE comentario_work_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido TEXT NOT NULL,
    usuario_id INT NOT NULL,
    work_group_id INT NOT NULL,
    fecha_comentario DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comentario_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_comentario_workgroup FOREIGN KEY (work_group_id) REFERENCES work_group(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table: calificacion_work_group
CREATE TABLE calificacion_work_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    calificacion INT NOT NULL,
    usuario_id INT NOT NULL,
    work_group_id INT NOT NULL,
    fecha_calificacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_calificacion_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_calificacion_workgroup FOREIGN KEY (work_group_id) REFERENCES work_group(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Indexes for faster look‑ups (optional)
CREATE INDEX idx_usuario_email ON usuario(correo_electronico);
CREATE INDEX idx_workgroup_convocatoria ON work_group(convocatoria_id);
CREATE INDEX idx_comentario_workgroup ON comentario_work_group(work_group_id);
CREATE INDEX idx_calificacion_workgroup ON calificacion_work_group(work_group_id);
