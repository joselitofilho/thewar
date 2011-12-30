package br.com.thewar.server.protocol;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonProcessingException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;

import br.com.thewar.server.dao.LoginDAO;
import br.com.thewar.server.model.Login;
import br.com.thewar.server.response.ListUsersLoggedResponse;
import br.com.thewar.server.response.LoginResponse;
import br.com.thewar.server.response.UserLoggedResponse;

/**
 * Class that receive the socket and treat the data, forwarding to the target
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Receiver extends Thread {

	// Sentinel variable to while block
	private boolean execute;

	// Socket with client
	private Socket socket;

	// Logger class to log the actions
	private Logger logger;

	// Object mapper of JSON
	private ObjectMapper mapper;
	
	// Sesion object
	private Session session;

	/**
	 * This class will receiver the socket data and forward to respective target
	 * 
	 * @param Client
	 *            socket
	 */
	public Receiver(Socket socket) {

		// Preparing the battlefield :-)
		logger = Logger.getLogger(Receiver.class.getName());
		execute = true;
		session = Session.getInstance();
		this.socket = socket;
		logger.log(Level.INFO, "Receiver initialized...");

	}

	/**
	 * Read the socket data and send to specific target
	 */
	public void run() {

		try {

			// Preparing the DataInputStrean to read the socket data
			DataInputStream in = new DataInputStream(socket.getInputStream());
			byte[] data;
			int bufferLength;

			/*
			 * While the execute sentinel varibale is true execute the block
			 * bellow
			 */
			while (execute) {

				// Buffer length of data
				bufferLength = in.available();

				// Byte array of data
				data = new byte[bufferLength];

				/*
				 * If bufferLength is major then 0 read the data and process it
				 */
				if (bufferLength > 0) {

					// Read the data and send to the processData
					in.read(data);
					processData(new String(data));

				}

			}

		} catch (IOException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, "ERROR: " + e.getMessage());

		}

	}

	/**
	 * Process the data receives of the client socket
	 * 
	 * @param json
	 *            data of the client
	 */
	private void processData(String json) {

		try {

			// Register the data received of client on the log and create the
			// object mapper of JSON
			logger.log(Level.INFO, "Receive data: " + json);
			mapper = new ObjectMapper();

			// Read the type of data was received
			String type = mapper.readTree(json).path("type").asText();

			/*
			 * Decide who must respond the type received
			 */
			if (type.equals("loginrequest")) {

				Login l = mapper.readValue(mapper.readTree(json).path("data"),
						Login.class);
				
				processLogin(l);

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
	
	/**
	 * Processes the data received by the client login
	 * 
	 * @param loginRequest
	 * 					  data of login request
	 */
	private void processLogin(Login loginRequest)
	{
		try {
			
			String nick = loginRequest.getNick();
			
			// Get the login in database
			LoginDAO loginDAO = new LoginDAO();
			loginRequest = loginDAO.load(nick, loginRequest.getPass());
			
			ResponseCode respCode = ResponseCode.UNKNOW;
			
			// Checking for user data
			respCode = (loginRequest != null) ? ResponseCode.SUCCESS : ResponseCode.LOGIN_UNKNOW_USER;
			
			LoginResponse loginResponse = new LoginResponse();
			loginResponse.setStatus(respCode.getCode());
			
			// Send message to the current socket
			Server.sendMessage(loginResponse.getResponseMessage(), new Socket[] { socket });
			
			if (respCode == ResponseCode.SUCCESS) {
				
				// Fill the last login atribute
				loginRequest.setLastLogin(new Date());
				loginDAO.save(loginRequest);
				
				// Adds the current socket in the session
				session.add(nick, socket);
				
				// Get the list of all users logged
				List<String> nicks = session.getAllNicks();
				
				// Create the response of list users logged
				ListUsersLoggedResponse listUsersloggedResponse = new ListUsersLoggedResponse();
				listUsersloggedResponse.setUsers(nicks);
				
				// Send the message to the list of users logged into the current socket 
				Server.sendMessage(listUsersloggedResponse.getResponseMessage(), new Socket[] { socket });
				
				// Create the response of the user logged
				UserLoggedResponse userLoggedResponse = new UserLoggedResponse();
				userLoggedResponse.setNick(nick);
				
				// Send the message for all users logged that this user(nick) logged
				Server.sendMessage(userLoggedResponse.getResponseMessage(), (Socket[]) session.getAllSockets().toArray());
				
			}
		
		} catch (JsonGenerationException e) {
			
			// Register the exception on log
			logger.log(Level.SEVERE, null, e);
			
		} catch (JsonMappingException e) {
			
			// Register the exception on log
			logger.log(Level.SEVERE, null, e);
			
		} catch (IOException e) {
			
			// Register the exception on log
			logger.log(Level.SEVERE, null, e);
			
		}
	
	}

}
