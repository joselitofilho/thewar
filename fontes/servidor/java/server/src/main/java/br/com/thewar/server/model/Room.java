package br.com.thewar.server.model;

import java.io.Serializable;
import java.util.LinkedList;

import br.com.thewar.server.protocol.ResponseCode;

public class Room implements Serializable {

	private static final long serialVersionUID = 1L;

	private Integer id;

	private String nickOwner;

	private LinkedList<RoomPlayer> roomlPlayers;

	public Room(int id) {
		
		roomlPlayers = new LinkedList<RoomPlayer>();

		this.id = id;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getNickOwner() {
		return nickOwner;
	}

	public void setNickOwner(String nickOwner) {
		this.nickOwner = nickOwner;
	}

	public LinkedList<RoomPlayer> getRoomplPlayers() {
		return roomlPlayers;
	}

	public Boolean isPositionEmpty(Integer position) {

		for (RoomPlayer rp : roomlPlayers) {

			if (rp.getPosition() == position) {

				return false;

			}

		}

		return true;

	}

	public Integer addPlayer(String nick, Integer position) {

		Integer status = -1;

		RoomPlayer player = new RoomPlayer(nick, position);

		if (!isPositionEmpty(position)) {

			// Já existe um jogador na popsição que ele quer entrar
			status = 3;

		} else {

			if (!roomlPlayers.contains(player)) {

				if (roomlPlayers.isEmpty()) {

					// Usuário entrou na sala e é o dono
					status = 1;

				} else {

					status = ResponseCode.SUCCESS.getCode();

				}

				roomlPlayers.addLast(player);

				return status;

			}

			for (RoomPlayer rp : roomlPlayers) {

				if (rp.getNick().equals(nick)) {

					if (rp.getPosition() != position) {

						rp.setPosition(position);

						// Usuário mudou de canto na própia sala
						status = 2;

					}

				}

			}

		}

		return status;

	}

}
