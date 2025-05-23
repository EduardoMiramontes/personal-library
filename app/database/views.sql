-- Vista: libros leídos con fecha y calificación
CREATE OR REPLACE VIEW libros_leidos AS
SELECT
    L.id_libro,
    L.titulo,
    H.fecha_registro,
    H.calificación_personal,
    H.comentario
FROM HISTORIAL H
JOIN LIBRO L ON H.id_libro = L.id_libro
WHERE H.estatus = 'leído';


-- Vista: libros por autor
CREATE OR REPLACE VIEW libros_por_autor AS
SELECT
    A.nombre_completo AS autor,
    L.titulo,
    L.id_libro
FROM LIBRO L
JOIN LIBRO_AUTOR LA ON L.id_libro = LA.id_libro
JOIN AUTOR A ON LA.id_autor = A.id_autor;


-- Vista: libros por categoría
CREATE OR REPLACE VIEW libros_por_categoria AS
SELECT
    C.nombre_categoria,
    L.titulo,
    L.id_libro
FROM LIBRO L
JOIN LIBRO_CATEGORIA LC ON L.id_libro = LC.id_libro
JOIN CATEGORIA C ON LC.id_categoria = C.id_categoria;


-- Vista: estado actual de lectura
CREATE OR REPLACE VIEW estado_lectura_actual AS
SELECT
    H.id_historial,
    L.titulo,
    H.estatus,
    H.calificación_personal,
    H.fecha_registro
FROM HISTORIAL H
JOIN LIBRO L ON H.id_libro = L.id_libro
WHERE H.fecha_registro = (
    SELECT MAX(H2.fecha_registro)
    FROM HISTORIAL H2
    WHERE H2.id_libro = H.id_libro
);


-- Vista: resumen de libros por estatus
CREATE OR REPLACE VIEW resumen_por_estatus AS
SELECT
    estatus,
    COUNT(*) AS total
FROM HISTORIAL
GROUP BY estatus;


-- Vista: libros sin comenzar
CREATE OR REPLACE VIEW libros_sin_comenzar AS
SELECT L.*
FROM LIBRO L
WHERE NOT EXISTS (
    SELECT 1 FROM HISTORIAL H
    WHERE H.id_libro = L.id_libro
);