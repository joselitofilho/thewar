package br.com.thewar.server.protocol;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.codehaus.jackson.JsonProcessingException;
import org.codehaus.jackson.map.ObjectMapper;

import br.com.thewar.server.dao.LoginDAO;
import br.com.thewar.server.model.Login;
import br.com.thewar.server.response.LoginResponse;

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

	// PrintStream that write the response to client
	private PrintStream printStream;

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
			String message = "";

			/*
			 * Decide who must respond the type received
			 */
			if (type.equals("loginrequest")) {

				Login l = mapper.readValue(mapper.readTree(json).path("data"),
						Login.class);

				LoginDAO loginDAO = new LoginDAO();

				l = loginDAO.load(l.getNick(), l.getPass());
					
				LoginResponse loginResponse = new LoginResponse();

				if (l != null) {

					// Response Code of SUCCESS
					loginResponse.setStatus(ResponseCode.SUCCESS.getCode());
					
					Session.getInstance().add(l.getNick(), socket);

				} else {

					// Response Code of UNKNOW_USER
					loginResponse.setStatus(ResponseCode.LOGIN_UNKNOW_USER
							.getCode());

				}		
				
				message = loginResponse.getResponseMessage();
				
				loginDAO = null;

			}
			
			// PrintStream that write the response to client
			printStream = new PrintStream(socket.getOutputStream());
			printStream.print(message);
			printStream.flush();

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
