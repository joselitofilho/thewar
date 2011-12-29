/**
 * 
 */
package br.com.thewar.server.dao;

import java.util.List;

/**
 * GenericDAO that define the main methods
 * 
 * @author Bruno Lopes Alcantara Batista
 *
 */
public interface GenericDAO<T> {

	/**
	 * Method that save or update a object
	 * @param obj to be save or update
	 */
	public void save(T obj);
	
	/**
	 * Method that delete a object
	 * @param obj to be deleted
	 */
	public void delete(T obj);
	
	/**
	 * Method that return a object 
	 * @param id of object
	 * @return a object
	 */
	public T load(Integer id);
	
	/**
	 * Methos that list all object
	 * @return list of all objects
	 */
	public List<T> loadAll();
	
}
