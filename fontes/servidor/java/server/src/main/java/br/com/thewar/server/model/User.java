/**
 * 
 */
package br.com.thewar.server.model;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.SequenceGenerator;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

/**
 * Model that represent the user of the game
 * 
 * @author Bruno Lopes Alcantara Batista
 * 
 */
@Entity
@Table(name = "users")
@SequenceGenerator(name="SEQ_USER", sequenceName="seq_user_id")
public class User implements Serializable {

	private static final long serialVersionUID = 1L;

	// The identity of the user
	@Id
	@GeneratedValue(generator="SEQ_USER", strategy = GenerationType.AUTO)
	private Integer id;

	// The first name of user
	@Column(nullable = false)
	private String firstName;

	// The last name of user
	@Column(nullable = false)
	private String lastName;

	// The email of user
	@Column(nullable = false, unique = true)
	private String email;

	// The twitter usename of user
	@Column(nullable = true, unique = true)
	private String twitter;

	// The list of login who user have
	@OneToMany(mappedBy="user")
	private List<Login> logins;

	// When the user was created
	@Temporal(TemporalType.TIMESTAMP)
	private Date createdAt;

	// The last
	@Temporal(TemporalType.TIMESTAMP)
	private Date updatedAt;

	/**
	 * Model that represent the user of the game
	 */
	public User() {

	}

	/**
	 * Model that represent the user of the game
	 * 
	 * @param firstName
	 *            of the user
	 * @param lastName
	 *            of the user
	 * @param email
	 *            of the user
	 * @param twitter
	 *            username of the user
	 */
	public User(String firstName, String lastName, String email, String twitter) {

		this.firstName = firstName;

		this.lastName = lastName;

		this.email = email;

		this.twitter = twitter;

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

	public String getFirstName() {

		return firstName;

	}

	public void setFirstName(String firstName) {

		this.firstName = firstName;

	}

	public String getLastName() {

		return lastName;

	}

	public void setLastName(String lastName) {

		this.lastName = lastName;

	}

	public String getEmail() {

		return email;

	}

	public void setEmail(String email) {

		this.email = email;

	}

	public String getTwitter() {

		return twitter;

	}

	public void setTwitter(String twitter) {

		this.twitter = twitter;

	}

	public List<Login> getLogins() {

		return logins;

	}

	public void setLogins(List<Login> logins) {

		this.logins = logins;

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

	/*
	 * End of the getters and setters of the attributes
	 */

}
