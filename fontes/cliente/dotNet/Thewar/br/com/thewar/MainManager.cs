/**
 * \name    MainManager.cs
 * \author  Joselito Viveiros Nogueira Filho - joselitofilhoo@gmail.com
 * \date    28/12/2011
 */
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
    /// 
    /// </summary>
    public class MainManager : /*implements*/IObserver
    {
        #region Construtores
        /// <summary>
        /// Manager client's main.
        /// </summary>
        /// <param name="mainWindow_"></param>
        public MainManager(MainWindow mainWindow_)
        {
            // Instance of the communication.
            // TODO: pegar do arquivo de configuração.
            Communication = new CommunicationInterface("127.0.0.1", 1234);

            //communication = new CommunicationInterface("192.168.1.9", 1234);
            // Instance of the session.
            session = Session.getSession();

            // Reference main control.
            mainWindow = mainWindow_;

            // Adding the class itself MainManager(Observer) in Communication(Subject).
            Communication.Attach(this);
        }
        #endregion

        #region Métodos
        /**
         * \overload void IObserver::Update()
         */
        public void Update()
        {
            processResponse(Communication.SubjectState);
        }
        /// <summary>
        /// Processes the data received from the server.
        /// </summary>
        /// <param name="json">data in json format.</param>
        private void processResponse(string json)
        {
            JObject jObj = JObject.Parse(json);
            JToken jTk;

            // Searching for the type of response.
            string type = jObj.Property("type").Value.ToString();

            // Searching for the data.
            jTk = jObj.Property("data").Value;

            JsonSerializer jsonSerializer = new JsonSerializer();

            // Type: Login
            if (type.Equals("loginresponse"))
            {
                LoginResponse l = (LoginResponse)jsonSerializer.Deserialize(
                    new JTokenReader(jTk), 
                    typeof(LoginResponse));
                processLogin(l);
            }
            // Type: User Logged
            else if (type.Equals("userloggedresponse"))
            {
                UserLoggedResponse userLogged = (UserLoggedResponse)jsonSerializer.Deserialize(
                    new JTokenReader(jTk), 
                    typeof(UserLoggedResponse));
                processUserLogged(userLogged);
            }
            // Type: List Users Logged
            else if (type.Equals("listusersloggedresponse"))
            {
                ListUsersLoggedResponse listUsers = (ListUsersLoggedResponse)jsonSerializer.Deserialize(
                    new JTokenReader(jTk),
                    typeof(ListUsersLoggedResponse));
                processListUsersLogged(listUsers);
            }
        }
        /// <summary>
        /// Processes the login received from the server.
        /// </summary>
        /// <param name="loginResp">Login data</param>
        private void processLogin(LoginResponse loginResp)
        {
            if (loginResp.Status == (int)ResponseStatus.SUCCESS)
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
                mainWindow.LoginView.processResponse(loginResp);
            }
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="userLoggedResp"></param>
        private void processUserLogged(UserLoggedResponse userLoggedResp)
        {
            if (userLoggedResp.Nick != session.User.Login.Nick)
                mainWindow.GridMain.Dispatcher.Invoke(
                        System.Windows.Threading.DispatcherPriority.Normal,
                        new Action(
                            delegate()
                            {
                                // Procurando elemento da sala.
                                RoomView roomView = UIUtils.FindChild<RoomView>(mainWindow.GridMain, "RoomView");
                                if (roomView != null)
                                {
                                    session.addUsersList(userLoggedResp.Nick);

                                    // Adicionando nick na lista de usuários.
                                    roomView.ListUsers.addUser(userLoggedResp.Nick);
                                }
                                else
                                {
                                    // TODO: o que fazer quando não estiver na sala e receber essa mensagem?
                                }
                            }
                        ));
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="listUsersLoggedResp"></param>
        private void processListUsersLogged(ListUsersLoggedResponse listUsersLoggedResp)
        {
            mainWindow.GridMain.Dispatcher.Invoke(
                        System.Windows.Threading.DispatcherPriority.Normal,
                        new Action(
                            delegate()
                            {
                                // Procurando elemento da sala.
                                RoomView roomView = UIUtils.FindChild<RoomView>(mainWindow.GridMain, "RoomView");
                                if (roomView != null)
                                {
                                    foreach(string nick in listUsersLoggedResp.ListUsers)
                                    {
                                        session.addUsersList(nick);
                                        // Adicionando nick na lista de usuários.
                                        roomView.ListUsers.addUser(nick);
                                    }
                                }
                                else
                                {
                                    // TODO: o que fazer quando não estiver na sala e receber essa mensagem?
                                }
                            }
                        ));
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
