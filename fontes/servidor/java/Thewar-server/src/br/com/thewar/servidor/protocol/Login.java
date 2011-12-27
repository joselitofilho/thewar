/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package br.com.thewar.servidor.protocol;

/**
 *
 * @author usuario
 */
public class Login {

	public enum CodigoResposta
	{
		DESCONHECIDO(-1),
		SUCESSO(0),
		USUARIO_JA_ESTA_LOGADO(1),
		USUARIO_NAO_ESTA_DEVIDAMENTE_CADASTRADO(2);
		
		private int id;
		CodigoResposta(int id)
		{
			this.id = id;
		}
		
		public int Codigo() {
			return id;
		}
	}
	
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

	private String nick;
    private String pass;
}
