/**
 * 
 */
package br.com.thewar.server.response;


/**
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

	public void setStatus(Integer status) {
	
		data.put("status", status);

	}

}
