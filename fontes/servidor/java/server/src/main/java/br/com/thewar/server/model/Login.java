package br.com.thewar.server.model;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.SequenceGenerator;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

/**
 * Model that represents the login
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
@Entity
@Table(name = "logins")
@SequenceGenerator(name="SEQ_LOGIN", sequenceName="seq_login_id")
public class Login implements Serializable {

	private static final long serialVersionUID = 1L;

	// The identity of logins
	@Id
	@GeneratedValue(generator="SEQ_LOGIN", strategy = GenerationType.AUTO)
	private Integer id;

	// The nick of user
	@Column(nullable = false, unique = true)
	private String nick;

	// The password of the user
	@Column(nullable = false)
	private String pass;
	
	// The user owner of this login
	@ManyToOne(cascade={CascadeType.PERSIST, CascadeType.MERGE} )
	@JoinColumn(name="user_id")
	private User user;

	// When the login was created
	@Temporal(TemporalType.TIMESTAMP)
	private Date createdAt;

	// The last time when the login was updated
	@Temporal(TemporalType.TIMESTAMP)
	private Date updatedAt;

	// The last time that user logged in the game
	@Temporal(TemporalType.TIMESTAMP)
	private Date lastLogin;

	/**
	 * Model that represents the login
	 */
	public Login() {

	}
	
	/**
	 * Model that represents the login
	 */
	public Login(String nick, String pass, User user) {
		
		this.nick = nick;
		
		this.pass = pass;
		
		this.user = user;
		
	}

	/*
	 * Begin of the getters and setters of the attributes
	 */

	public Integer getId() {

		return id;

	}

	public void setId(Integer id) {

		this.id = id;

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
	
	public User getUser() {
	
		return user;
	
	}

	public void setUser(User user) {
	
		this.user = user;
	
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
