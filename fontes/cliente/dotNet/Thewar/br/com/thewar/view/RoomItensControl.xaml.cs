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
using br.com.thewar.protocol.request;
using br.com.thewar.lang;
using br.com.thewar;

namespace Thewar.br.com.thewar.view
{
    /// <summary>
    /// Interaction logic for RoomItensControl.xaml
    /// </summary>
    public partial class RoomItensControl : UserControl
    {
        public RoomItensControl()
        {
            InitializeComponent();
        }

        private void TextBlock_MouseUp(object sender, MouseButtonEventArgs e)
        {
            // Instância da sessão.
            Session session = Session.getSession();

            // É verificado se existe alguma requisição (RoomChangeRequest) na sessão pendente.
            // Caso não exista, a requisição é enviada ao servidor e colocada na sessão para
            // posteriormente ser processada, quando o servidor responder.
            if (!session.ContainsKey("RoomChangeReq"))
            {
                // Extrai as informações do x:Name do TextBlock na forma rX_pY.
                // r: Id da sala            X: Valor correspondente
                // p: Posição na sala       Y: Valor correspondente
                string roomPositionStr = ((TextBlock)sender).Name; /*rX_pY*/
                int roomId = Convert.ToInt32(roomPositionStr.Substring(1, roomPositionStr.LastIndexOf('_') - 1));
                int position = Convert.ToInt32(roomPositionStr.Substring(roomPositionStr.LastIndexOf('_') + 2));

                // Cria a requisição para o servidor.
                RoomChangeRequest roomChangeReq = new RoomChangeRequest()
                {
                    Id = roomId,
                    Pos = position
                };

                // Atualiza a requisição na sessão.
                session["RoomChangeReq"] = roomChangeReq;

                // Send the request to the server.
                MainManager.Communication.SendObject(roomChangeReq);
            }
        }
    }
}
