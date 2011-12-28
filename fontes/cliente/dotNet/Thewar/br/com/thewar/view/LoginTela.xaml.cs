using System;
using System.Windows;
using System.Windows.Controls;
using br.com.thewar.protocolo;
using br.com.thewar.protocol;
using br.com.thewar.lang;
using br.com.thewar.model;
using br.com.thewar;

namespace Thewar.br.com.thewar
{
    /// <summary>
    /// Interaction logic for Login.xaml
    /// </summary>
    public partial class LoginTela : UserControl
    {
        public LoginTela()
        {
            InitializeComponent();
        }

        public void processResponse(LoginResponse loginRequest)
        {
            if (loginRequest.Status != 0)
            {
                MessageBox.Show("Error codi: " + loginRequest.Status, "Login", MessageBoxButton.OK, MessageBoxImage.Error);

                // É isso mesmo! Para atualizar o botão precisa de toda essa novela!
                btLogin.Dispatcher.Invoke(
                    System.Windows.Threading.DispatcherPriority.Normal,
                    new Action(
                      delegate()
                      {
                          btLogin.IsEnabled = true;
                      }
                  ));
            }
        }

        private void btLogin_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Desabilita o botão de login.
                btLogin.IsEnabled = false;

                // Cria a requisição de login
                LoginRequest login = new LoginRequest()
                {
                    Nick = tbEmail.Text,
                    Pass = tbSenha.Text
                };

                // Adicionando usuário na sessão.
                Session.getSession().User = new User()
                {
                    Login = new Login()
                    {
                        Nick = tbEmail.Text,
                        Pass = tbSenha.Text
                    }
                };

                // Envia a requisição.
                MainManager.Communication.SendObject(login);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.StackTrace);
            }
        }
    }
}
