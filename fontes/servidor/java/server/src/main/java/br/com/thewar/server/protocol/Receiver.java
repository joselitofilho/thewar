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
import br.com.thewar.server.lang.IObserver;
import br.com.thewar.server.lang.ISubject;
import br.com.thewar.server.model.Login;
import br.com.thewar.server.model.Room;
import br.com.thewar.server.request.RoomChangeRequest;
import br.com.thewar.server.response.ListPlayersRoomResponse;
import br.com.thewar.server.response.ListUsersLoggedResponse;
import br.com.thewar.server.response.LoginResponse;
import br.com.thewar.server.response.RoomChangeResponse;
import br.com.thewar.server.response.UserLoggedResponse;

/**
 * Class that receive the socket and treat the data, forwarding to the target
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Receiver extends Thread implements ISubject {

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

	//
	private List<Server> list = new ArrayList<Server>();

	//
	private String stateMessage;

	//
	private List<Socket> stateSockets;

	public Socket getSocket() {
		return socket;
	}

	public String getStateMessage() {
		return stateMessage;
	}

	public void setStateMessage(String stateMessage) {
		this.stateMessage = stateMessage;
	}

	public List<Socket> getStateSockets() {
		return stateSockets;
	}

	public void setStateSockets(List<Socket> stateSockets) {
		this.stateSockets = stateSockets;
	}

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

			} else if (type.equals("roomchangerequest")) {

				RoomChangeRequest roomChangeRequest = mapper.readValue(mapper
						.readTree(json).path("data"), RoomChangeRequest.class);

				processRoomChange(roomChangeRequest.getRoom(),
						roomChangeRequest.getPos(), Session.getInstance()
								.getNick(socket));

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

	private void processRoomChange(Integer room, Integer pos, String nick) {

		try {
			Room r = Session.getInstance().getRoomList().get(room);
			RoomChangeResponse resp = new RoomChangeResponse();
			resp.setStatus(r.addPlayer(nick, pos));

			ArrayList<Socket> currentSocket = new ArrayList<Socket>();
			currentSocket.add(socket);

			notifyObservers(resp.getResponseMessage(), currentSocket);
			
			//if (0, 1, 2) {
			
			//}
		} catch (JsonGenerationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JsonMappingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * Processes the data received by the client login
	 * 
	 * @param loginRequest
	 *            data of login request
	 */
	private void processLogin(Login loginRequest) {
		try {

			String nick = loginRequest.getNick();

			// Get the login in database
			LoginDAO loginDAO = new LoginDAO();
			loginRequest = loginDAO.load(nick, loginRequest.getPass());

			ResponseCode respCode = ResponseCode.UNKNOW;

			// Checking for user data
			respCode = (loginRequest != null) ? ResponseCode.SUCCESS
					: ResponseCode.LOGIN_UNKNOW_USER;

			LoginResponse loginResponse = new LoginResponse();
			loginResponse.setStatus(respCode.getCode());

			// Send message to the current socket
			ArrayList<Socket> currentSocket = new ArrayList<Socket>();
			currentSocket.add(socket);
			notifyObservers(loginResponse.getResponseMessage(), currentSocket);

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

				// Send the message to the list of users logged into the current
				// socket
				notifyObservers(listUsersloggedResponse.getResponseMessage(),
						currentSocket);
				
				// Get the list of all players room
				List<Room> playersRoom = session.getAllPlayersRoom(); 
				
				// Create the response of list players room
				ListPlayersRoomResponse listPlayersRoom = new ListPlayersRoomResponse();
				listPlayersRoom.setPlayersRoom(playersRoom);
				
				// Send the message to the list of users logged into the current
				// socket
				notifyObservers(listPlayersRoom.getResponseMessage(),
						currentSocket);

				// Create the response of the user logged
				UserLoggedResponse userLoggedResponse = new UserLoggedResponse();
				userLoggedResponse.setNick(nick);

				// Send the message for all users logged that this user(nick)
				// logged

				notifyObservers(userLoggedResponse.getResponseMessage(),
						session.getAllSockets());

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

	/**
	 * 
	 * @param observer
	 */
	public void attach(IObserver observer) {
		list.add((Server) observer);
	}

	/**
	 * 
	 * @param observer
	 */
	public void detach(IObserver observer) {
		list.remove(observer);
	}

	/**
	 * 
	 * @param subjectState
	 */
	public void notifyObservers(String stateMessage, List<Socket> stateSockets) {

		this.stateMessage = stateMessage;

		this.stateSockets = stateSockets;

		notifyObservers();

	}

	public void notifyObservers() {

		for (IObserver ob : list) {
			((Server) ob).Update(socket);
		}

	}

}
