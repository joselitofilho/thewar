package br.com.thewar.server.protocol;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.codehaus.jackson.JsonProcessingException;
import org.codehaus.jackson.map.ObjectMapper;

import br.com.thewar.server.model.Login;

public class Receiver implements Runnable{
	
	/**
	 * 
	 */
	private boolean execute;
	
	/**
	 * 
	 */
	private Socket socket;

	/**
	 * 
	 */
	private Logger logger;
	
	public Receiver(Socket socket) {
	
		logger = Logger.getLogger(Receiver.class.getName());
		
		execute = true;
		
		this.socket = socket;
		
		logger.log(Level.INFO, "Receiver initialized...");
		
	}

	public void run() {
		
		try{
			
			DataInputStream in = new DataInputStream(socket.getInputStream());
			
			byte[] buffer;
			
			int bufferLength;
			
			while(execute){
				
				bufferLength = in.available();
				
				buffer = new byte[bufferLength];
				
				if(bufferLength > 0){
					
					in.read(buffer);
					
					processData(new String(buffer));
					
				}
				

				
			}
			
		} catch (IOException e) {
			
			// TODO: handle exception
			e.printStackTrace();
			
			logger.log(Level.SEVERE, "ERROR: " + e.getMessage());
			
			e.printStackTrace();
			
		}
		
	}

	private void processData(String json) {
		
		try {
			
			logger.log(Level.INFO, "DATA: " + json );
			
			ObjectMapper mapper = new ObjectMapper();
			
			
			String type = mapper.readTree(json).path("type").asText();
			
			if(type.equals("login")){
				
				Login l = mapper.readValue(mapper.readTree(json).path("data"), Login.class);
				
				System.out.println(l.getNick());
				
			}
			
		} catch (JsonProcessingException e) {
			
			// TODO Auto-generated catch block
			e.printStackTrace();
			
			logger.log(Level.SEVERE, "ERROR: " + e.getMessage());
			
			
		} catch (IOException e) {
			
			// TODO Auto-generated catch block
			e.printStackTrace();
			
			logger.log(Level.SEVERE, "ERROR: " + e.getMessage());
			
		}	
		
	}

}
