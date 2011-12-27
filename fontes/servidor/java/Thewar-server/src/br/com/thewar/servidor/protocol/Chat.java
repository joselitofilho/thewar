/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package br.com.thewar.servidor.protocol;

/**
 *
 * @author Joselito
 */
public class Chat {

    private String to;
    private String msg;

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public String getTo() {
        return to;
    }

    public void setTo(String to) {
        this.to = to;
    }
}
