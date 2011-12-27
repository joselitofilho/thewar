/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author zumbits
 */
public class Client extends Thread {

    Socket socket;
    BufferedReader in;
    PrintStream out;

    @Override
    public void run() {
        try {
            socket = new Socket("127.0.0.1", 1234);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintStream(socket.getOutputStream());
            Scanner scanner = new Scanner(System.in);

            Thread t = new Thread() {

                public void run() {
                    while (true) {
                        try {
                            System.out.println("server: " + in.readLine().trim());
                        } catch (Exception ex) {
                            Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
                        }
                    }
                }
            };

            t.start();

            String xml = "...";
            //Teste do login - OK
            //xml = "<?xml version='1.0' encoding='UTF-8'?><login><nick>masterneo</nick></login>";
            //out.println(xml);
            //System.out.println(in.readLine());
            //Teste do logoff - OK
//        xml = "<?xml version='1.0' encoding='UTF-8'?><logoff><nick>masterneo</nick></logoff>";
//        out.println(xml);
//        System.out.println(in.readLine());
            //Test do setPlayer - OK
//        xml = "<?xml version='1.0' encoding='UTF-8'?>" +
//                "<setPlayer>" +
//                "<id>1</id>" +
//                "<pos>3</pos>" +
//                "</setPlayer>";
            out.println(xml);
//        System.out.println(in.readLine());
//
//        xml = "<?xml version='1.0' encoding='UTF-8'?>" +
//                "<setPlayer>" +
//                "<id>2</id>" +
//                "<pos>3</pos>" +
//                "</setPlayer>";
//        out.println(xml);
//        System.out.println(in.readLine());
//<?xml version='1.0' encoding='UTF-8'?><chat><to></to><msg>oieeeeeeee</msg></chat>
            while (true) {
                System.out.println("esperando xml...");
                xml = scanner.nextLine();
                out.println(xml);
                System.out.println("xml enviado...");
            }
        } catch (Exception ex) {
            Logger.getLogger(Client.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public static void main(String args[]) throws Exception {
        // cria o socket de acesso ao server hostname na porta específica
        Client c = new Client();

        c.start();
    }
}
