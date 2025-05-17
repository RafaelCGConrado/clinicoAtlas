import config 
import util
import semantic
import streamlit as st
import streamlit.components.v1 as components
from streamlit_plotly_events import plotly_events
import pandas as pd


def eda_tab():

    if config.flag_data_loaded:

        with st.expander(label="Selecione as opções do grafo", expanded=True):
            cc1, cc2, cc3, cc4 = st.columns(4)

            with cc1:
                hasSource = st.checkbox(label="Origem", value=True, disabled=True)
                config.source_node_color = st.color_picker("Cor dos vértices de origem", "#FF0000")

            with cc2:
                hasDestination = st.checkbox(label="Destino", value=True, disabled=True)
                config.destination_node_color = st.color_picker("Cor dos vértices de destino", "#FF0000")

            with cc3:
                hasMeasure = st.checkbox(label="Peso", value=False)
            
            with cc4:
                hasTimestamp = st.checkbox(label="Timestamp", value=False)

            c1, c2, c3, c4 = st.columns(4)


           
            with c1:
                if hasSource:
                    config.opt_source = st.selectbox(label="Origem", options=config.df_query_result.columns, index=min(0, len(config.df_query_result.columns)-1))
                else:
                    config.opt_source = None 
           
            with c2:
                if hasDestination:
                    config.opt_destination = st.selectbox(label="Destino", options=config.df_query_result.columns, index=min(1, len(config.df_query_result.columns)-1))
                else:
                    config.opt_destination = None

          
            with c3:
                if hasMeasure:
                    config.opt_measure = st.selectbox(label="Peso", options=config.df_query_result.columns, index=min(2, len(config.df_query_result.columns)-1))
                else:
                    config.opt_measure = None
          
            with c4:
                if hasTimestamp:
                    config.opt_timestamp = st.selectbox(label="Timestamp", options=config.df_query_result.columns, index=min(3, len(config.df_query_result.columns)-1))
                else:
                    config.opt_timestamp = None


        form_model_graph = st.form(key="model_graph")
        config.flag_use_prefix_in_graph = form_model_graph.checkbox("Modelar relacionamento entre conceitos",
                                                                    help="Adiciona o nome do atributo como prefixo aos valores modelados",
                                                                    value=True)
        
        graph_construct_submitted = form_model_graph.form_submit_button("Criar grafo", use_container_width=True)

        if graph_construct_submitted:
            semantic_label = semantic.extract_semantic_label(config.opt_source, config.opt_destination)
            st.write(config.opt_source + " " + semantic_label +" "+config.opt_destination)
           
            tgraph_columns = []
        
            for v in [config.opt_source, config.opt_destination, config.opt_measure, config.opt_timestamp]:
                if v is not None:
                    tgraph_columns.append(v)
            
            config.df_tgraph_features = util.run_t_graph(config.df_query_result[tgraph_columns],
                                                                source=config.opt_source,
                                                                destination=config.opt_destination,
                                                                measure=config.opt_measure,
                                                                timestamp=config.opt_timestamp)

        if config.df_tgraph_features is not None:
                    config.flag_features_extracted = True

                    #Tradução das features de acordo com as semânticas definidas
                    feature_mapping = {}
                    for feature in config.df_tgraph_features.columns:
                        translated_feature = semantic.extract_semantic_feature(config.opt_source, config.opt_destination, feature)
                        if (translated_feature != "undefined"):
                            feature_mapping[feature] = translated_feature


                    config.df_tgraph_features.rename(columns=feature_mapping, inplace=True)
                    config.available_features = config.df_tgraph_features.columns[1:]

                    st.success("Grafo criado com sucesso.")


    if config.df_tgraph_features is not None:
        copt_source, copt_destination, copt_measure, copt_timestamp = st.columns(4)

        with copt_source:
            st.write("Origem (out):", config.opt_source)
        with copt_destination:
            st.write("Destino (in):",  config.opt_destination)
        with copt_measure:
            st.write("Peso da aresta:", config.opt_measure)
        with copt_timestamp:
            st.write("Timestamp:",  config.opt_timestamp)


        with st.expander("Explore as características extraídas e o grafo criado", expanded=False):
            st.dataframe(config.df_tgraph_features, use_container_width=True)

            if st.checkbox("Visualizar grafo (pode demorar)", False, help="A visualização pode demorar para ser gerada para redes grandes"):
                if (config.df_tgraph_features is not None) and len(config.df_tgraph_features):
                    # Load HTML file in HTML component for display on Streamlit page
                    components.html(util.plot_interactive_graph_pyvis().read(), height=900)

        with st.expander("Visualizações 1-D", expanded=False):
        
            selected_feature = st.selectbox("Selecione a característica que deseja visualizar",
                                            options=config.available_features)
            st.write(util.get_template(selected_feature))

            c1_hist, c2_hist = st.columns(2)

            with c1_hist:
                st.write("Histograma 1-D")
                st.plotly_chart(util.plot_interactive_histogram(df=config.df_tgraph_features[config.df_tgraph_features[selected_feature] > 0],
                                                                column=selected_feature),
                                use_container_width=True)
            with c2_hist:
                st.write("Box-plot")
                st.plotly_chart(util.plot_interactive_boxplot(config.df_tgraph_features[config.df_tgraph_features[selected_feature] > 0],
                                                                column=selected_feature),
                                use_container_width=True)
            

        with st.expander("Visualizações 2-D", expanded=False):
            c1_col_opthexbin, c2_col_opthexbin, c3_col_opthexbin = st.columns([4,4,3])

            with c1_col_opthexbin:
                selected_feature_hexbin1 = st.selectbox("Selecione característica #1 que deseja visualizar",
                                                options=config.available_features)
            with c2_col_opthexbin:
                selected_feature_hexbin2 = st.selectbox("Selecione característica #2 que deseja visualizar",
                                                options=config.available_features)
            with c3_col_opthexbin:
                config.opt_logx_hexbin = st.checkbox("Log-scale no eixo x do HexBin", help="Valores serão escalados para log10(x+1)")
                config.opt_logy_hexbin = st.checkbox("Log-scale no eixo y do HexBin", help="Valores serão escalados para log10(x+1)")
            
            c1_col_hexbin, _, c2_col_hexbin = st.columns([5,1,5])
            with c1_col_hexbin:
                st.plotly_chart(util.plot_interactive_scatter(
                                        c1=selected_feature_hexbin1,
                                        c2=selected_feature_hexbin2))
            with c2_col_hexbin:
                st.pyplot(util.plot_hexbin(df=config.df_tgraph_features,
                                        c1=selected_feature_hexbin1,
                                        c2=selected_feature_hexbin2))


        with st.expander("Scatter Plots N-D", expanded=False):
            col1_scatter_matrix_options, col2_scatter_matrix_options = st.columns([5,1])

            with col1_scatter_matrix_options:
                config.columns_matrix_lasso = st.multiselect("Selecione (três ou mais) características a visualizar",
                                                             help="Selecione três ou mais características",
                                                             options=config.df_tgraph_features.columns[1:].values)
            
            with col2_scatter_matrix_options:
                config.opt_logx_scatter_matrix = st.checkbox("Log-scale no eixo x", help="Valores serão escalados para log10(x+1)")
                config.opt_logy_scatter_matrix = st.checkbox("Log-scale no eixo y", help="Valores serão escalados para log10(x+1)")

            if (len(config.columns_matrix_lasso) > 1):
                
                fig_lasso = util.plot_lasso_scatter_matrix()

                config.selected_points_lasso = plotly_events(fig_lasso, select_event=True,
                                                override_height=config.plotly_height,
                                                override_width=config.plotly_width,)
                
                if len(config.selected_points_lasso) > 0:
                    config.df_selected = pd.DataFrame(config.selected_points_lasso)
                    st.write("Nós selecionados:", len(config.selected_points_lasso))
                    st.markdown("**Características dos nós selecionados:**")
                    st.dataframe(config.df_tgraph_features.loc[config.df_selected["pointNumber"].values])

                    col_selected_points_data1, col_selected_points_data2 = st.columns(2)
                    with col_selected_points_data1:
                        st.markdown("Dados selecionados em Origem: " + str(config.opt_source))
                        st.dataframe(config.df_query_result[config.df_query_result[config.opt_source].isin(config.df_tgraph_features.loc[config.df_selected["pointNumber"].values][config.NODE_ID])])

                    with col_selected_points_data2:
                        st.markdown("Dados selecionados em Destino: " + str(config.opt_destination))
                        st.dataframe(config.df_query_result[config.df_query_result[config.opt_destination].isin(config.df_tgraph_features.loc[config.df_selected["pointNumber"].values][config.NODE_ID])])


    else:
        st.write("Carregue os dados da consulta!")

