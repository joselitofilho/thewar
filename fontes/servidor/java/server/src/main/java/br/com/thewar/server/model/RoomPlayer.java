package br.com.thewar.server.model;

import java.io.Serializable;

public class RoomPlayer implements Serializable{

	private static final long serialVersionUID = 1L;

	private Integer position;

	private String nick;
	
	public RoomPlayer() {
		// TODO Auto-generated constructor stub
	}
	
	public RoomPlayer(String nick, Integer position) {
		
		this.nick = nick;
		
		this.position = position;
		
	}

	public Integer getPosition() {
		return position;
	}

	public void setPosition(Integer position) {
		this.position = position;
	}

	public String getNick() {
		return nick;
	}

	public void setNick(String nick) {
		this.nick = nick;
	}

}
