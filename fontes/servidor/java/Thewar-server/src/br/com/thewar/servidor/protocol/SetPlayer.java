/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package br.com.thewar.servidor.protocol;

/**
 *
 * @author zumbits
 */
public class SetPlayer {

    private int room;
    private int pos;

    public SetPlayer() {
    }

    public int getRoom() {
        return room;
    }

    public void setRoom(int room) {
        this.room = room;
    }

    public int getPos() {
        return pos;
    }

    public void setPos(int pos) {
        this.pos = pos;
    }
}
