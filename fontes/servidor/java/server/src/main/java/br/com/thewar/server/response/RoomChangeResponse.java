package br.com.thewar.server.response;

public class RoomChangeResponse extends AbstractResponse {

	public RoomChangeResponse() {
		super(RoomChangeResponse.class.getSimpleName());
	}

	/**
	 * Set the status of response
	 * 
	 * @param status of response
	 */
	public void setStatus(Integer status) {
	
		data.put("status", status);

	}
}
