.mode lines

# Desafios

SELECT datetime(date('2020-06-19'), time('23:00:00'));
SELECT datetime(date('2020-06-20'), time('22:59:59'));

DELETE FROM DesafiosEmAndamento;
DELETE FROM DesafiosEmAndamento WHERE terminaEm < datetime(date('now'), time('22:59:59'));
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


###### Testes desafios
DELETE FROM DesafiosEmAndamento;
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (16, 'Prince', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (17, 'Lucy', 0, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));
INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (19, 'Lutz', 1, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));

INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(2, 16, 'Lucy', '2020-07-02 15:00:00');


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
SELECT * FROM PontuacaoEventos WHERE idUsuario = 2 AND idEvento = ( SELECT CAST(valor AS INTEGER) FROM Configuracoes WHERE chave = 'id_evento_atual' ); 
INSERT INTO PontuacaoEventos(idUsuario, pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido, idEvento) VALUES (2, 150, 1, 1, 0, 1);  # (first time)
UPDATE  Pontuacao SET pontos = pontos + 150 WHERE idUsuario = 2;  # (or just update)
INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador, data) VALUES(2, 16, 'Lucy', '2020-07-02 15:00:00');



update pontuacaoeventos set pontos = 200 where id = 10;
SELECT u.nome, p.pontos, p.quantidadeDePartidas, p.quantidadeDeVitorias, p.quantidadeDestruido, p.atualizado
                  FROM PontuacaoEventos p 
                  JOIN Eventos e ON e.id = p.idEvento
                  JOIN Usuarios u ON u.id = p.idUsuario
                 WHERE e.id = 0
              ORDER BY pontos+quantidadeDePartidas+quantidadeDeVitorias+quantidadeDestruido+atualizado 
                  DESC;