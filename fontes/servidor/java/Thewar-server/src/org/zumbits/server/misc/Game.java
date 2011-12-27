/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.zumbits.server.misc;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.Random;

/**
 *
 * @author joselito
 */
public class Game {

    public static int START_GAME_CREATE_SUCCESS = 0;
    public static int START_GAME_ROOM_NOT_EXIST = 1;
    public static int START_GAME_PREVOUSLY_CREATED = 2;
    public static int START_GAME_CREATE_INVALID_NUMBER_PLAYERS = 3;
    //public static int START_GAME_LOAD_SUCCESS = 10;
    //
    public static int OBJECTIVES_ID[] =
        {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
         11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
    //
    private int _startPlayer;
    //
    private String[] _listPlayers;
    //
    private Hashtable<Integer, ArrayList<Integer>/*Ids territórios...*/> _territoriesPerPlayer;
    private HashMap<Integer, Territory> _territories;
    private HashMap<Integer, PlayerOfGame> _playersOfGame;
    //
    private Hashtable<Integer, Integer> _objective;
    //
    private int _numberSession;

    public Game(String[] listPlayers, int numberSession) {
        _startPlayer = -1;
        _listPlayers = listPlayers;
        _territoriesPerPlayer = new Hashtable<Integer, ArrayList<Integer>>();
        _territories = new HashMap<Integer, Territory>();
        _playersOfGame = new HashMap<Integer, PlayerOfGame>();
        _objective = new Hashtable<Integer, Integer>();
        _numberSession = numberSession;

        for ( int i=Territory.TERRITORIES_ID[0]; i <= Territory.TERRITORIES_ID.length; ++i ) {
            _territories.put(i, new Territory(i, 1));
        }
        //init();
    }

    public void init() {
        // TODO: inicializar os elementos da sala...
        ///Selecionando o jogador que começará a partida
        int numPlayers = 0;
        for (int i=0; i < 6; ++i) {
            if ( _listPlayers[i] != null ) {
                ++numPlayers;
            }
        }

        //Verifica apenas a posição... Logo na frente ele recebe o valor mesmo do jogador
        _startPlayer = new Random().nextInt(numPlayers);

        ///Distribuindo cartões
        int numCards = Territory.TERRITORIES_ID.length / numPlayers;
        LinkedList<Integer> l_territories = new LinkedList<Integer>();
        LinkedList<Integer> l_objetivo = new LinkedList<Integer>();
        Random r = new Random();
        int rand;
        boolean sairDoWhile;
        boolean selectedStartPlayerYet = false;
        
        //for ( int i=0; i < numPlayers; ++i ) {
        for (int i=0,k=0; i < 6; ++i) {
            if ( _listPlayers[i] != null ) {

                if ( k == _startPlayer && !selectedStartPlayerYet ) {
                    _startPlayer = i;
                }

                ArrayList<Integer> territoryPerPlayer = new ArrayList<Integer>();
                for ( int j=(k*numCards); j < (k+1)*numCards; ++j ) {
                    do {
                        rand = (r.nextInt(Territory.TERRITORIES_ID.length)) + 1; /*1 to 42*/

                        if ( !l_territories.contains(rand) ) {
                            l_territories.add(rand);
                            territoryPerPlayer.add(rand);
                            sairDoWhile = true;
                        } else {
                            sairDoWhile = false;
                        }
                    } while( !sairDoWhile );
                }

                _territoriesPerPlayer.put(i, territoryPerPlayer);
                _playersOfGame.put( i , new PlayerOfGame(i, _listPlayers[i], territoryPerPlayer));

                ///Gerar objetivo
                do {
                    rand = r.nextInt(OBJECTIVES_ID.length);
                    if ( !l_objetivo.contains(rand) ) {
                        l_objetivo.add(rand);
                        sairDoWhile = true;
                    } else {
                        sairDoWhile = false;
                    }
                } while ( !sairDoWhile );

                _objective.put(i, rand);
            }
        }        
    }

    public int getStartPlayer() {
        return _startPlayer;
    }

    public ArrayList<Integer> getTerritoriesPerPlayer(int player) {
        return _territoriesPerPlayer.get(player);
    }

    public String getTerritoriesPerPlayerList(int player) {
        ArrayList<Integer> territoriesPerPlayer = _territoriesPerPlayer.get(player);
        String ret = "";

        int i;
        for ( i=0; i < territoriesPerPlayer.size()-1; ++i ) {
            ret += territoriesPerPlayer.get(i) + ";";
        }
        ret += territoriesPerPlayer.get(i);

        return ret;
    }

    public int getObjective(int player) {
        return _objective.get(player);
    }

    public int updateTerritoryAdd(int stateFrom, int quantity, int playerPos) {
        PlayerOfGame p = _playersOfGame.get(playerPos);
        Territory t = _territories.get(stateFrom);

        if ( p.getSoldiersInTurn()-quantity >= 0) {
            p.setSoldiersInTurn( p.getSoldiersInTurn()-quantity );
            _playersOfGame.put(playerPos, p);
            
            t.setQuantity(t.getQuantity()+quantity);
            _territories.put(stateFrom, t);
        }

        return t.getQuantity();
    }

    public PlayerOfGame getPlayerOfGame( int playerPos ) {
        return _playersOfGame.get( playerPos );
    }

    public String[] getListPlayer() {
        return _listPlayers;
    }
}
