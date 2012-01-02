/*!
 * \file    Configuracao.cs
 * \author  ELO Sistemas Eletrônicos
 * \date    28 de Outubro de 2011
 */
using System.IO;
using System.Text;
using System.Xml.Serialization;
using br.com.thewar.configuration;

namespace br.com.thewar
{
    /// <summary>
    /// Singleton que representa a configuração do Kraftwerk.
    /// </summary>
    public class Configuration
    {
        #region Construtores
        /// <summary>
        /// Construtor padrão.
        /// </summary>
        protected Configuration()
        {
            // Faz nada
            inicializar();
        }
        /// <summary>
        /// Construtor que recebe o nome do arquivo.
        /// A referência da instância da classe é atualizada dentro desse contrutor.
        /// </summary>
        /// <param name="nomeArquivo"></param>
        protected Configuration(string nomeArquivo)
        {
            FileStream arquivo = null;
            try
            {
                // Tentamos abrir o arquivo na intenção de saber se o existe.
                arquivo = new FileStream(nomeArquivo, FileMode.Open);
                arquivo.Close();

                // Desserializar
                XmlSerializer serializer = new XmlSerializer(this.GetType());
                var caracteres = File.ReadAllText(nomeArquivo);
                var stream = new MemoryStream(Encoding.UTF8.GetBytes(caracteres));

                // Atualiza a instância da classe.
                _configuration = (Configuration)serializer.Deserialize(stream);

                // Serializar
                arquivo = new FileStream(nomeArquivo, FileMode.Create);
                System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(this.GetType());
                x.Serialize(arquivo, _configuration);
                arquivo.Close();
            }
            catch
            {
                // Se a exceção acontecer não existe um arquivo de configuração ainda.
                // Neste caso criamos um.

                // Inicializa as variáveis.
                inicializar();

                // Serializar
                arquivo = new FileStream(nomeArquivo, FileMode.Create);
                System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(this.GetType());
                x.Serialize(arquivo, this);
                arquivo.Close();

                // Atualiza a instância da classe.
                _configuration = this;
            }
            finally
            {
                if (arquivo != null) arquivo.Close();
            }
        }
        #endregion

        #region Métodos
        /// <summary>
        /// Retorna a instância singleton da configuração.
        /// </summary>
        /// <returns></returns>
        public static Configuration getConfiguration()
        {
            if (_configuration == null)
            {
                // A referência da classe é atualiza no próprio construtor.
                new Configuration("thewar-config.xml");
            }

            return _configuration;
        }
        
        /// <summary>
        /// Inicializa as informações padrões de Configuração.
        /// </summary>
        private void inicializar()
        {
            //
            Versao = "0.6";
            //
            Directories = new ConfDirectories();
            //
            Communication = new ConfCommunication();
        }
        #endregion

        #region Getters/Setters
        /// <summary>
        /// Versão do Kraftwerk.
        /// </summary>
        public string Versao { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public ConfDirectories Directories { get; set; }
        /// <summary>
        /// 
        /// </summary>
        public ConfCommunication Communication { get; set; }
        #endregion

        #region Atributos
        /// <summary>
        /// Singleton da configuração.
        /// </summary>
        private static Configuration _configuration;
        #endregion
    }
}
