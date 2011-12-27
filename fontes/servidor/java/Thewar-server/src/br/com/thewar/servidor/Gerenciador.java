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

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;

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
			DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
			DocumentBuilder builder;
			builder = fact.newDocumentBuilder();
			Document doc = builder.parse(new ByteArrayInputStream(xml
					.getBytes()));
			Node node = doc.getDocumentElement();
			String root = node.getNodeName();

			logger.log(Level.INFO, "Processando: " + xml);

			if (root.equals(Servidor.LOGIN)) {
				Servidor.ProcessarLogin(socket, xml);
			}
		} catch (ParserConfigurationException e) {
			e.printStackTrace();
			logger.log(Level.SEVERE, null, e);
		} catch (SAXException e) {
			e.printStackTrace();
			logger.log(Level.SEVERE, null, e);
		} catch (IOException e) {
			e.printStackTrace();
			logger.log(Level.SEVERE, null, e);
		}
	}

	private boolean rodar;
	private Socket socket;

	private Logger logger;
}
