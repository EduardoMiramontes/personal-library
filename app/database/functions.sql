-- Función auxiliar: obtener o insertar autor
CREATE OR REPLACE FUNCTION get_or_create_autor(
    _nombre_completo VARCHAR,
    _pais VARCHAR,
    _fecha_nac DATE
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    _id INT;
BEGIN
    SELECT id_autor INTO _id
    FROM AUTOR
    WHERE LOWER(nombre_completo) = LOWER(_nombre_completo);

    IF _id IS NULL THEN
        INSERT INTO AUTOR (nombre_completo, pais_origen, fecha_nacimiento)
        VALUES (_nombre_completo, _pais, _fecha_nac)
        RETURNING id_autor INTO _id;
    END IF;

    RETURN _id;
END;
$$;