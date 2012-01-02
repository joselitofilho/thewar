﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using br.com.thewar.model;
using br.com.thewar.communication;

namespace br.com.thewar.lang
{
    /// <summary>
    /// Singleton.
    /// </summary>
    public class Session
    {
        #region Contrutores
        /// <summary>
        /// Construtor padrão.
        /// </summary>
        private Session()
        {
            //
            UsersList = new List<string>();
            //
            Configuration = Configuration.getConfiguration();
        }
        #endregion

        #region Métodos
        /// <summary>
        /// Verifica se existe alguma instância de Session. Se não existir
        /// ela é criada e retornada. Caso contrário, ela apenas é retornada.
        /// </summary>
        /// <returns>Singleton da classe Session.</returns>
        public static Session getSession()
        {
            if (session == null)
            {
                session = new Session();
            }

            return session;
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="nick"></param>
        public void addUsersList(string nick)
        {
            // O nick do jogador atual não é adicionado na lista de usuários.
            if (nick != User.Login.Nick && !UsersList.Contains(nick))
            {
                UsersList.Add(nick);
            }
        }
        #endregion

        #region Atributos
        /// <summary>
        /// Singleton desta classe.
        /// </summary>
        private static Session session;
        #endregion

        #region Propriedades
        /// <summary>
        /// 
        /// </summary>
        public User User { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public List<string> UsersList { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public Configuration Configuration { get; set; }
        #endregion
    }
}
