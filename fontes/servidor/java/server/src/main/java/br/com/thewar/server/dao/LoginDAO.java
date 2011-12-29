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

import br.com.thewar.server.model.Login;

/**
 * @author bruno
 * 
 */
public class LoginDAO implements GenericDAO<Login> {

	private Session session;

	private Transaction transaction;

	private Logger logger;

	private Login login;

	private List<Login> logins;

	private Criteria criteria;

	private static LoginDAO instance;

	/**
	 * Class that mapping the Login object with the database
	 */
	private LoginDAO() {

		logger = Logger.getLogger(LoginDAO.class.getName());

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#save(java.lang.Object)
	 */
	public void save(Login obj) {

		try {

			// Set the date on fields createdAt and updatedAt
			setDate(obj);

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, save or update the login and commit
			transaction.begin();
			session.saveOrUpdate(obj);
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "Login " + obj.getNick()
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
	public void delete(Login obj) {

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, save or update the login and commit
			transaction.begin();
			session.delete(obj);
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "Login " + obj.getNick() + " was deleted.");

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
	public Login load(Integer id) {

		// setting null
		login = null;

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, get the Login and commit
			transaction.begin();
			criteria = session.createCriteria(Login.class);
			criteria.add(Restrictions.idEq(id));
			login = (Login) criteria.uniqueResult();
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "Listing the Login " + login.getNick());

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

		// Return a login
		return login;

	}

	/**
	 * Method that return a login
	 * 
	 * @param nick
	 *            of login
	 * @param password
	 *            of login
	 * @return a Login object
	 */
	public Login load(String nick, String password) {

		// setting null
		login = null;

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, get the login and commit
			transaction.begin();
			criteria = session.createCriteria(Login.class);
			criteria.add(Restrictions.eq("nick", nick));
			criteria.add(Restrictions.eq("pass", password));
			login = (Login) criteria.uniqueResult();
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			if (login != null) {

				logger.log(Level.INFO, "Listing the Login " + login.getNick());

			}

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

		// Return a login
		return login;

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#loadAll()
	 */
	@SuppressWarnings("unchecked")
	public List<Login> loadAll() {

		// setting null
		logins = null;

		try {

			// Get a hibernate session
			session = HibernateUtil.getSessionFactory().openSession();

			// Create a transaction
			transaction = session.beginTransaction();

			// Begin the transaction, get the login and commit
			transaction.begin();
			criteria = session.createCriteria(Login.class);
			logins = criteria.list();
			transaction.commit();

			// Close the session
			session.close();

			// Register the action on the log
			logger.log(Level.INFO, "Listing all logins");

		} catch (HibernateException e) {

			// Register the error on the log
			logger.log(Level.SEVERE, e.getMessage());

		}

		// Return a list of logins
		return logins;

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see br.com.thewar.server.dao.GenericDAO#setDate(java.lang.Object)
	 */
	public void setDate(Login obj) {

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

	/**
	 * Return a instance of LoginDAO
	 * 
	 * @return a instance of LoginDAO
	 */
	public static LoginDAO getInstance() {

		if (instance == null) {

			instance = new LoginDAO();

		}

		return instance;

	}

}
