package br.com.thewar.server.protocol;

import java.io.IOException;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The War server class game
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Server implements Runnable {

	/**
	 * LOGIN Constant
	 */
	public static String LOGIN = "login";

	/**
	 * LOGOFF constant
	 */
	public static String LOGOFF = "logoff";

	/**
	 * SET_PLAYER constant
	 */
	public static String SET_PLAYER = "setPlayer";

	/**
	 * CHAT constant
	 */
	public static String CHAT = "chat";

	/**
	 * START_GAME constant
	 */
	public static String START_GAME = "startGame";

	/**
	 * UPDATE_GAME constant
	 */
	public static String UPDATE_GAME = "updateGame";

	// Sentinel variable to while block
	private boolean execute;

	// ServerSocker to receive the client connection
	private ServerSocket serverSocket;

	// Sockect with the client
	private Socket socket;

	// Logger class to log the actions
	private static Logger logger;

	/**
	 * Network server of The War game
	 * 
	 * @param port
	 *            of server will be listening
	 */
	public Server(int port) {

		try {

			// Initialize the main variables
			logger = Logger.getLogger("Server initialized!");
			serverSocket = new ServerSocket(port);
			execute = true;

		} catch (IOException e) {

			// Register the action on the log and close the application
			logger.log(Level.SEVERE,
					"error to create the server: " + e.getMessage());
			System.exit(-1);

		}

	}

	/**
	 * The method run
	 */
	public void run() {
		/*
		 * When the sentinel variable is true will execute this block. Case
		 * occur a error launch the exception!
		 */
		while (execute) {

			try {

				// Wait the client connect with the server and log the actions
				logger.log(Level.INFO, "Waiting connection...");
				socket = serverSocket.accept();

				// Log the client connection and transfer the socket to receiver
				// object to treat the conversation
				logger.log(Level.INFO,
						"Client " + socket.getRemoteSocketAddress()
								+ " is now connected!");
				
				// Create a new receiver object to treat this request
				new Receiver(socket).start();

			} catch (IOException e) {

				// Log the exception
				logger.log(Level.SEVERE, e.getMessage());

			}

		}

	}

	/**
	 * Method that send a message to a list of sockets
	 * 
	 * @param message to send
	 * @param sockets of session
	 */
	public static void sendMessage(String message, List<Socket> sockets) {

		if(sockets != null){
			
			for (Socket socket : sockets) {
				
				try {
					
					PrintStream printStream = new PrintStream(socket.getOutputStream());
					printStream.print(message);
					printStream.flush();
					
				} catch (IOException e) {
					
					// Log the exception
					logger.log(Level.SEVERE, e.getMessage());
					
				}
				
			}
			
		}
		
	}
}
