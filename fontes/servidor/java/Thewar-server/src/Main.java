import java.io.IOException;

import br.com.thewar.servidor.Servidor;

public class Main {

	public static void main(String args[]) {
		Servidor ic;
		try {
			ic = new Servidor();
			ic.run();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
