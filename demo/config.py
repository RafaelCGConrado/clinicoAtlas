from sqlalchemy import create_engine

# database connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/incordb') 
connection = engine.connect()


# data
df_query_all_tables = None
df_query_result = None
df_tgraph_features = None

available_features = None 
available_features_translate = None
NxGraph = None 

df_query_supervision = None 
df_tgraph_features_supervision = None


#flag
flag_data_loaded = None
flag_use_prefix_in_graph = False


#Graph config
opt_source = None
opt_destination = None 
opt_timestamp = None
opt_measure = None
source_node_color = None
destination_node_color = None

#io
feature_file_path = None

#plot
cmap = "rainbow"
cmap_colorshade = "jet"
plotly_width = "100%"
plotly_height = 800

columns_matrix_lasso = []
selected_points_lasso = []
df_selected = None

opt_logx_hexbin = False
opt_logy_hexbin = False

opt_logx_scatter_matrix = False
opt_logy_scatter_matrix = False



NODE_ID = "node_ID"

concepts_flag = None
prompt_flag = None
relationship_label_flag = None
graph_flag = None
graph_add_flag = None

#table
df_query_result = None
table_names_query_result = None
table_columns_query_result = None
table = None

#Graph
NxGraph = None
KGraph = None 

#concepts
origin_concept = None
destination_concept = None

#prompt
relationship_prompt_text = None
feature_prompt_text = None

#llm model
model = "gemma:latest"
relationship_prompts = "no_shot_complex_prompt"
features_prompts = "initial_template"

#relationship label
concepts_relationship_label = " relates to " #placeholder
concepts_list = []

#node features
selected_feature = None
feature_response = " "

features = ["in_degree",
            "out_degree",
            "in_average_IAT",
            "out_average_IAT",
            "weighted_in_degree",
            "weighted_out_degree",
            "core_number"]

knowledge_dict = {
    
}

features_list = []


