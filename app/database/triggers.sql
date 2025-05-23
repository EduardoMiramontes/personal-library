-- 1. Capitalizar títulos automáticamente al insertar o actualizar
CREATE OR REPLACE FUNCTION capitalizar_titulo_libro()
RETURNS TRIGGER AS $$
BEGIN
    NEW.titulo := INITCAP(NEW.titulo);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_capitalizar_titulo
BEFORE INSERT OR UPDATE ON LIBRO
FOR EACH ROW
EXECUTE FUNCTION capitalizar_titulo_libro();


-- 2. Capitalizar nombre completo de autores
CREATE OR REPLACE FUNCTION capitalizar_nombre_autor()
RETURNS TRIGGER AS $$
BEGIN
    NEW.nombre_completo := INITCAP(NEW.nombre_completo);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_capitalizar_autor
BEFORE INSERT OR UPDATE ON AUTOR
FOR EACH ROW
EXECUTE FUNCTION capitalizar_nombre_autor();


-- 3. Evitar duplicados por ISBN
CREATE OR REPLACE FUNCTION evitar_duplicados_isbn()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM EDICION WHERE isbn = NEW.isbn
    ) THEN
        RAISE EXCEPTION 'El libro con ISBN % ya existe.', NEW.isbn;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_evitar_duplicados_isbn
BEFORE INSERT ON EDICION
FOR EACH ROW
EXECUTE FUNCTION evitar_duplicados_isbn();


-- 4. Insertar comentario por defecto si está vacío
CREATE OR REPLACE FUNCTION comentario_por_defecto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.comentario IS NULL OR TRIM(NEW.comentario) = '' THEN
        NEW.comentario := 'Sin comentarios';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_comentario_default
BEFORE INSERT ON HISTORIAL
FOR EACH ROW
EXECUTE FUNCTION comentario_por_defecto();


-- 5. Normalizar idioma a minúsculas
CREATE OR REPLACE FUNCTION normalizar_idioma()
RETURNS TRIGGER AS $$
BEGIN
    NEW.idioma := LOWER(NEW.idioma);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_normalizar_idioma
BEFORE INSERT OR UPDATE ON EDICION
FOR EACH ROW
EXECUTE FUNCTION normalizar_idioma();


-- 6. Validar que solo se califique si el estado es "leído"
CREATE OR REPLACE FUNCTION validar_calificacion_en_estado()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estatus <> 'leído' AND NEW.calificación_personal IS NOT NULL THEN
        RAISE EXCEPTION 'Solo puedes calificar libros que ya has leído.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_calificacion_por_estado
BEFORE INSERT ON HISTORIAL
FOR EACH ROW
EXECUTE FUNCTION validar_calificacion_en_estado();


-- 7. Limpiar el ISBN eliminando guiones y espacios
CREATE OR REPLACE FUNCTION limpiar_isbn()
RETURNS TRIGGER AS $$
BEGIN
    NEW.isbn := REGEXP_REPLACE(NEW.isbn, '[^0-9X]', '', 'g');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_limpiar_isbn
BEFORE INSERT OR UPDATE ON EDICION
FOR EACH ROW
EXECUTE FUNCTION limpiar_isbn();