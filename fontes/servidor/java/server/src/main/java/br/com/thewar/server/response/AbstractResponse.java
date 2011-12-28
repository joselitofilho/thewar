/**
 * 
 */
package br.com.thewar.server.response;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;

/**
 * @author Bruno Lopes Alcantara Batista
 *
 */
public abstract class AbstractResponse {

	// The class name
	protected String className;
	
	// Hasmap that contains the data of response
	protected HashMap<String, Object> data;
	
	// Hashmap that contains the login response
	protected Map<String, Object> response;
	
	/**
	 * Abstract class that encapsulate the response logic
	 * @param className
	 */
	protected AbstractResponse(String className) {
	
		this.className = className;
		
		data = new HashMap<String, Object>();
	}
	
	public HashMap<String, Object> getData(){
		
		return data;
		
	}
	
	public String getType(){
		
		return this.className;
		
	}
	
	/**
	 * The response of login protocol
	 * 
	 * @return a well-formed JSON string object
	 * @throws JsonGenerationException
	 * @throws JsonMappingException
	 * @throws IOException
	 */
	public String getResponseMessage() throws JsonGenerationException, JsonMappingException, IOException{
		
		response = new HashMap<String, Object>();
		
		response.put("type", getType());
		response.put("data", getData());
		
		return new ObjectMapper().writeValueAsString(response).toLowerCase();
		
	}
	
}
