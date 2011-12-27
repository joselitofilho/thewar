package br.com.thewar.server;

import br.com.thewar.server.protocol.Server;

public class Main {
	
	public static void main(String[] args) {
		 
		try{
			
			Server server = new Server();
			
			server.run();
			
		} catch (Exception e) {
			
			// TODO: handle exception
			e.printStackTrace();
		}
		
	}
	
}
