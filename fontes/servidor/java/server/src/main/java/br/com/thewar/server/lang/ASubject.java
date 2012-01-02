package br.com.thewar.server.lang;

import java.util.ArrayList;
import java.util.List;

public abstract class ASubject {
	
	//
	private List<IObserver> list = new ArrayList<IObserver>();
	//
	private String subjectState;

	/**
	 * 
	 * @param observer
	 */
	public void Attach(IObserver observer) {
		list.add(observer);
	}

	/**
	 * 
	 * @param observer
	 */
	public void Detach(IObserver observer) {
		list.remove(observer);
	}

	/**
	 * 
	 */
	public void Notify() {
		for (IObserver ob : list) {
			ob.Update();
		}
	}
	
	/**
	 * 
	 * @param subjectState
	 */
	public void Notify(String subjectState) {
		this.subjectState = subjectState;
		
		for (IObserver ob : list) {
			ob.Update();
		}
	}
	
	public String getSubjectState() {
		return subjectState;
	}
	
	public void setSubjectState(String subjectState) {
		this.subjectState = subjectState;
	}
}
