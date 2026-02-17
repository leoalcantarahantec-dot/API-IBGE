import requests
import pandas as pd
import  streamlit as st

def pegar_nome_por_decada(nome):
        """
        Consulta a API do IBGE e retorna a frequência do nome
        agrupada por período (década).

        :param nome: Nome a ser consultado
        :return: Dicionário {periodo: frequencia}
        """
        url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"

        resultado = fazer_request(url)
        # Caso a API não retorne dados válidos
        if not resultado:
             return {}
        return {dados['periodo']: dados['frequencia'] for dados in resultado[0]['res']}
              
        

def fazer_request(url, params=None):
      """
       Realiza uma requisição HTTP GET e retorna o conteúdo
       da resposta em formato JSON.
      
      :param url: URL da requisição
      :param params: Parâmetros opcionais da requisição
      :return: JSON da resposta
      """
      try:
        resposta = requests.get(url,params=params)
        resposta.raise_for_status()
        return resposta.json()
      except requests.RequestException:
        return None

def main():
    """
    Função principal da aplicação Streamlit.
    Controla a interface, entrada do usuário,
    consulta à API e exibição dos dados.
    """
    st.title('WEb APP Nomes')
    st.write('Dados IBGE (FONTE:https://servicodados.ibge.gov.br/api/docs/nomes?versao=2 )')
    nome =st.text_input('Consulte um nome: ')
   
    if not nome:
        st.stop()
    dict_decada = pegar_nome_por_decada(nome)
    if not dict_decada:
         st.warning(f'Nome não encontrado {nome}')
         st.stop()
    df = pd.DataFrame.from_dict(dict_decada, orient= 'index')

    col1,col2 = st.columns([0.3, 0.7])
    with col1:
        st.write('frequencia por decada')
        st.dataframe(df)
    with col2:
        st.write('Evolução no tempo')
        st.line_chart(df)

if __name__== '__main__':
     main()

      