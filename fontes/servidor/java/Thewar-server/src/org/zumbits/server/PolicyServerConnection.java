/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.server;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

/**
 *
 * @author usuario
 */
public class PolicyServerConnection extends Thread {

    protected Socket socket;
    protected BufferedReader socketIn;
    protected PrintWriter socketOut;

    /**
     * Creates a new instance of PolicyServerConnection.
     *
     * @param socket client's socket connection
     */
    public PolicyServerConnection(Socket socket) {
        this.socket = socket;
    }

    /**
     * Create a reader and writer for the socket and call readPolicyRequest.
     */
    public void run() {
        try {
            this.socketIn = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
            this.socketOut = new PrintWriter(this.socket.getOutputStream(), true);
            readPolicyRequest();
        } catch (Exception e) {
            System.out.println("Exception (run): " + e.getMessage());
        }
    }

    /**
     * Reads a string from the client and if it is a policy request we write the policy, then we close the connection.
     */
    protected void readPolicyRequest() {
        try {
            String request = read();
            System.out.println("client says '" + request + "'");

            if (request.equals(PolicyServer.POLICY_REQUEST)) {
                writePolicy();
            }
        } catch (Exception e) {
            System.out.println("Exception (readPolicyRequest): " + e.getMessage());
        }
        finalize();
    }

    /**
     * Writes the policy of the server.
     */
    protected void writePolicy() {
        try {
            this.socketOut.write(PolicyServer.POLICY_XML + "\u0000");
            this.socketOut.close();
            System.out.println("policy sent to client");
        } catch (Exception e) {
            System.out.println("Exception (writePolicy): " + e.getMessage());
        }
    }

    /**
     * Safely read a string from the reader until a zero character is received or the 200 character is reached.
     *
     * @return the string read from the reader.
     */
    protected String read() {
        StringBuffer buffer = new StringBuffer();
        int codePoint;
        boolean zeroByteRead = false;

        try {
            do {
                codePoint = this.socketIn.read();

                if (codePoint == 0) {
                    zeroByteRead = true;
                } else if (Character.isValidCodePoint(codePoint)) {
                    buffer.appendCodePoint(codePoint);
                }
            } while (!zeroByteRead && buffer.length() < 200);
        } catch (Exception e) {
            System.out.println("Exception (read): " + e.getMessage());
        }

        return buffer.toString();
    }

    /**
     * Closes the reader, the writer and the socket.
     */
    protected void finalize() {
        try {
            this.socketIn.close();
            this.socketOut.close();
            this.socket.close();
            System.out.println("connection closed");
        } catch (Exception e) {
            System.out.println("Exception (finalize): " + e.getMessage());
        }
    }
}
