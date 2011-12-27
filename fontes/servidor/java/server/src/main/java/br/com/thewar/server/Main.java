package br.com.thewar.server;

import java.util.logging.Level;
import java.util.logging.Logger;

import br.com.thewar.server.protocol.Server;

/**
 * Main class of The War game
 * @author Bruno Lopes Alcantara Batista
 *
 */
public class Main {
	
	public static void main(String[] args) {
		
		// Log object to log events
		Logger logger = Logger.getLogger(Main.class.getName());
		
		try{
			
			// Start the server
			Server server = new Server(1234);
			server.run();
			
		} catch (Exception e) {
			
			// Register the action on the log and close the application
			logger.log(Level.SEVERE, "Error to initialize the game: " + e.getMessage());
			System.exit(-1);
			
		}
		
	}
	
}
