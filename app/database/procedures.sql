-- Procedimiento: insertar libro completo
CREATE OR REPLACE PROCEDURE insertar_libro_completo(
    _titulo VARCHAR,
    _descripcion TEXT,
    _numero_paginas INT,
    _portada TEXT,
    _nombre_autor VARCHAR,
    _pais_autor VARCHAR,
    _nacimiento DATE,
    _editorial VARCHAR,
    _fecha_pub DATE,
    _idioma VARCHAR,
    _isbn VARCHAR,
    _formato_id INT,
    _categorias INT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    id_libro INT;
    id_autor INT;
    cat_id INT;
BEGIN
    INSERT INTO LIBRO (titulo, descripcion, numero_paginas, portada)
    VALUES (_titulo, _descripcion, _numero_paginas, _portada)
    RETURNING LIBRO.id_libro INTO id_libro;

    id_autor := get_or_create_autor(_nombre_autor, _pais_autor, _nacimiento);

    INSERT INTO LIBRO_AUTOR (id_libro, id_autor) VALUES (id_libro, id_autor);

    INSERT INTO EDICION (id_libro, id_formato, editorial, fecha_publicación, idioma, isbn)
    VALUES (id_libro, _formato_id, _editorial, _fecha_pub, _idioma, _isbn);

    FOREACH cat_id IN ARRAY _categorias LOOP
        INSERT INTO LIBRO_CATEGORIA (id_libro, id_categoria) VALUES (id_libro, cat_id);
    END LOOP;
END;
$$;


-- Procedimientos auxiliares
CREATE OR REPLACE PROCEDURE registrar_estado_lectura(
    _id_libro INT,
    _estatus VARCHAR,
    _calificacion SMALLINT,
    _comentario TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO HISTORIAL (
        id_libro, estatus, calificación_personal, comentario
    )
    VALUES (
        _id_libro, _estatus, _calificacion, _comentario
    );
END;
$$;

CREATE OR REPLACE PROCEDURE actualizar_estado_lectura(
    _id_historial INT,
    _nuevo_estatus VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE HISTORIAL
    SET estatus = _nuevo_estatus
    WHERE id_historial = _id_historial;
END;
$$;

CREATE OR REPLACE PROCEDURE marcar_leido_hoy(
    _id_libro INT,
    _calificacion SMALLINT,
    _comentario TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO HISTORIAL (
        id_libro, estatus, calificación_personal, fecha_registro, comentario
    )
    VALUES (
        _id_libro, 'leído', _calificacion, CURRENT_DATE, _comentario
    );
END;
$$;