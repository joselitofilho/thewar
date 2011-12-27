/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.server;

import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.zumbits.server.misc.Game;
import org.zumbits.server.misc.PlayerOfGame;
import org.zumbits.server.misc.Room;

import br.com.thewar.servidor.protocol.UpdateGame;

/**
 * Classe principal do servidor.
 * @author zumbits
 */
public class Server extends Thread {
    
    /// Vari�veis staticas
    //End of file
    public static final char EOF = (char) 0x00;
    //Lista de usuários logados <nick, socket>
    public static Hashtable<String, Socket> listUsers;
    //Lista das salas <idRoom, room>
    public static Hashtable<Integer, Room> listRooms;
    //Lista dos jogos <idGame, Game>
    public static Hashtable<Integer, Game> listGames;
    
    ///Vari�veis privadas
    //Socket principal do servidor
    private ServerSocket serverSocket;
    //
    private int _port;
    //TODO: essa estrutura deve ser uma fila circular. E o número de sessão não
    //deve se repitir nos últimos 100 gerados.
    private static int _sessionsId[];

    static {
        _sessionsId = new int[100];
    }

    /**
     * Construtor que recebe uma porta como parâmetro. Iniciando o servidor socket
     * nesta porta.
     *
     * @param port: Porta na qual o servidor irá executar.
     * @throws Exception
     */
    public Server(int port) throws Exception {
        //Armazena a porta selecionada
        _port = port;
        //cria socket de comunica��o com os clientes na porta especificada
        serverSocket = new ServerSocket(port);
        //
        listUsers = new Hashtable<String, Socket>();
        //
        listRooms = new Hashtable<Integer, Room>();
        //
        listGames = new Hashtable<Integer, Game>();
    }

    @Override
    public void run() {
        //Cliente.
        Socket socket;

        //Servidor sempre esperando alguém se conectar.
        while (true) {
            try {
                //TODO: Gerar arquivo de log...
                System.out.println("Waiting for players...");
                //Esperando conex�o de algum cliente
                socket = serverSocket.accept();
                System.out.println("Oh! A player connected! Your socket:" + socket);

                //Thread que tratará tudo este socket enviar ao servidor.
                new Receive(socket);
            } catch (Exception ex) {
                //TODO: Debug...
                //TODO: se a exception for RESET, retirar  o usuário da lista de logados.
                ex.printStackTrace();
            }
        }
    }

    /**
     * Retorna o nick correspondente ao socket. Basicamente é feito uma busca na
     * lista de usuários, procurando o nick correspondente ao socket recebido por
     * parâmetro.
     * 
     * @param socket: Conex�o do usu�rio
     * @return Retorna o nick do usu�rio correspondete ao socket passado, caso n�o
     *         seja encontrado, ser� retornado NULL.
     */
    public static String getIdListUsers(Socket socket) {
        String nick = null;

        //Realiza a busca...
        for (Enumeration e = listUsers.keys(); e.hasMoreElements();) {
            nick = (String) e.nextElement();
            if (socket.equals(listUsers.get(nick))) {
                return nick;
            }
        }

        return nick;
    }

    /**
     * Imprime a lista de usuários conectados
     */
    private static void printListUsers() {
        String nick = null;

        for (Enumeration e = listUsers.keys(); e.hasMoreElements();) {
            nick = (String) e.nextElement();
            System.out.println(nick + " " + listUsers.get(nick));
        }
    }

    /**
     * Verifica se o usuário está em outra sala. Se o usuário estiver em uma outra
     * sala, é retorna TRUE, caso contrário é retornado FALSE.
     *
     * @param idRoom
     * @param nick
     * @return
     */
    private static boolean inOtherRoom(int idRoom, String nick) {
        int id;
        Room r;

        for (Enumeration e = listRooms.keys(); e.hasMoreElements();) {
            id = (Integer) e.nextElement();
            r = listRooms.get(id);

            if (id != idRoom && r.getPos(nick) != -1) {
                return true;
            }
        }

        return false;
    }

    /**
     * Adiciona o usuário na lista de usuários logados.
     * 
     * @param nick: Nick do usuário
     * @param socket: Conexão com o usuário
     * @return Retorna o status da solicitação
     */
    public static void login(String nick, Socket socket) {
        try {
            String xml = "<?xml version='1.0' encoding='UTF-8'?><login><status>";
            int status = -1;

            //TODO: fazer verificacoes no banco
            if (!listUsers.containsKey(nick)) {
                listUsers.put(nick, socket);
                //sucesso
                status = 0;
            } else {
                //usuário logado!!!
                status = 1;
            }

            xml += status + "</status></login>";
            send(socket, xml);

            if (status == 0) {
                updateUsersList(nick, socket);

                for (Enumeration e = listRooms.keys(); e.hasMoreElements();) {
                    updateRoomPlayersList((Integer) e.nextElement());
                }
            }
        } catch (Exception ex) {
            Logger.getLogger(Server.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Remove o usuário da lista de logados.
     *
     * @param nick: Nick do usuário
     * @param socket: Conexão com o usuário
     * @return Retorna o status da solicitação
     */
    public static void logoff(Socket socket) {
        try {
            String xml = "<?xml version='1.0' encoding='UTF-8'?><logoff><status>";
            String nick = getIdListUsers(socket);
            int status = -1;

            if (nick != null) {
                Room r;
                int pos;

                for (Enumeration e = listRooms.keys(); e.hasMoreElements();) {
                    r = listRooms.get((Integer)e.nextElement());
                    pos = r.getPos(nick);

                    if ( pos != -1 )
                    {
                        r.removePlayer( nick );
                    }
                }
                //public static Hashtable<Integer, Room> listRooms;
                //Removendo da lista de usuários...
                listUsers.remove(nick);
                //sucesso
                status = 0;
            } else {
                //usuário não está logado!!!
                status = 1;
            }

            xml += status + "</status></logoff>";
            send(socket, xml);

            if (status == 0) {
                updateUsersList(nick, socket);
            }
        } catch (Exception ex) {
            Logger.getLogger(Server.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Atualiza a lista de usuários.
     *
     * @param nick
     * @param socket
     * @throws Exception
     */
    public static void updateUsersList(String nick, Socket socket) throws Exception {
        String xml = "<?xml version='1.0' encoding='UTF-8'?><usersList>";

        //TODO: Fazer um método para isso?
        for (Enumeration e = listUsers.keys(); e.hasMoreElements();) {
            xml += "<nick>" + (String) e.nextElement() + "</nick>";
        }

        xml += "</usersList>";

        //Envia a mensagem aos usuários.
        sendAll(xml);
    }

    /**
     * Atualiza a lista de usuários de uma sala.
     *
     * @param idRoom
     * @throws Exception
     */
    public static void updateRoomPlayersList(int idRoom) throws Exception {
        Room room = listRooms.get(idRoom);

        if (room != null) {
            Socket socket = null;
            String player = null;
            String i_xml = "";
            String xml = "<roomPlayerList>"
                    + "<room>" + idRoom + "</room>"
                    + "<owner>" + room.getOwner() + "</owner>";

            // Atualiza a lista dos jogadores
            String[] players = room.getListPlayers();

            // Lista os jogadores da sala
            for (int i = 0; i < players.length; i++) {
                if (players[i] != null) {
                    xml += "<player>"
                            + "<pos>" + i + "</pos>"
                            + "<nick>" + players[i] + "</nick>"
                            + "</player>";
                }
            }

            for (Enumeration e = listUsers.keys(); e.hasMoreElements();) {
                player = (String) e.nextElement();
                socket = listUsers.get(player);

                i_xml = xml + "<yours>" + room.getPos(player) + "</yours>"
                        + "</roomPlayerList>";

                send(socket, i_xml);
            }
        }
    }

    /**
     * Envia uma menssagem a um cliente socket.
     *
     * @param socket
     * @param xml
     * @throws Exception
     */
    public static void send(Socket socket, String xml) throws Exception {
        PrintStream out = new PrintStream(socket.getOutputStream());
        out.println(xml + EOF);
        out.flush();

        out = null;
        
        System.out.println("ENVIANDO: " + xml);
    }

    /**
     * Envia uma mensagem para todos clientes sockets conectados.
     *
     * @param xml
     * @throws Exception
     */
    public static void sendAll(String xml) throws Exception {
        Socket s = null;

        for (Enumeration e = listUsers.elements(); e.hasMoreElements();) {
            s = (Socket) e.nextElement();
            send(s, xml);
        }
    }

    /**
     * Envia uma mensagem apenas para os jogadores especificados.
     *
     * @param players
     * @param xml
     * @throws Exception
     */
    public static void sendAll(String[] players, String xml) throws Exception {
        Socket s = null;

        if (players != null) {
            for (String p : players) {
                if ( p != null ) {
                    s = (Socket) listUsers.get(p);
                    send(s, xml);
                }
            }
        }
    }

    /**
     * Ajusta o jogador na sala.
     * 
     * @param idRoom: id da sala
     * @param pos: Posição do jogador na sala
     * @param socket: Conexão com o usuário
     * @return Retorna o status da solicitação
     */
    public static void setPlayer(int idRoom, int pos, Socket socket) throws Exception {
        //recupera o nick na posição da sala
        String xml = "<?xml version='1.0' encoding='UTF-8'?>"
                + "<setPlayer>";

        String nick = getIdListUsers(socket);
        int status = -1;

        //verifica se o usuário está logado
        if (nick != null) {
            Room r;

            if (pos == Room.SET_PLAYER_EXIT_ROOM) {
                r = listRooms.get(idRoom);
                r.replacePlayer(pos, nick);
                listRooms.put(idRoom, r);

                //Sempre sucesso ao realizar saída da sala
                status = Room.SET_PLAYER_SUCCESS;
            } else {

                boolean otherRoom = inOtherRoom(idRoom, nick);

                if (!otherRoom) {
                    r = listRooms.get(idRoom);

                    if (r == null) {
                        r = new Room(idRoom);
                    }

                    status = r.replacePlayer(pos, nick);
                    listRooms.put(idRoom, r);
                } else {
                    //usuário está em outra sala
                    status = Room.SET_PLAYER_OTHER_ROOM;

                    // TODO: para clientes vips ele sai da sala e entra automaticamente na outra..
                }
            }
        } else {
            //usuário não logado!!!
            status = Room.SET_PLAYER_AUTHENTICATE;
        }

        xml += "<status>" + status + "</status>"
                + "</setPlayer>";

        send(socket, xml);

        //Enviar para todos os envolvidos
        if (status == Room.SET_PLAYER_SUCCESS
                || status == Room.SET_PLAYER_OWNER
                || status == Room.SET_PLAYER_SWAP
                || status == Room.SET_PLAYER_OTHER_ROOM) {
            updateRoomPlayersList(idRoom);
        }
    }

    /**
     * Envia uma mensagem ao chat de um outro jogador.
     *
     * @param s_from
     * @param to
     * @param msg
     */
    public static void chat(Socket s_from, String to, String msg) {
        String from = getIdListUsers(s_from);
        String xml = "<?xml version='1.0' encoding='UTF-8'?><chat><from>" + from + "</from>"
                + "<msg>" + msg + "</msg>"
                + "<pvt>" + ((to.equals("")) ? "0" : "1") + "</pvt>"
                + "</chat>";

        if (to.equals("")) {
            try {
                //envia para todos!
                sendAll(xml);
            } catch (Exception ex) {
                Logger.getLogger(Server.class.getName()).log(Level.SEVERE, null, ex);
            }
        } else {
            try {
                Socket s = listUsers.get(to);
                send(s, xml);

                s = listUsers.get(from);
                send(s, xml);
            } catch (Exception ex) {
                Logger.getLogger(Server.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    /**
     * Envia aos cliente de uma sala que o lider da sala iniciou a partida.
     *
     * @param socket
     * @param room
     * @throws Exception
     */
    public static void startGame(Socket socket, int room) throws Exception {
        String xml = "<?xml version='1.0' encoding='UTF-8'?><startGame>"
                + "<room>" + room + "</room>";
        int status = -1;
        String players[] = null;

        Room r = listRooms.get(room);
        Game g = null;
        if (r != null) {
            //TODO: gerar número de sessão!
            //
            int numberSession = generateNewNumberSession();/*Gerar número aleatório não repetido*/
            g = listGames.get(numberSession);
            
            //Sala não criada
            if (g == null) {
                players = r.getListPlayers();
                g = new Game(players, numberSession);

                //Número de jogadores
                if (r.getNumberPlayers() > 2) {
                    //TODO: fazer pelo número de sessão
                    g.init();
                    listGames.put(numberSession, g);

                    if (r != null) {
                        xml += "<numberSession>" + numberSession + "</numberSession>";
                        xml += "<startPlayer>" + g.getStartPlayer() + "</startPlayer>";

                        // Lista os jogadores da sala
                        for (int i = 0; i < players.length; i++) {
                            if (players[i] != null) {
                                xml += "<player>"
                                        + "<pos>" + i + "</pos>"
                                        + "<nick>" + players[i] + "</nick>"
                                        + "<territories>" + g.getTerritoriesPerPlayerList(i) + "</territories>"
                                        + "</player>";
                            }
                        }
                    }

                    status = Game.START_GAME_CREATE_SUCCESS;
                } else {
                    status = Game.START_GAME_CREATE_INVALID_NUMBER_PLAYERS;
                }
            } else {
                status = Game.START_GAME_PREVOUSLY_CREATED;
                //status = Game.START_GAME_UPDATE_SUCCESS;
            }
        } else {
            status = Game.START_GAME_ROOM_NOT_EXIST;
        }

        // Se a sala foi criada corretamente então a mensagem será enviada a todos
        // os participantes. Caso contrário é enviada apenas ao dono da sala.
        if (status == Game.START_GAME_CREATE_SUCCESS && players != null) {
            //Enviar para todos os participantes da sala que o jogo irá começar...
            String i_xml = "";
            for (int i = 0; i < 6; i++) {
                if (players[i] != null) {
                    if (g != null) {
                        i_xml = "<objective>" + g.getObjective( i ) + "</objective>";
                    } else {
                        i_xml = "<objective>0</objective>";
                        status = 99;
                    }
                    i_xml += "<yours>" + r.getPos( players[i] ) + "</yours>";
                    i_xml += "<status>" + status + "</status>"
                        + "</startGame>";

                    send(listUsers.get(players[i]), xml+i_xml);
                }
            }
        } else {
            xml += "<status>" + status + "</status>"
                + "</startGame>";
            send(socket, xml);
        }
    }

    public static void updateGame(Socket socket, int numberSession, int playerPos,
            int quantity, int stateFrom, int stateTo, int turn ) throws Exception {
        String xml = "<?xml version='1.0' encoding='UTF-8'?><updateGame>";
        String[] listPlayers = null;
        Game g = listGames.get(numberSession);

        if ( g != null ) {
            PlayerOfGame playerOfGame = g.getPlayerOfGame(playerPos);

            if ( turn == UpdateGame.UPDATE_GAME_TURN_INIT ) {
                //NOTE: neste caso, o stateFrom e o stateTo são iguas. Por isso o stateTo
                //será ignorado.
                int qtd = g.updateTerritoryAdd( stateFrom, quantity, playerPos );
                xml += "<territory>"
                       + "<id>"+stateFrom+"</id>"
                       + "<quantity>"+qtd+"</quantity>"
                       //TODO: Apenas para não esqucer.. Existem 3 tipos de status: Adicionar, Remover e Conquistar(é passado soldados como parâmetros)
                       + "<status>0</status>" //Apenas adicionado sodados.
                     + "</territory>";
                listPlayers = g.getListPlayer();
            }

            xml += "<numberSoldiersRemained>"+ playerOfGame.getSoldiersInTurn() +"</numberSoldiersRemained>";
            xml += "<playersTurn>"+ playerPos +"</playersTurn>";
            xml += "</updateGame>";
            //Enviar para todos os jogadores do Game...
            sendAll(listPlayers, xml);
        }
    }

    private static int generateNewNumberSession() {
        Random random = new Random();
        int n = random.nextInt(999999)+1;

        return n;
    }

    /**
     * Rotina principal.
     * 
     * @param args
     * @throws Exception
     */
    public static void main(String args[]) throws Exception {
        //Servidor principal
        new Server(1234).start();

        //Servidor da política de segurança.
        //new PolicyServer(1235).start();
    }
}
