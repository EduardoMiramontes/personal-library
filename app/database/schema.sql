-- Tabla: LIBRO
CREATE TABLE LIBRO (
    id_libro INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    titulo VARCHAR(255),
    descripcion TEXT,
    numero_paginas INT,
    portada VARCHAR(2083) -- URL
);

-- Tabla: AUTOR
CREATE TABLE AUTOR (
    id_autor INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre_completo VARCHAR(255),
    pais_origen VARCHAR(60),
    fecha_nacimiento DATE,
    fecha_muerte DATE
);

-- Tabla: FORMATO
CREATE TABLE FORMATO (
    id_formato INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre_formato VARCHAR(100)
);

-- Tabla: CATEGORÍA
CREATE TABLE CATEGORIA (
    id_categoria INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre_categoria VARCHAR(100)
);

-- Tabla: EDICIÓN
CREATE TABLE EDICION (
    id_libro INT,
    id_formato INT,
    editorial VARCHAR(100),
    fecha_publicación DATE,
    idioma VARCHAR(50),
    isbn VARCHAR(20),
    PRIMARY KEY (id_libro, id_formato),
    FOREIGN KEY (id_libro) REFERENCES LIBRO(id_libro),
    FOREIGN KEY (id_formato) REFERENCES FORMATO(id_formato)
);

-- Tabla: HISTORIAL
CREATE TABLE HISTORIAL (
    id_historial INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_libro INT NOT NULL,
    estatus VARCHAR(20) CHECK (estatus IN ('leído', 'leyendo', 'sin comenzar', 'abandonado')),
    calificación_personal SMALLINT CHECK (calificación_personal BETWEEN 1 AND 10),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    comentario TEXT,
    FOREIGN KEY (id_libro) REFERENCES LIBRO(id_libro)
);

-- Tabla: LIBRO_AUTOR
CREATE TABLE LIBRO_AUTOR (
    id_libro INT,
    id_autor INT,
    PRIMARY KEY (id_libro, id_autor),
    FOREIGN KEY (id_libro) REFERENCES LIBRO(id_libro),
    FOREIGN KEY (id_autor) REFERENCES AUTOR(id_autor)
);

-- Tabla: LIBRO_CATEGORÍA
CREATE TABLE LIBRO_CATEGORIA (
    id_libro INT,
    id_categoria INT,
    PRIMARY KEY (id_libro, id_categoria),
    FOREIGN KEY (id_libro) REFERENCES LIBRO(id_libro),
    FOREIGN KEY (id_categoria) REFERENCES CATEGORÍA(id_categoria)
);


