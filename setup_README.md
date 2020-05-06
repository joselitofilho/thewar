Foram criados:
- Docker network chamada "docker-network":
  $ docker network create docker-network
- screen session para executar o container docker do jogowar
  $ docker run --name jogowar --rm -p 8080:8080 --network docker-network -v $(pwd):/app -it ricardogpsf/jogowar:v1 bash -c 'cd /app && ./start_game.sh'
- screen session para executar o nginx
  Executar dentro da pasta nginx que foi criada:
  $ docker run --rm --name nginx -p 80:80 --network docker-network -v $(pwd)/reverse-proxy.conf:/etc/nginx/conf.d/reverse-proxy.conf nginx:1.17.9
- Lembrar de modificar a url de acesso ao Google Maps api para adicionar a key do usuario da api. Existe um comentario nessa parte do codigo html.

Para listar os screen sessions: 
  $ screen -ls
Para acessar um screen session:
  $ screen -r id_do_screen_session

Pasta ngix deve ser criada contendo um arquivo chamado "reverse-proxy.conf" com o seguinte conteudo:
server {
        listen 80;
        server_name jogowar.com.br www.jogowar.com.br;
        location / {
                proxy_pass http://jogowar:9092/;
        }
}

