package br.com.thewar.model;

public class GenericModel {

	public GenericModel() {
		
	}
	
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public Object getData() {
		return data;
	}
	public void setData(Object data) {
		this.data = data;
	}

	private String type;
	private Object data;
	
}
