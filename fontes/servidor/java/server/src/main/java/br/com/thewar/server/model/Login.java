package br.com.thewar.server.model;

import java.io.Serializable;
import java.util.Date;

/**
 * Model that represents the login
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class Login implements Serializable{

	private static final long serialVersionUID = 1L;

	// The nick of user
	private String nick;

	// The password of the user
	private String pass;

	// When the login was created
	private Date createdAt;

	// The last time when the login was updated
	private Date updatedAt;

	// The last time that user logged in the game
	private Date lastLogin;

	/**
	 * Model that represents the login
	 */
	public Login() {

	}

	/*
	 * Begin of the getters and setters of the attributes
	 */
	
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
	
	/*
	 * End of the getters and setters of the attributes
	 */

}
