.mode lines

# Desafios

SELECT datetime(date('now'), time('23:00:00'));

DELETE FROM DesafiosEmAndamento;
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm) VALUES (10, 'Häyhä', 1, datetime(date('now'), time('23:00:00')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm) VALUES (30, 'Lucy', 0, datetime(date('now'), time('23:00:00')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm) VALUES (2, 'Reisch', 1, datetime(date('now'), time('23:00:00'))); 
SELECT * FROM DesafiosEmAndamento;
SELECT json_extract(infos, '$.desafio.id') FROM DesafiosEmAndamento;
SELECT json_extract(infos, '$.desafio.id'),
       iniciaEm AS ini,
       datetime(iniciaEm, '+1 DAY') AS fim
  FROM DesafiosEmAndamento;

DELETE FROM DesafiosConcluidos;
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador) VALUES (1, 10, 'Häyhä');
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES (1, 2, 'Lucy', datetime('now', '+1 DAY'));
SELECT dc.*, u.nome FROM DesafiosConcluidos dc JOIN Usuarios u ON u.id = dc.idUsuario ;
SELECT dc.*, u.nome FROM DesafiosConcluidos dc JOIN Usuarios u ON u.id = dc.idUsuario WHERE u.nome = 't1' ;

###### Desafios do dia que foram concluídos pelo usuários.
SELECT * FROM DesafiosEmAndamento da JOIN DesafiosConcluidos dc ON dc.idDesafio = da.idDesafio JOIN Usuarios u ON u.id = dc.idUsuario WHERE dc.data BETWEEN da.iniciaEm AND datetime(da.iniciaEm, '+1 DAY') AND u.nome = 't1';