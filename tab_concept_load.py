import config
import util
import streamlit as st

import llm_interface

def concept_load_tab():
    #Verifica conexão com a database
    if(not(config.connection)):
        st.error("No database connected!")
    else:
        st.write("Database connected!")

    #Usuário escolhe como vai importar os conceitos
    with st.expander("Select how to import concepts: ", expanded=True):
        import_option = st.radio("Select: ", 
                                ("Run a SQL Query", "Select a database table"))

    #Executa uma query
    if(import_option=="Run a SQL Query"):
        with st.expander("Run a SQL Query on the database:", expanded=True):
            form_sql_statement = st.form(key='form_sql_statement_concept')

            sql_statement = form_sql_statement.text_area("SQL Query")
            sql_submitted = form_sql_statement.form_submit_button("Run query", use_container_width=True)

            if(sql_submitted):
                config.df_query_result = util.run_query(sql_statement)
                print(config.df_query_result)
                config.table_columns_query_result = util.query_table_columns_by_table(config.df_query_result)

    
    #Escolhe diretamente uma tabela da base de dados
    if(import_option=="Select a database table"):
        with st.expander("Select the database table:", expanded=True):
            config.table_names_query_result = util.query_table_names()
            config.table = st.selectbox(label="Table", options=(config.table_names_query_result), index=None, placeholder="Table")
            config.table_columns_query_result = util.query_table_columns_by_name(config.table)

    #Seleção dos conceitos a partir da tabela
    if(config.table_columns_query_result):
        
        with st.expander("Select the concepts:", expanded=True):
            config.origin_concept = st.selectbox(label="Origin Concept", options=(config.table_columns_query_result), index=None, placeholder="Origin Concept")
            config.destination_concept = st.selectbox(label="Destiny Concept", options=(config.table_columns_query_result), index=None, placeholder="Destination Concept")

        if config.origin_concept and config.destination_concept:
            config.concepts_flag = True

        if config.concepts_flag and st.button("Generate LLM Prompts", use_container_width=True):
            config.prompt_flag = True
            config.graph_flag = True
            st.write("LLM Prompts generated!")
            
        

