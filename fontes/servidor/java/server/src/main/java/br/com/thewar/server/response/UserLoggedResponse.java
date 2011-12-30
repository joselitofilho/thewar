package br.com.thewar.server.response;

/**
 * Class that encapsulate the login response
 * 
 * @author Joselito Viveiros - joselitofilhoo@gmail.com
 * 
 */
public class UserLoggedResponse extends AbstractResponse {

	/**
	 * Create the response of user logged protocol
	 */
	public UserLoggedResponse() {

		super(UserLoggedResponse.class.getSimpleName().toLowerCase());

	}
	
	/**
	 * Set the nick of response
	 * 
	 * @param nick of response
	 */
	public void setNick(String nick) {
	
		data.put("nick", nick);

	}
}
