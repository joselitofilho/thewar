package br.com.thewar.servidor;

import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.codehaus.jackson.map.ObjectMapper;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;

import br.com.thewar.model.GenericModel;
import br.com.thewar.servidor.protocol.Login;

/**
 * 
 * @author Joselito
 *
 */
public class Gerenciador extends Thread {
	/**
	 * 
	 * @param socket_
	 */
	public Gerenciador(Socket socket_) {
		rodar = true;
		socket = socket_;
		//
		logger = Logger.getLogger("Gerenciador");
	}

	@Override
	public void run() {
		try {
			DataInputStream in = new DataInputStream(socket.getInputStream());

			byte[] buffer;
			int tamanhoBuffer;
			while (rodar) {
				tamanhoBuffer = in.available();
				buffer = new byte[tamanhoBuffer];

				if (tamanhoBuffer > 0) {
					in.read(buffer);
					processar(new String(buffer));
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
			logger.log(Level.SEVERE, null, e);
		}
	}

	private void processar(String xml) {
		try {
			logger.log(Level.INFO, "XML: " + xml );
			ObjectMapper mapper = new ObjectMapper(); // can reuse, share globally
			String type = mapper.readTree(xml).path("type").asText();
			
			if (type.equals("login")) {
				Login l = mapper.readValue(mapper.readTree(xml).path("data"), Login.class);
				//Servidor.ProcessarLogin(socket, xml);
				System.out.println(l.getNick());
			}

			//logger.log(Level.INFO, "Jason: " + );
		} catch (IOException e) {
			e.printStackTrace();
			logger.log(Level.SEVERE, null, e);
		}
	}

	private boolean rodar;
	private Socket socket;

	private Logger logger;
}
