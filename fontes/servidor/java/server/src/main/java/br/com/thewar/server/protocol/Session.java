/**
 * 
 */
package br.com.thewar.server.protocol;

import java.net.Socket;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import br.com.thewar.server.model.Room;

/**
 * Class that maintain the socket session
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Session {

	// HashMap that contains the session
	private HashMap<String, Socket> sessionMap;

	private HashMap<Integer, Room> roomList;

	// Instance of this class
	private static Session instance;

	// List of all sockets of the session
	private List<Socket> sockets;

	// List of all nicks of the session
	private List<String> nicks;

	// Register events on the log
	private static Logger logger = Logger.getLogger(Session.class
			.getSimpleName());

	/**
	 * Private constructor
	 */
	private Session() {

		sessionMap = new HashMap<String, Socket>();

		roomList = new HashMap<Integer, Room>();
		for (int i = 1; i <= 10; ++i) {
			roomList.put(i, new Room(i));
		}
	}

	public HashMap<Integer, Room> getRoomList() {
		return roomList;
	}

	/**
	 * Add a new entry on session
	 * 
	 * @param nick
	 *            of the session
	 * @param socket
	 *            of the session
	 */
	public void add(String nick, Socket socket) {

		logger.log(Level.INFO, "adding socket " + socket.toString());

		sessionMap.put(nick, socket);

	}

	/**
	 * Delete a specific session by nick
	 * 
	 * @param nick
	 *            of the session
	 */
	public void delete(String nick) {

		logger.log(Level.INFO, "removing nick " + nick);

		sessionMap.remove(nick);

	}

	/**
	 * Get a socket of specific nikc
	 * 
	 * @param nick
	 *            of the session
	 * @return a socket of the session's nick
	 */
	public Socket getSocket(String nick) {

		logger.log(Level.INFO, "get socket of nick " + nick);

		return sessionMap.get(nick);

	}

	public String getNick(Socket socket) {

		logger.log(Level.INFO, "get nick of socket " + socket);

		Iterator<String> it = sessionMap.keySet().iterator();

		for (Socket s : sessionMap.values()) {

			if (socket.equals(s)) {

				return it.next();

			} else {

				it.next();

			}

		}

		return null;

	}

	/**
	 * Get a list of all sockets
	 * 
	 * @return a list of all sockets
	 */
	public List<Socket> getAllSockets() {

		logger.log(Level.INFO, "gel all socket of the session ");

		sockets = null;

		// If sessionMap is major than zero, return a list of session's socket
		if (sessionMap.size() > 0) {

			sockets = new ArrayList<Socket>();

			Collection<Socket> collection = sessionMap.values();

			Iterator<Socket> iterator = collection.iterator();

			while (iterator.hasNext()) {

				Socket socket = (Socket) iterator.next();

				sockets.add(socket);

			}

		}

		return sockets;

	}

	/**
	 * Get a list of all nicks
	 * 
	 * @return a list the nicks
	 */
	public List<String> getAllNicks() {

		logger.log(Level.INFO, "gel all nicks of the session ");

		nicks = null;

		if (sessionMap.size() > 0) {

			nicks = new ArrayList<String>();

			Collection<String> collection = sessionMap.keySet();

			Iterator<String> iterator = collection.iterator();

			while (iterator.hasNext()) {

				String nick = iterator.next();

				nicks.add(nick);

			}

		}

		return nicks;

	}
	
	public List<Room> getAllPlayersRoom() {
		
		ArrayList<Room> r = new ArrayList<Room>();
		
		for (Room rl : roomList.values()) {
			
			r.add(rl);
			
		}
		
		return r;
	}

	/**
	 * Get all session's nicks and sockets
	 * 
	 * @return the HashMap with all nicks (key) and sockets (value)
	 */
	public HashMap<String, Socket> getSession() {

		logger.log(Level.INFO, "get the session list of nicks and sockets ");

		return sessionMap;

	}

	/**
	 * Return the number of sockets on the session
	 * 
	 * @return the size of session
	 */
	public Integer size() {

		logger.log(Level.INFO, "get the size of the session");

		return sessionMap.size();

	}

	/**
	 * @return the instance of session class
	 */
	public static Session getInstance() {

		logger.log(Level.INFO, "returning the instance os session");

		// If instance is equal null, create a new instance of session
		if (instance == null) {

			instance = new Session();

		}

		return instance;

	}

}
