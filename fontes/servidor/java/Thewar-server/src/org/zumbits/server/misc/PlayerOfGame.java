/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.zumbits.server.misc;

import java.util.ArrayList;

/**
 *
 * @author joselito
 */
public class PlayerOfGame {

    private int _pos;
    private String _nick;
    private ArrayList<Integer/*ID Territory*/> _territories;
    private int _soldiersInTurn;

    public PlayerOfGame( int pos, String nick, ArrayList<Integer> territories ) {
        _pos = pos;
        _nick = nick;
        _territories = territories;
        _soldiersInTurn = (int) Math.floor(territories.size() / 2);
    }

    public int getSoldiersInTurn() {
        return _soldiersInTurn;
    }

    public void setSoldiersInTurn(int _soldiersInTurn) {
        this._soldiersInTurn = _soldiersInTurn;
    }
    
}
