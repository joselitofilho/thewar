var gpscheck = gpscheck || {};
gpscheck.web = gpscheck.web || {};

gpscheck.web.Cookie = function() {
    /** 
     * Função para criar o cookie.
     * Para que o cookie seja destruído quando o brawser for fechado, basta passar 0
     * no parametro lngDias.
     */    
    this.cria = function(strCookie, strValor, lngDias) {
        var dtmData = new Date();
 
        if(lngDias)
        {
            dtmData.setTime(dtmData.getTime() + (lngDias * 24 * 60 * 60 * 1000));
            var strExpires = "; expires=" + dtmData.toGMTString();
        }
        else
        {
            var strExpires = "";
        }
        document.cookie = strCookie + "=" + strValor + strExpires + "; path=/";    
    };
    
    /**
     * Função para ler o cookie.
     */
    this.le = function(strCookie) {
        var strNomeIgual = strCookie + "=";
        var arrCookies = document.cookie.split(';');
     
        for(var i = 0; i < arrCookies.length; i++)
        {
            var strValorCookie = arrCookies[i];
            while(strValorCookie.charAt(0) == ' ')
            {
                strValorCookie = strValorCookie.substring(1, strValorCookie.length);
            }
            if(strValorCookie.indexOf(strNomeIgual) == 0)
            {
                return strValorCookie.substring(strNomeIgual.length, strValorCookie.length);
            }
        }
        return null;
    };
     
    /**
     * Função para excluir o cookie desejado.
     */
    this.exclui = function(strCookie) {
        this.cria(strCookie, '', -1);
    };
};
