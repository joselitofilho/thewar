using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Threading;
using Thewar;
using System.Xml;
using Newtonsoft.Json;
using br.com.thewar.protocolo;
using Newtonsoft.Json.Linq;
using br.com.thewar.lang;

namespace br.com.thewar.communication
{
    /// <summary>
    /// Interface de comunicação entre o cliente e servidor. Utiliza-se o protocolo
    /// TCP/IP numa comunicação assincrona.
    /// </summary>
    public class CommunicationInterface : /*extends*/ASubject
    {
        #region Construtores
        /// <summary>
        /// Construtor que recebe o ip e porta que será criado o cliente.
        /// </summary>
        /// <param name="ip"></param>
        /// <param name="port"></param>
        public CommunicationInterface(string ip, int port)
        {
            client = new TcpClient();
            client.Connect(ip, port);
            data = new byte[dataSize];

            //
            client.GetStream().BeginRead(data, 0, dataSize, ReceiveMessage, null);
            //
            Thread.Sleep(200);
        }
        #endregion

        #region Métodos
        /// <summary>
        /// Serializa um objeto no formato JSON e envia para o servidor.
        /// </summary>
        /// <param name="objeto">Instância do objeto a ser serializado.</param>
        public void SendObject(object objeto)
        {
            // Criá-se uma instância do objeto genérico.
            GenericObject genericObj = new GenericObject()
            {
                Type = objeto.GetType().Name.ToString(),
                Data = objeto
            };

            // Serializa o objeto no formato JSON.
            string json = JsonConvert.SerializeObject(genericObj);
            // Envia a string gerada.
            SendMessage(json.ToLower());
        }
        /// <summary>
        /// Send message to the server.
        /// </summary>
        /// <param name="message"></param>
        public void SendMessage(string message)
        {
            try
            {
                NetworkStream netStr = client.GetStream();
                byte[] Data = System.Text.Encoding.ASCII.GetBytes(message);
                netStr.Write(Data, 0, Data.Length);
                netStr.Flush();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }
        /// <summary>
        /// Receive message from the server. 
        /// </summary>
        /// <param name="ar"></param>
        public void ReceiveMessage(IAsyncResult ar)
        {
            int bufferLength;
            try
            {
                bufferLength = client.GetStream().EndRead(ar);
                string message = (System.Text.Encoding.ASCII.GetString(data, 0, bufferLength)).ToString();

                SubjectState = message;
                Notify();

                // Continua lendo do servidor.
                client.GetStream().BeginRead(data, 0, dataSize, ReceiveMessage, null);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }
        #endregion

        #region Atributos
        /// <summary>
        /// Instância do socket para comunicação com o servidor.
        /// </summary>
        private TcpClient client;
        /// <summary>
        /// Utilizado para recebimento dos dados vindos do servidor.
        /// </summary>
        private byte[] data;
        /// <summary>
        /// Tamanho máximo de dados a receber do servidor.
        /// </summary>
        private int dataSize = 102400;
        #endregion
    }
}