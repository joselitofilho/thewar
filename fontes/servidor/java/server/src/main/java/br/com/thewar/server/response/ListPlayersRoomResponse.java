package br.com.thewar.server.response;

import java.util.List;

import br.com.thewar.server.model.Room;

public class ListPlayersRoomResponse extends AbstractResponse {

	public ListPlayersRoomResponse() {
		
		super(ListPlayersRoomResponse.class.getSimpleName().toLowerCase());
		
	}

	public void setPlayersRoom(List<Room> rooms){
		
		data.put("listusers", rooms);
		
	}
}
