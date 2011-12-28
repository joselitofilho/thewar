using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Thewar;
using br.com.thewar.communication;
using br.com.thewar.lang;

namespace br.com.thewar
{
    public class MainManager
    {

        #region Atributos
        /// <summary>
        /// 
        /// </summary>
        public static Session Session;
        /// <summary>
        /// Interface de comunicação com o servidor. Ela será utilizada em toda a aplicação.
        /// </summary>
        public static CommunicationInterface communication = new CommunicationInterface("127.0.0.1", 1234);
        //public static CommunicationInterface communication = new CommunicationInterface("192.168.1.9", 1234);
        /// <summary>
        /// Referência estática para a janela principal.
        /// </summary>
        public static MainWindow thiss;
    }
}
