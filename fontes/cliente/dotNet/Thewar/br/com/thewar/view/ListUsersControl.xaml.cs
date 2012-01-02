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

namespace Thewar.br.com.thewar.view
{
    /// <summary>
    /// Interaction logic for ListUsersControl.xaml
    /// </summary>
    public partial class ListUsersControl : UserControl
    {
        public ListUsersControl()
        {
            InitializeComponent();
        }

        public void addUser(string nick)
        {
            ListViewItem item = new ListViewItem();
            item.Height = 30;
            item.Content = nick;

            if (!ListViewUsers.Items.Contains(item))
            {
                ListViewUsers.Items.Add(item);
            }
        }

        public void updateList(List<string> list)
        {
            //listUsers = list;
        }

        //private List<string> listUsers;
    }
}
