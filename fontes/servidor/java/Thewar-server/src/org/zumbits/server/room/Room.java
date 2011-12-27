/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.zumbits.server.room;

/**
 *
 * @author zumbits
 */
public class Room {

    public static int SET_PLAYER_EXIT_ROOM = -1;
    public static int SET_PLAYER_SUCCESS = 0;
    public static int SET_PLAYER_OWNER = 1;
    public static int SET_PLAYER_SWAP = 2;
    public static int SET_PLAYER_ALREADY = 3;
    public static int SET_PLAYER_OTHER_ROOM = 4;
    public static int SET_PLAYER_AUTHENTICATE = 5;
    //
    private int id;
    private int owner;
    private String[] listPlayers;

    public Room(int id) {
        this.id = id;
        owner = -1;
        listPlayers = new String[6];

        for (int i = 0; i < 6; i++) {
            listPlayers[i] = null;
        }
    }

    public int getPos(String nick) {
        for (int i = 0; i < listPlayers.length; i++) {
            if (listPlayers[i] != null && listPlayers[i].equals(nick)) {
                return i;
            }
        }

        return -1;
    }

    public String[] getListPlayers() {
        return listPlayers;
    }

    public int getOwner() {
        return owner;
    }

    /**
     * Adiciona um novo usuário na lista de jogadores se ele não estiver ou
     * atualiza a sua posição caso contrário.
     *
     * @param pos
     * @param nick
     * @return
     */
    public int replacePlayer(int pos, String nick) {
        int status = -1;
        int posOld;

        //recupera a posição anterior
        posOld = getPos(nick);

        if (pos == SET_PLAYER_EXIT_ROOM && posOld != -1) {
            listPlayers[posOld] = null;
            status = SET_PLAYER_SUCCESS;

            if (owner == posOld) {
                owner = -1;

                //sorteia um novo dono da sala...
                owner = randomNewOwner();
            }
        } else {

            //pequena correção de ID do vetor
            pos = pos - 1;

            if (listPlayers[pos] == null) {
                listPlayers[pos] = nick;

                if (posOld != -1) {
                    listPlayers[posOld] = null;
                    //mudou de posição
                    status = SET_PLAYER_SWAP;

                    if (owner == posOld) {
                        owner = pos;
                    }
                } else {
                    //adicionado
                    status = SET_PLAYER_SUCCESS;
                }

                if (owner == -1) {
                    owner = pos;

                    //adicionado e setado o owner
                    status = SET_PLAYER_OWNER;
                }
            } else {
                //já existe um usuário na posição
                status = SET_PLAYER_ALREADY;
            }
        }

        return status;
    }

    private int randomNewOwner() {
        for ( int i=0; i < listPlayers.length; i++ ) {
            if ( listPlayers[i] != null ) {
                return i;
            }
        }

        return -1;
    }
}
