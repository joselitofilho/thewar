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

	protected String className;
	
	protected HashMap<String, Object> data;
	
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
	
	public String getResponseMessage() throws JsonGenerationException, JsonMappingException, IOException{
		
		Map<String, Object> userInMap = new HashMap<String, Object>();
		
		userInMap.put("type", getType());
		userInMap.put("data", getData());
		
		return new ObjectMapper().writeValueAsString(userInMap).toLowerCase();
		
	}
	
}
