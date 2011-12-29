using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace br.com.thewar.lang
{
    /// <summary>
    /// 
    /// </summary>
    public abstract class ASubject
    {
        #region Métodos
        /// <summary>
        /// 
        /// </summary>
        /// <param name="observer"></param>
        public void Attach(IObserver observer)
        {
            listObservers.Add(observer);
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="observer"></param>
        public void Detach(IObserver observer)
        {
            listObservers.Remove(observer);
        }
        /// <summary>
        /// 
        /// </summary>
        public void Notify()
        {
            foreach (IObserver o in listObservers)
            {
                o.Update();
            }
        }
        #endregion

        #region Atributos
        /// <summary>
        /// 
        /// </summary>
        private List<IObserver> listObservers = new List<IObserver>();
        #endregion

        #region Propriedades
        /// <summary>
        /// 
        /// </summary>
        public string SubjectState { get; set; }
        #endregion
    }
}
