package br.com.thewar.server.protocol;

public enum ResponseCode {

	UNKNOW(-1), SUCCESS(0), LOGIN_USER_ALREADY_LOGGED(1), LOGIN_UNKNOW_USER(2);

	private int id;

	private ResponseCode(int id) {

		this.id = id;

	}

	public int getCode() {

		return id;

	}
}
