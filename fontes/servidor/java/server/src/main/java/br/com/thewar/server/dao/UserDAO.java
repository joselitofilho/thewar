/**
 * 
 */
package br.com.thewar.server.dao;

import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.hibernate.Criteria;
import org.hibernate.HibernateException;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.criterion.Restrictions;

import br.com.thewar.server.model.User;

/**
 * @author Bruno Lopes Alcantara Batista
 * 
 */
public class UserDAO implements GenericDAO<User> {

	private Session session;

	private Transaction transaction;

	private Logger logger;

	private User user;

	private List<User> users;

	private Criteria criteria;

	/**
	 * Class that mapping the User object with the database
	 */
	public UserDAO() {

		logger = Logger.getLogger(UserDAO.class.getName());

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#save(java.lang.Object)
	 */
	public void save(User obj) {

		try {

			// Set the date on fields createdAt and updatedAt
			setDate(obj);

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, save or update the user and commit
			transaction.begin();
			session.saveOrUpdate(obj);
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "User " + obj.getFirstName()
					+ " was saved or updated.");

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#delete(java.lang.Object)
	 */
	public void delete(User obj) {

		try {

			setDate(obj);

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, delete the user and commit
			transaction.begin();
			session.delete(obj);
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "User " + obj.getFirstName()
					+ " was deleted.");

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#load(java.lang.Integer)
	 */
	public User load(Integer id) {

		// setting null
		user = null;

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, get the user and commit
			transaction.begin();
			criteria = session.createCriteria(User.class);
			criteria.add(Restrictions.idEq(id));
			user = (User) criteria.uniqueResult();
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "List the user " + user.getFirstName());

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

		// Return a users
		return user;

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#loadAll()
	 */
	@SuppressWarnings("unchecked")
	public List<User> loadAll() {

		// setting null
		users = null;

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, get the user and commit
			transaction.begin();
			criteria = session.createCriteria(User.class);
			users = criteria.list();
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "Listing the all users");

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

		// Return a list of users
		return users;

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#setDate(java.lang.Object)
	 */
	public void setDate(User obj) {

		Date date = new Date();

		// Verify if the obj is new and add the createdAt value and updatedAt
		// value
		if (obj.getId() == null) {

			obj.setCreatedAt(date);

			obj.setUpdatedAt(date);

		} else {

			obj.setUpdatedAt(date);

		}

		date = null;

	}

}
