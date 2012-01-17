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
using Thewar.br.com.thewar.view;
using br.com.thewar.protocol.response;
using br.com.thewar.util;
using br.com.thewar.communication;
using System.Diagnostics;

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
            mainManager = new MainManager(this);
        }

        #region Atributos
        /// <summary>
        /// 
        /// </summary>
        private MainManager mainManager;
        #endregion

        private void Window_Closed(object sender, EventArgs e)
        {
            // Mata a aplicação pois as threads que eram criadas no decorrer da aplicação
            // não estavam sendo fechadas quando a aplicação fechava normalmente.
            Process.GetCurrentProcess().Kill();
        }
    }
}
