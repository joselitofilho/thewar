package br.com.thewar.server.protocol;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Hashtable;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Server implements Runnable{

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
	 * 
	 */
	private boolean execute;
	
	/**
	 * 
	 */
	private ServerSocket serverSocket;
	
	/**
	 * 
	 */
	private Socket socket;
	
	/**
	 * 
	 */
	private static Hashtable<String, Socket> loggedUser;
	
	/**
	 * 
	 */
	private static Logger logger = Logger.getLogger("Servidor");
	
	public Server() {
		
		try {
			
			serverSocket = new ServerSocket(1234);
			
			execute = true;
			
			loggedUser = new Hashtable<String, Socket>();
			
		} catch (IOException e) {
			
			// TODO Auto-generated catch block
			e.printStackTrace();
			
		}
		
	}
	
	
	public void run() {
		
		while(execute){
			
			try{
				
				logger.log(Level.INFO, "Waiting connection...");
				
				socket = serverSocket.accept();
				
				logger.log(Level.INFO, "Waiting connection...");
				
				new Receiver(socket).run();
				
			} catch (IOException e) {
				
				// TODO: handle exception
				e.printStackTrace();
				
				logger.log(Level.SEVERE, e.getMessage());
				
			}
			
		}
		
	}

}
