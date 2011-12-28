package br.com.thewar.servidor;

import java.io.IOException;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Hashtable;
import java.util.logging.Level;
import java.util.logging.Logger;

import br.com.thewar.servidor.protocol.Login;
import br.com.thewar.servidor.protocol.Login.CodigoResposta;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.DomDriver;

public class Servidor implements Runnable {

	/**
	 * End of file
	 */
	public static final char EOF = (char) 0x00;
	/**
	 * 
	 */
	public static String LOGIN = "login";
	/**
	 * 
	 */
	public static String LOGOFF = "logoff";
	/**
	 * 
	 */
	public static String SET_PLAYER = "setPlayer";
	/**
	 * 
	 */
	public static String CHAT = "chat";
	/**
	 * 
	 */
	public static String START_GAME = "startGame";
	/**
	 * 
	 */
	public static String UPDATE_GAME = "updateGame";
	
	/**
	 * @throws IOException 
	 * 
	 */
	public Servidor() throws IOException
	{
		rodar = true;
		serverSocket = new ServerSocket(1234);
		//
		xstream = new XStream(new DomDriver());
		//
		listaUsuariosLogados = new Hashtable<String, Socket>();
	}
	
	@Override
	public void run() {
		Socket socket;
		
		while(rodar)
		{
			try {
	            logger.log(Level.INFO, "Esperando algu�m conectar-se...");
	            //Esperando conex�o de algum cliente
	            socket = serverSocket.accept();
	            logger.log(Level.INFO, "Algu�m conectou. Seu Socket:" + socket);
	
	            // Agora passa a bola para algu�m tratar o recebimento...
	            new Gerenciador(socket).start();
	        } catch (Exception ex) {
	            ex.printStackTrace();
	            logger.log(Level.SEVERE, ex.getMessage());
	        }
		}
	}
	
	/**
	 * 
	 * @param loginXml
	 */
	public static void ProcessarLogin(Socket socket, String loginXml) {
		try {
			Login loginXstream = (Login)xml2object(loginXml, Login.class, LOGIN);
			
			String xml = "<?xml version='1.0' encoding='UTF-8'?><login><status>";
			CodigoResposta status = Login.CodigoResposta.DESCONHECIDO;
			String nick = loginXstream.getNick();

			// TODO: Fazer verifica��es no banco.
			if (!listaUsuariosLogados.containsKey(nick)) {
				// Sucesso
				listaUsuariosLogados.put(nick, socket);
				status = Login.CodigoResposta.SUCESSO;
			} else {
				// Usu�rio logado!!!
				status = Login.CodigoResposta.USUARIO_JA_ESTA_LOGADO;
			}

			xml += status.Codigo() + "</status></login>";
			send(socket, xml);

			// Atualizando a lista de usuários...
			// if (status == Login.CodigoResposta.SUCESSO) {
			// updateUsersList(nick, socket);
			//
			// for (Enumeration e = listRooms.keys(); e.hasMoreElements();) {
			// updateRoomPlayersList((Integer) e.nextElement());
			// }
			// }
		} catch (Exception ex) {
			logger.log(Level.SEVERE, null, ex);
		}
	}
	
	/**
	 * Converte um xml em uma instância de classe correspondente através da
	 * biblioteca xstream.
	 * 
	 * @param xml
	 * @param type
	 * @return
	 */
	private static Object xml2object(String xml, Class tipo, String nome) {
		xstream.alias(nome, tipo);
		return xstream.fromXML(xml);
	}

	/**
	 * 
	 * @param socket
	 * @param xml
	 * @throws Exception
	 */
	public static void send(Socket socket, String xml) throws Exception {
		logger.log(Level.INFO, "Enviando: " + xml);
		PrintStream out = new PrintStream(socket.getOutputStream());
		//out.print(xml + EOF);
		out.print(xml);
		out.flush();

		out = null;
	}

	private boolean rodar;
	//
	private ServerSocket serverSocket;
	//
	private static XStream xstream;
	//
	private static Hashtable<String, Socket> listaUsuariosLogados;
	//
	private static Logger logger = Logger.getLogger("Servidor");
}