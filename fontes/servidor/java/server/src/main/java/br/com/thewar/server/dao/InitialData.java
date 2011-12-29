/**
 * 
 */
package br.com.thewar.server.dao;

import br.com.thewar.server.model.Login;
import br.com.thewar.server.model.User;

/**
 * Temporary clas to fill the database
 * 
 * @author Bruno Lopes Alcantara Batista
 *
 */
public class InitialData {

	
	/**
	 * 
	 */
	private InitialData() {
		
	}
	
	public static void fill() {
		
		User bruno = new User("Bruno", "Lopes", "brunolopesjn@gmail.com", "brunolopesjn");
		User joselito = new User("Joselito", "Filho", "joselitofilhoo@gmail.com", "");
		
		Login brunoLogin = new Login("bruno", "1234", bruno);
		Login joselitoLogin = new Login("joselito", "1234", joselito);
		
		UserDAO.getInstance().save(bruno);
		UserDAO.getInstance().save(joselito);
		
		LoginDAO.getInstance().save(brunoLogin);
		LoginDAO.getInstance().save(joselitoLogin);
		
	}
	
}
