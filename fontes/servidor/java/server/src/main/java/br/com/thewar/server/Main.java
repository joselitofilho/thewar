package br.com.thewar.server;

import java.util.logging.Level;
import java.util.logging.Logger;

import org.hibernate.Session;

import br.com.thewar.server.dao.HibernateUtil;
import br.com.thewar.server.model.Login;
import br.com.thewar.server.model.User;
import br.com.thewar.server.protocol.Server;

/**
 * Main class of The War game
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Main {

	public static void main(String[] args) {

		// Log object to log events
		Logger logger = Logger.getLogger(Main.class.getName());

		try {
			
			User admin = new User("admin", "admin","admin@admin.com", "admin");
			
			Login adminLogin = new Login("admin", "admin", admin);
			
			Session session = HibernateUtil.getSessionFactory().openSession();
			
			session.beginTransaction().begin();
			session.save(admin);
			session.save(adminLogin);
			session.beginTransaction().commit();
			
			// Start the server
			Server server = new Server(1234);
			server.run();

		} catch (Exception e) {

			// Register the action on the log and close the application
			logger.log(Level.SEVERE,
					"Error to initialize the game: " + e.getMessage());
			e.printStackTrace();
			System.exit(-1);

		}

	}

}
