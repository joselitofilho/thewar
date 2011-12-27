package br.com.thewar.server.protocol;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

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

	private void processData(String data) {
		
		
		
	}
	
	

}
