using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using br.com.thewar;
using Newtonsoft.Json;
using br.com.thewar.protocolo;
using Newtonsoft.Json.Linq;
using br.com.thewar.protocol;
using br.com.thewar.lang;
using br.com.thewar.model;

namespace Thewar
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            //
            Session = Session.getSession();
            //
            thiss = this;
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="json"></param>
        public static void ProcessResponse(string json)
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
                    // Removendo tela de login.
                    thiss.GridMain.Dispatcher.Invoke(
                        System.Windows.Threading.DispatcherPriority.Normal,
                        new Action(
                          delegate()
                          {
                              thiss.GridMain.Children.Remove(thiss.LoginView);
                          }
                      ));

                    // Adicionando tela de salas de espera.
                    // thiss.Child
                }
                else
                {
                    // Remove o usuário da sessão.
                    Session.User = null;
                    // Processa a resposta para a tela de login.
                    thiss.LoginView.processResponse(l);
                }
            }
        }

        #region Atributos
        /// <summary>
        /// 
        /// </summary>
        public static Session Session;
        /// <summary>
        /// Interface de comunicação com o servidor. Ela será utilizada em toda a aplicação.
        /// </summary>
        public static CommunicationInterface communication = new CommunicationInterface("127.0.0.1", 1234);
        //public static InterfaceComunicacao comunicacao = new InterfaceComunicacao("192.168.1.9", 1234);
        /// <summary>
        /// Referência estática para a janela principal.
        /// </summary>
        public static MainWindow thiss;
        #endregion
    }
}
