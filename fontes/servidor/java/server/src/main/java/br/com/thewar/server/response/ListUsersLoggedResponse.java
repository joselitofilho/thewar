/**
 * 
 */
package br.com.thewar.server.response;

import java.util.List;

/**
 * Class that encapsulate the list users logged response
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class ListUsersLoggedResponse extends AbstractResponse {


	/**
	 * Class that encapsulate the list users logged response 
	 */
	public ListUsersLoggedResponse() {

		// Call the super class constructor passing the class name
		super(ListUsersLoggedResponse.class.getSimpleName().toLowerCase());

	}
	
	/**
	 * Set the list of users
	 * 
	 * @param users list
	 */
	public void setUsers(List<String> users){
		
		data.put("listusers", users);
		
	}

}
