/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package br.com.thewar.servidor.protocol;

/**
 *
 * @author joselito
 */
public class UpdateGame {

    public static int UPDATE_GAME_TURN_INIT = 0;
    public static int UPDATE_GAME_TURN_PLACE = 1;
    public static int UPDATE_GAME_TURN_ATACK = 2;
    public static int UPDATE_GAME_TURN_MOVE = 3;

    private int numberSession;
    private int type;
    private int stateFrom;
    private int stateTo;
    private int quantity;
    private int player; /*nick*/

    public int getNumberSession() {
        return numberSession;
    }

    public void setNumberSession(int numberSession) {
        this.numberSession = numberSession;
    }

    public int getPlayer() {
        return player;
    }

    public void setPlayer(int player) {
        this.player = player;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public int getStateFrom() {
        return stateFrom;
    }

    public void setStateFrom(int stateFrom) {
        this.stateFrom = stateFrom;
    }

    public int getStateTo() {
        return stateTo;
    }

    public void setStateTo(int stateTo) {
        this.stateTo = stateTo;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }
}
