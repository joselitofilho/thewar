/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.server;

import java.net.ServerSocket;
import java.net.Socket;

/**
 *
 * @author usuario
 */
public class PolicyServer extends Thread {

    public static final String POLICY_REQUEST = "<policy-file-request/>";
    public static final String POLICY_XML =
            "<?xml version='1.0'?>"
            + "<cross-domain-policy>"
            + "<allow-access-from domain='*' to-ports='*' />"
            + "</cross-domain-policy>";
    protected int port;
    protected ServerSocket serverSocket;
    protected boolean listening;

    /**
     * Creates a new instance of PolicyServer.
     *
     * @param serverPort the port to be used by the server
     */
    public PolicyServer(int serverPort) {
        this.port = serverPort;
        this.listening = false;
    }

    /**
     * Waits for clients' connections and handles them to a new PolicyServerConnection.
     */
    public void run() {
        try {
            this.serverSocket = new ServerSocket(this.port);
            this.listening = true;
            System.out.println("Policy Server: listening...");

            while (this.listening) {
                Socket socket = this.serverSocket.accept();
                System.out.println("Policy Server: Client connection from " + socket.getRemoteSocketAddress());
                PolicyServerConnection socketConnection = new PolicyServerConnection(socket);
                socketConnection.start();
            }
        } catch (Exception e) {
            System.out.println("Policy Server Exception (run): " + e.getMessage());
        }
    }
}
