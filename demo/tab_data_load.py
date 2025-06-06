import config
import util
import streamlit as st
import pandas as pd

def data_load_tab():

    with st.expander("Load Data", expanded=True):    
        if(not(config.connection)):
            st.error("No connection with the database!")
        
        else:
            st.write("Database Connected")
            form_sql_statement = st.form(key='form_sql_statement')

            sql_statement = form_sql_statement.text_area("Query (in SQL):")
            sql_submitted = form_sql_statement.form_submit_button("Run Query", use_container_width=True)

            if sql_submitted:
                config.df_query_result = None
                config.flag_data_loaded = False

                config.df_query_result = util.run_query(sql_statement)

            if config.df_query_result is not None:
                config.flag_data_loaded = True
                st.dataframe(config.df_query_result, use_container_width=True)
                st.write("Tuples in the resulting dataframe:", len(config.df_query_result))
                st.success("Query successfully completed.")

                config.df_query_result.to_csv("query_results.csv", index=False)
            
            else:
                config.flag_data_loaded = False
                st.error("Error while running the query. Check the provided SQL command.")
