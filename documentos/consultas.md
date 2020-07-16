.mode lines

# Desafios

SELECT datetime(date('2020-06-19'), time('23:00:00'));
SELECT datetime(date('2020-06-20'), time('22:59:59'));

DELETE FROM DesafiosEmAndamento;
DELETE FROM DesafiosEmAndamento WHERE terminaEm < datetime(date('now'), time('22:59:59'));
DELETE FROM DesafiosEmAndamento WHERE terminaEm > datetime(date('now'), time('23:00:00'));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (1, 'Prince', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (2, 'Lucy', 0, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (3, 'Lutz', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59'))); 
SELECT * FROM DesafiosEmAndamento;
SELECT * FROM DesafiosEmAndamento WHERE datetime('now') BETWEEN iniciaEm AND terminaEm;
SELECT * FROM DesafiosEmAndamento WHERE datetime('now', '+1.43 hours') BETWEEN iniciaEm AND terminaEm;
SELECT json_extract(infos, '$.desafio.id') FROM DesafiosEmAndamento;
SELECT json_extract(infos, '$.desafio.id'),
       iniciaEm AS ini,
       datetime(iniciaEm, '+1 DAY') AS fim
  FROM DesafiosEmAndamento;

DELETE FROM DesafiosConcluidos;
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador) VALUES (1, 1, 'Häyhä');
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES (1, 2, 'Lucy', datetime('now', '+1 DAY'));
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador) VALUES ( (SELECT id FROM Usuarios WHERE nome='t1'), 1, 'Häyhä');
SELECT dc.*, u.nome FROM DesafiosConcluidos dc JOIN Usuarios u ON u.id = dc.idUsuario ;
SELECT dc.*, u.nome FROM DesafiosConcluidos dc JOIN Usuarios u ON u.id = dc.idUsuario WHERE u.nome = 't1' ;

###### Desafios do dia que foram concluídos pelo usuários.
SELECT da.idDesafio FROM DesafiosEmAndamento da JOIN DesafiosConcluidos dc ON dc.idDesafio = da.idDesafio JOIN Usuarios u ON u.id = dc.idUsuario WHERE dc.data BETWEEN da.iniciaEm AND da.terminaEm AND u.nome = 't1';


###### Limpar desafios
DELETE FROM desafiosEmAndamento;
DELETE FROM sqlite_sequence where name='DesafiosEmAndamento';


###### Testes desafios
DELETE FROM DesafiosEmAndamento;
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (16, 'Prince', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (17, 'Lucy', 0, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (19, 'Lutz', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));

INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(2, 16, 'Lucy', '2020-07-02 15:00:00');


###### Testes desafios em andamento
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 21, 'Mad Jack', datetime('now'));
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 30, 'Prince', datetime('now'));

INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm, ordem) VALUES (30, 'Prince', 0, '2020-07-15 10:00:00', '2020-07-16 09:59:59', 1);
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm, ordem) VALUES (1, 'Lucy', 0, '2020-07-15 10:00:00', '2020-07-16 09:59:59', 2);
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm, ordem) VALUES (22, 'Kratos', 0, '2020-07-15 10:00:00', '2020-07-16 09:59:59', 3);

SELECT * FROM DesafiosEmAndamento ORDER BY apenasDoador DESC, iniciaEm, ordem ;
SELECT * FROM DesafiosEmAndamento WHERE datetime('now') BETWEEN iniciaEm AND terminaEm ORDER BY apenasDoador DESC, iniciaEm, ordem ;

SELECT da.idDesafio
  FROM DesafiosEmAndamento da 
  JOIN DesafiosConcluidos dc ON dc.idDesafio = da.idDesafio 
  JOIN Usuarios u ON u.id = dc.idUsuario 
 WHERE dc.data BETWEEN da.iniciaEm AND da.terminaEm AND datetime('now') BETWEEN da.iniciaEm AND da.terminaEm AND  u.nome = 't1';


# Doações

###### Limpar doações
DELETE FROM Doacoes WHERE valor > -1;

###### Meta de doações
INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('meta_doacao', '300');

###### Inserir uma doação
INSERT INTO Doacoes(idUsuario, valor) VALUES (2, 20);


# Eventos
INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('id_evento_atual', 1);
INSERT INTO Eventos (id, nome, iniciaEm, terminaEm) VALUES (1, 'Guerra Mundia #1', datetime('now','start of month','23:00:00'), datetime('now','start of month','22:59:59','+1 month','-1 day'));

###### Pontuação dos eventos
INSERT INTO PontuacaoEventos(idUsuario, pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido, idEvento) VALUES (2, 150, 1, 1, 0, 1);
UPDATE  Pontuacao SET pontos = pontos + 150 WHERE idUsuario = 2;
UPDATE  PontuacaoEventos SET pontos = pontos + 150 WHERE idUsuario = 2;


# SELECT da.idDesafio
#   FROM DesafiosEmAndamento da
#  WHERE da.iniciaEm >= datetime(date('now', '-1 DAY'), time('23:00:00'))
#    AND da.terminaEm <= datetime(date('now'), time('22:59:59'))
#    AND da.idDesafio NOT IN ( SELECT dc.idDesafio
#                                FROM DesafiosConcluidos dc
#                                JOIN Usuarios u ON u.id = dc.idUsuario
#                               WHERE dc.data BETWEEN da.iniciaEm AND da.terminaEm
#                                 AND u.nome = ? );


# Ações rápidas

###### Criar um evento
INSERT INTO Eventos (id, nome, iniciaEm, terminaEm) VALUES (1, 'Guerra Mundia #1', datetime('2020-07-01 23:00:00'), datetime('2020-07-31 22:59:59'));
INSERT INTO pontuacaoeventos(idUsuario, idEvento) SELECT id, 1 FROM usuarios;
INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('id_evento_atual', 1);

###### Se der merda no desafio de alguém.
SELECT * FROM PontuacaoEventos WHERE idUsuario = 1 AND idEvento = ( SELECT CAST(valor AS INTEGER) FROM Configuracoes WHERE chave = 'id_evento_atual' );
INSERT INTO PontuacaoEventos(idUsuario, pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido, idEvento) VALUES (2, 150, 1, 1, 0, 1);  # (first time)
UPDATE  Pontuacao SET pontos = pontos + 350 WHERE idUsuario = 1;  # (or just update)
UPDATE  PontuacaoEventos SET pontos = pontos + 350 WHERE idUsuario = 1 AND idEvento = 1;  # (or just update)
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(26, 3, 'Mad Jack', '2020-07-02 00:47:12');


SELECT * FROM DesafiosEmAndamento ORDER BY iniciaEm;
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 3, 'Bradley', datetime('now'));
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 2, 'Winters', datetime('now'));
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 8, 'Major', datetime('now'));
UPDATE  Pontuacao SET quantidadeDePartidas = quantidadeDePartidas + 1, quantidadeDeVitorias = quantidadeDeVitorias + 1, pontos = pontos + 100 WHERE idUsuario = 1;
UPDATE  PontuacaoEventos SET quantidadeDePartidas = quantidadeDePartidas + 1, quantidadeDeVitorias = quantidadeDeVitorias + 1, pontos = pontos + 100 WHERE idUsuario = 1 AND idEvento = 1;

INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(1, 27, 'Lutz', datetime('now'));
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(26, 2, 'Winters', datetime('now'));
UPDATE  Pontuacao SET pontos = pontos + 250 WHERE idUsuario = 26;
UPDATE  PontuacaoEventos SET pontos = pontos + 250 WHERE idUsuario = 26 AND idEvento = 1;


update pontuacaoeventos set pontos = 200 where id = 10;
SELECT u.nome, p.pontos, p.quantidadeDePartidas, p.quantidadeDeVitorias, p.quantidadeDestruido, p.atualizado
                  FROM PontuacaoEventos p 
                  JOIN Eventos e ON e.id = p.idEvento
                  JOIN Usuarios u ON u.id = p.idUsuario
                 WHERE e.id = 0
              ORDER BY pontos+quantidadeDePartidas+quantidadeDeVitorias+quantidadeDestruido+atualizado 
                  DESC;