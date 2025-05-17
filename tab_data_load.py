import config
import util
import streamlit as st
import pandas as pd

def data_load_tab():

    with st.expander("Carregar dados", expanded=True):
        data_option = st.radio("Escolha como prosseguir:", 
                                ("Inserir consulta SQL", "Importar arquivo CSV"))
        
        if(data_option == "Inserir consulta SQL"):
            if(not(config.connection)):
                st.error("Sem conexão com a base de dados!")
            
            else:
                st.write("Base de dados conectada")
                form_sql_statement = st.form(key='form_sql_statement')

                sql_statement = form_sql_statement.text_area("Consulta (em SQL):")
                sql_submitted = form_sql_statement.form_submit_button("Fazer consulta", use_container_width=True)

                if sql_submitted:
                    config.df_query_result = None
                    config.flag_data_loaded = False

                    config.df_query_result = util.run_query(sql_statement)

                if config.df_query_result is not None:
                    config.flag_data_loaded = True
                    st.dataframe(config.df_query_result, use_container_width=True)
                    st.write("Tuplas no dataframe resultante:", len(config.df_query_result))
                    st.success("Consulta realizada com sucesso")

                    config.df_query_result.to_csv("Resultados_consulta.csv", index=False)
                
                else:
                    config.flag_data_loaded = False
                    st.error("Erro ao carregar consulta. Confira o comando SQL informado")

        if(data_option == "Importar arquivo CSV"):
            file = st.file_uploader("Escolha o arquivo CSV", type=["csv"])

            if file is not None:
                try:
                    config.df_query_result = pd.read_csv(file)
                    config.flag_data_loaded = True

                    st.dataframe(config.df_query_result, use_container_width = True)
                    st.write("Tuplas no dataframe resultante:", len(config.df_query_result))
                    st.success("Arquivo CSV carregado com sucesso")
                
                except Exception as error:
                    config.flag_data_loaded = False
                    st.error(f"Erro ao importar arquivo CSV {error}")
                    