package br.com.thewar.server.model;

import java.util.Date;

/**
 * Model that represents the login
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Login {

	private String nick;

	private String pass;

	private Date createdAt;

	private Date updatedAt;

	private Date lastLogin;

	/**
	 * Model that represents the login
	 */
	public Login() {

	}

	public String getNick() {

		return nick;

	}

	public void setNick(String nick) {

		this.nick = nick;

	}

	public String getPass() {

		return pass;

	}

	public void setPass(String pass) {

		this.pass = pass;

	}

	public Date getCreatedAt() {

		return createdAt;

	}

	public void setCreatedAt(Date createdAt) {

		this.createdAt = createdAt;

	}

	public Date getUpdatedAt() {

		return updatedAt;

	}

	public void setUpdatedAt(Date updatedAt) {

		this.updatedAt = updatedAt;

	}

	public Date getLastLogin() {

		return lastLogin;

	}

	public void setLastLogin(Date lastLogin) {

		this.lastLogin = lastLogin;

	}

}
