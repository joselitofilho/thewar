using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace br.com.thewar.configuration
{
    /// <summary>
    /// 
    /// </summary>
    public class ConfCommunication
    {
        #region Constructors
        /// <summary>
        /// 
        /// </summary>
        public ConfCommunication()
        {
            Ip = "127.0.0.1";
            Port = 1234;
        }
        #endregion

        #region Properties
        /// <summary>
        /// 
        /// </summary>
        public string Ip { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public int Port { get; set; }
        #endregion
    }
}
