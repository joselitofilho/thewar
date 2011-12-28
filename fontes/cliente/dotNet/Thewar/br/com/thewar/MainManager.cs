using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Thewar;
using br.com.thewar.communication;
using br.com.thewar.lang;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using br.com.thewar.protocol;
using Thewar.br.com.thewar.view;
using br.com.thewar.protocol.response;
using br.com.thewar.util;

namespace br.com.thewar
{
    /// <summary>
    /// Singleton
    /// </summary>
    public class MainManager : /*implements*/IObserver
    {
        #region Construtores
        /// <summary>
        /// 
        /// </summary>
        /// <param name="mainWindow_"></param>
        public MainManager(MainWindow mainWindow_)
        {
            Communication = new CommunicationInterface("127.0.0.1", 1234);
            //communication = new CommunicationInterface("192.168.1.9", 1234);
            session = Session.getSession();
            mainWindow = mainWindow_;

            Communication.Attach(this);
        }
        #endregion

        #region Métodos
        /// <summary>
        /// 
        /// </summary>
        public void Update()
        {
            processResponse(Communication.SubjectState);
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="json"></param>
        private void processResponse(string json)
        {
            JObject jObj = JObject.Parse(json);
            JToken jTk;

            // Descobrindo o tipo da resposta
            string tipo = jObj.Property("type").Value.ToString();

            // Pegando o campo data com os atributos do objeto.
            jTk = jObj.Property("data").Value;

            JsonSerializer serializer = new JsonSerializer();

            // Login
            if (tipo.Equals("loginresponse"))
            {
                LoginResponse l = (LoginResponse)serializer.Deserialize(new JTokenReader(jTk), typeof(LoginResponse));
                if (l.Status == 0)
                {
                    mainWindow.GridMain.Dispatcher.Invoke(
                        System.Windows.Threading.DispatcherPriority.Normal,
                        new Action(
                          delegate()
                          {
                              // Removendo tela de login.
                              mainWindow.GridMain.Children.Remove(mainWindow.LoginView);

                              // Adicionando tela de salas de espera.
                              RoomView roomView = new RoomView();
                              roomView.Name = "RoomView";

                              mainWindow.GridMain.Children.Add(roomView);
                          }
                      ));
                }
                else
                {
                    // Remove o usuário da sessão.
                    session.User = null;
                    // Processa a resposta para a tela de login.
                    mainWindow.LoginView.processResponse(l);
                }
            }
            else if (tipo.Equals("userloggedresponse"))
            {
                UserLoggedResponse userLogged = (UserLoggedResponse)serializer.Deserialize(new JTokenReader(jTk), typeof(UserLoggedResponse));

                if (userLogged.Nick != session.User.Login.Nick)
                    mainWindow.GridMain.Dispatcher.Invoke(
                            System.Windows.Threading.DispatcherPriority.Normal,
                            new Action(
                                delegate()
                                {
                                    // Procurando elemento da sala.
                                    RoomView roomView = UIUtils.FindChild<RoomView>(mainWindow.GridMain, "RoomView");
                                    if (roomView != null)
                                    {
                                        session.addUsersList(userLogged.Nick);

                                        // Adicionando nick na lista de usuários.
                                        roomView.ListUsers.addUser(userLogged.Nick);
                                    }
                                    else
                                    {
                                        // TODO: o que fazer quando não estiver na sala e receber essa mensagem?
                                    }
                                }
                            ));
            }
        }
        #endregion

        #region Atributos
        /// <summary>
        /// Interface de comunicação com o servidor. Ela será utilizada em toda a aplicação.
        /// </summary>
        public static CommunicationInterface Communication { get; set; }
        /// <summary>
        /// 
        /// </summary>
        private Session session;
        /// <summary>
        /// Referência estática para a janela principal.
        /// </summary>
        private MainWindow mainWindow;
        #endregion
    }
}
