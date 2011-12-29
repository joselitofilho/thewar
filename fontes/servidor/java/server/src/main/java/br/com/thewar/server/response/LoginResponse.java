/**
 * 
 */
package br.com.thewar.server.response;


/**
 * Class that encapsulate the login response
 * 
 * @author bruno
 * 
 */
public class LoginResponse extends AbstractResponse {

	/**
	 * Create the response of login protocol
	 */
	public LoginResponse() {

		super(LoginResponse.class.getSimpleName().toLowerCase());

	}

	/**
	 * Set the status of response
	 * 
	 * @param status of response
	 */
	public void setStatus(Integer status) {
	
		data.put("status", status);

	}

}
