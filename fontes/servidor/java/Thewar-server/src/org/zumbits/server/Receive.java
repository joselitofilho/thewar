/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.server;

import br.com.thewar.servidor.protocol.Chat;
import br.com.thewar.servidor.protocol.Login;
import br.com.thewar.servidor.protocol.SetPlayer;
import br.com.thewar.servidor.protocol.StartGame;
import br.com.thewar.servidor.protocol.UpdateGame;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.DomDriver;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.xml.sax.SAXParseException;

/**
 *
 * @author zumbits
 */
public class Receive extends Thread {

    //
    public static String LOGIN = "login";
    public static String LOGOFF = "logoff";
    public static String SET_PLAYER = "setPlayer";
    public static String CHAT = "chat";
    public static String START_GAME = "startGame";
    public static String UPDATE_GAME = "updateGame";
    //
    private Socket socket;
    private InetAddress iClient;
    private BufferedReader in;
    //
    private XStream xstream;

    public Receive(Socket socket) {
        try {
            //
            this.socket = socket;
            //
            this.iClient = socket.getInetAddress();
            //
            this.xstream = new XStream(new DomDriver());

            //inicia o recebimento
            start();
        } catch (Exception ex) {
            //TODO: Debug
            ex.printStackTrace();
        }
    }

    @Override
    public void run() {
        try {
        	//DataInputStream inn = new DataInputStream(socket.getInputStream());
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            
            String xml;// = inn.readUTF();
            
            System.out.println("esperando recebimento...");

            while ((xml = in.readLine()) != null) {
                process(xml.trim());
            }
        } catch (SAXParseException ex) {
            if ( ex.getMessage().equals("Premature end of file.") )
            {
                Server.logoff(socket);
            }
        } catch (Exception ex) {
            //TODO: Debug...
            ex.printStackTrace();
            System.out.println("2 =(");
        }
    }

    //Processa a informação recebida
    private void process(String xml) throws Exception {
    	System.out.println("Alow ");
        DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = fact.newDocumentBuilder();
        Document doc = builder.parse(new ByteArrayInputStream(xml.getBytes()));
        Node node = doc.getDocumentElement();
        String root = node.getNodeName();
        int status = -1;

        System.out.println("xml: " + xml);

        //O xml passado como parâmetro será alterado para o xml de resposta
        if (root.equals(LOGIN)) {
            Login l = login(xml);
            Server.login(l.getNick().trim(), socket);
        } else if (root.equals(LOGOFF)) {
            Server.logoff(socket);
        } else if (root.equals(SET_PLAYER)) {
            SetPlayer r = setPlayer(xml);
            Server.setPlayer(r.getRoom(), r.getPos(), socket);
        } else if (root.equals(CHAT)) {
            Chat c = chat(xml);
            Server.chat(this.socket, c.getTo(), c.getMsg());
        } else if (root.equals(START_GAME)) {
            StartGame sg = startGame(xml);
            Server.startGame(socket, sg.getRoom());
        } else if (root.equals(UPDATE_GAME)) {
            UpdateGame ug = updateGame(xml);
            Server.updateGame(socket, ug.getNumberSession(), ug.getPlayer(),
                    ug.getQuantity(), ug.getStateFrom(), ug.getStateTo(),
                    ug.getType());
        }
    }

    private Login login(String xml) {
        xstream.alias(LOGIN, Login.class);
        return (Login) xstream.fromXML(xml);
    }

    private SetPlayer setPlayer(String xml) {
        xstream.alias(SET_PLAYER, SetPlayer.class);
        return (SetPlayer) xstream.fromXML(xml);
    }

    private Chat chat(String xml) {
        xstream.alias(CHAT, Chat.class);
        return (Chat) xstream.fromXML(xml);
    }

    private StartGame startGame(String xml) {
        xstream.alias(START_GAME, StartGame.class);
        return (StartGame) xstream.fromXML(xml);
    }

    private UpdateGame updateGame(String xml) {
        xstream.alias(UPDATE_GAME, UpdateGame.class);
        return (UpdateGame) xstream.fromXML(xml);
    }

    public void close() throws Exception {
        socket.close();
    }
}
