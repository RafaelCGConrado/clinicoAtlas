import sys
import config

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyvis.network import Network
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.colors 
import matplotlib.patches as patches

import streamlit as st

sys.path.insert(0, "tgraph")
from tgraph import TGraph, fn

plt.rcParams.update({'font.size': 12})
figsize=[8, 6]


def run_query(sql_statement):
    try:
        df_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        return df_query_result

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None



def run_t_graph(df, source, destination, measure, timestamp):
    print(source, destination, measure, timestamp)

    if config.flag_use_prefix_in_graph: # Use prefix
        df[source] = source + '_' + df[source].map(str)
        df[destination] = destination + '_' + df[destination].map(str)

    my_tgraph = TGraph(#filename=file,
                       df,
                       source=source,
                       destination=destination,
                       measure=measure,
                       timestamp=timestamp)
    
    if timestamp is not None:
        for prefix in ['in_', 'out_']:
            for iat_feature in [fn.AVG_IAT, fn.MEDIAN_IAT, fn.MIN_IAT, fn.MAX_IAT, fn.STD_IAT, fn.QUANT25_IAT, fn.QUANT50_IAT, fn.QUANT75_IAT]:
                # my_tgraph.data_network.df_nodes[prefix+iat_feature] = pd.to_datetime(my_tgraph.data_network.df_nodes[prefix+iat_feature], errors='coerce').dt.days.astype('int16')
                my_tgraph.data_network.df_nodes[prefix+iat_feature] = my_tgraph.data_network.df_nodes[prefix+iat_feature].values.astype('timedelta64[D]').astype(int)
            

    config.NxGraph = my_tgraph.data_network.G
    my_tgraph.data_network.df_nodes.to_csv(config.feature_file_path, index=False)

    print(my_tgraph.data_network.df_nodes.head())

    # Return tgraph features
    return my_tgraph.data_network.df_nodes


def plot_interactive_histogram(df=config.df_tgraph_features, column=None, nbins=10):
    fig_interactive_histogram = px.histogram(df, x = column, nbins=nbins)
    fig_interactive_histogram.update_layout(
                template="seaborn",
            )
    return fig_interactive_histogram


def plot_interactive_boxplot(df=config.df_tgraph_features, column=None):
    fig_interactive_boxplot = px.box(df, x = column, points="all",
                                     hover_data={config.NODE_ID},)
    fig_interactive_boxplot.update_layout(
                template="seaborn",
            )
    
    return fig_interactive_boxplot


def plot_static_histogram(df=config.df_tgraph_features, column=None, nbins=10):
    # Density normalizes the inputs by the total number of counts
    fig_histogram = plt.figure(figsize=[5, 3])
    plt.hist(df[column], bins=nbins, density=True, color="dodgerblue")
    plt.title("Histograma - " + str(column).replace("_", " "))
    plt.xlabel(str(column).replace("_", " "))
    plt.ylabel("Frequência")

    return fig_histogram


def plot_hexbin(df=config.df_tgraph_features, c1=None, c2=None,
                                c1_name=None, c2_name=None):
    """
    Plot hexbin with selected features
    """

    c1_name = c1.replace('_', ' ') if c1_name is None else c1_name
    c2_name = c2.replace('_', ' ') if c2_name is None else c2_name
    
    fig_hexbin, ax = plt.subplots(figsize=figsize)
    if config.opt_logx_hexbin and config.opt_logy_hexbin:
        img = ax.hexbin(np.log10(df[c1]+1),
                        np.log10(df[c2]+1),
                        cmap=config.cmap, mincnt=1, bins='log')
        ax.set_xlabel(c1_name + ' — log10(x+1)')
        ax.set_ylabel(c2_name + ' — log10(x+1)')
    else:
        img = ax.hexbin(df[c1],
                        df[c2],
                        cmap=config.cmap, mincnt=1, bins='log')
        ax.set_xlabel(c1_name)
        ax.set_ylabel(c2_name)
    
    cb = plt.colorbar(img, ax=ax)
    cb.set_label("log10(N)")
    ax.grid(True)

    return fig_hexbin


def plot_interactive_scatter(c1=None, c2=None):
    """
    Plot hexbin with selected features
    """
    df=config.df_tgraph_features
    
    fig_interactive_scatter = px.scatter(df, x=c1, y=c2,
                                         hover_data={config.NODE_ID},
                                        #  trendline="ols"
                                         )
    fig_interactive_scatter.update_traces(marker_size=10)

    return fig_interactive_scatter


def plot_lasso_scatter_matrix():
    """
    Plot interactive scatter plot with the selected columns as features

    """
    df=config.df_tgraph_features
    
    # truecolor = '#f95a10'
    falsecolor = 'blue'
    # linecolor = 'white'
    
    dimensions=[]
    for c in config.columns_matrix_lasso:
        # Construct dict with column names and labels
        dimensions.append(dict(label=c.replace('_', ' '),# + ' — log10(x+1)',
                          values=df[c]))
                        # values=np.log10(df[c]+1)))

    colors = pd.Series(data=[falsecolor] * len(df))
    
    fig_matrix_lasso = go.Figure(data=go.Splom(
            dimensions = dimensions,
            customdata = df[config.NODE_ID],
            hovertemplate="<br>".join([
                        "%{xaxis.title.text}: %{x}",
                        "%{yaxis.title.text}: %{y}",
                        "hash: %{customdata}",
            ]),
            showlegend=False, #Show legend entries later on!
            showupperhalf=False, # remove plots in the diagonal
            marker=dict(color=list(colors),
                        showscale=False,
                        # line_color=linecolor,
                        line_width=0.8,
                        size=8,
                        opacity=0.5
            ),
    ))
    
    fig_matrix_lasso.update_traces(
                # unselected_marker=dict(opacity=0.1, size=10),
                # selected_marker=dict(size=15, opacity=0.9),
                selector=dict(type='splom'),
                diagonal_visible=False)
    
    fig_matrix_lasso.update_layout(
        # title='Matriz de plots',
        dragmode='select',
        hovermode='closest',
        template="seaborn",
    ) 
    
    return fig_matrix_lasso


def plot_interactive_graph_pyvis():
    nt = Network(height='800px',
                 width='100%',
                 select_menu=True,
                 cdn_resources='remote'
                 )

    # Use node degree as node size
    nx.set_node_attributes(config.NxGraph, dict(config.NxGraph.degree()), 'size')

    nt.from_nx(config.NxGraph)

    #nt.show_buttons(filter_=['physics'])
    nt.save_graph('Graph.html')

    HtmlFile = open(f'Graph.html', 'r', encoding='utf-8')
    return HtmlFile

def get_template(feature_name):
    template_text = ""
    if feature_name == "in_degree":
        template_text = "Intuição: Número de valores diferentes em \'" + str(config.opt_source) + "\' conectados a cada valor em \'" + str(config.opt_destination) + "\'"
    elif feature_name == "out_degree":
        template_text = "Intuição: Número de valores diferentes em \'" + str(config.opt_destination) + "\' conectados por cada valor em \'" + str(config.opt_source) + "\'"
    elif feature_name == "weighted_in_degree":
        template_text = "Intuição: Número de vezes em que \'" + str(config.opt_source) + "\' conectou-se a \'" + str(config.opt_destination) + "\'"
    elif feature_name == "weighted_out_degree":
        template_text = "Intuição: Número de vezes em que \'" + str(config.opt_destination) + "\' foi conectado por \'" + str(config.opt_source) + "\'"
    

    return template_text


def run_query(sql_statement):
    try:
        df_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        return df_query_result

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None

#list the name of all tables in database
def query_table_names():
    sql_statement = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'omop5';"
    
    try:
        table_names_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        return table_names_query_result

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None

#list table columns 
def query_table_columns_by_name(table_name):
    sql_statement = f"""SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}'
                        AND table_schema = 'omop5';
                        """
    
    try:
        table_columns_query_result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        # print(f"Query Result: {table_columns_query_result}")
        columns = table_columns_query_result['column_name'].tolist()
        return columns

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return None

def query_table_columns_by_table(table):
    columns = table.columns.tolist()
    return columns

#list all tables and columns name
def query_all_tables_and_columns():
    sql_statement = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'omop5'
    ORDER BY table_name, ordinal_position;    
    """

    try:
        result = pd.read_sql(sql_statement, con=config.connection)
        print("Consulta realizada com sucesso")
        tables_and_columns = result.groupby('table_name')['column_name'].apply(list).to_dict()
        return tables_and_columns

    except Exception as ex:
        print(f'Erro ao realizar a consulta: {ex}')
        try:
            config.connection.rollback()
        except Exception as rollback_ex:
            print("Erro no rollback")
        return {}

def write_concept_relationship():
    st.write(config.origin_concept +' '+ config.concepts_relationship_label +' '+ config.destination_concept)


def add_to_concept_list():
    triple = {
        "Origin Concept": config.origin_concept,
        "Relationship Label": config.concepts_relationship_label,
        "Destination Concept": config.destination_concept
    }
    config.concepts_list.append(triple)

#Add origin/destination pair to features dictionary
def add_feature_pair(origin_concept, destination_concept):
    config.features_dict[(origin_concept, destination_concept)] = {
        "in_degree": " ",
        "out_degree": " ",
        "in_average_IAT": " ",
        "out_average_IAT": " ",
        "weighted_in_degree": " ",
        "weighted_out_degree": " ",
        "core_number": " "
    }

#Add feature name --> feature meaning to features dictionary
def add_to_features_dict(origin_concept, destination_concept, feature_name, feature_meaning):
    if(origin_concept, destination_concept) not in config.features_dict:
        add_feature_pair(origin_concept, destination_concept)
    
    config.features_dict[(origin_concept, destination_concept)][feature_name] = feature_meaning


#Generate Knowledge/Conceptual Graph
def generate_graph():
    G = nx.Graph()
    config.NxGraph = G 

#Add related nodes to knowledge graph
def add_node():
    config.NxGraph.add_node(config.origin_concept)
    config.NxGraph.add_node(config.destination_concept)
    config.NxGraph.add_edge(config.origin_concept, config.destination_concept,
                            label=config.concepts_relationship_label)

def plot_graph():
    nt = Network("750px", width="100%", notebook=True)
    nt.from_nx(config.NxGraph)

    for node in nt.nodes:
        node['size']= 50
        node['color'] = "#FF0000"

    nt.repulsion(node_distance=100, spring_strength=0.05, damping=0.09)

    nt.show("nx.html")
    st.components.v1.html(open("nx.html").read(), height=300, width=950)
