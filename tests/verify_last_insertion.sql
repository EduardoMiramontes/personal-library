-- Último libro insertado
SELECT * FROM LIBRO ORDER BY id_libro DESC LIMIT 1;

-- Autor relacionado
SELECT A.* FROM AUTOR A
JOIN LIBRO_AUTOR LA ON A.id_autor = LA.id_autor
WHERE LA.id_libro = (SELECT MAX(id_libro) FROM LIBRO);

-- Edición relacionada
SELECT * FROM EDICION
WHERE id_libro = (SELECT MAX(id_libro) FROM LIBRO);

-- Formato de la edición
SELECT F.* FROM FORMATO F
JOIN EDICION E ON E.id_formato = F.id_formato
WHERE E.id_libro = (SELECT MAX(id_libro) FROM LIBRO);

-- Categorías del libro
SELECT C.* FROM CATEGORIA C
JOIN LIBRO_CATEGORIA LC ON C.id_categoria = LC.id_categoria
WHERE LC.id_libro = (SELECT MAX(id_libro) FROM LIBRO);