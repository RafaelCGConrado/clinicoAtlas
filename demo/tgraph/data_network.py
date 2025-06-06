import sys
import os
import argparse
import pandas as pd
import networkx as nx
import numpy as np
import fn # feature names

#ARRUMAR ESSA BAGUNÇA DEPOIS
current_dir = os.path.dirname(os.path.abspath(__file__))  
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) 
sys.path.insert(0, parent_dir)
import config

class DataNetwork():
    
    def __init__(self,
                 df,
                 source=fn.SOURCE,
                 destination=fn.DESTINATION,
                 measure=None,
                 timestamp=None):
        
        self.df = df
        
        # We should have at least SOURCE and DESTINATION columns
        assert len(self.df.columns) >= 2, "wrong # columns"
        
        column_order = [fn.SOURCE, fn.DESTINATION]
        
        self.df.rename(columns={source: fn.SOURCE,
                                destination: fn.DESTINATION},
                       errors="raise",
                       inplace=True)
        
        if measure: # Check if it's not None
            print("Measure found")
            self.df.rename(columns={measure: fn.MEASURE},
                           errors="raise",
                           inplace=True)
            column_order.append(fn.MEASURE)
            
        if timestamp: # Check if it's not None
            print("Timestamp found")
            self.df.rename(columns={timestamp: fn.TIMESTAMP},
                           errors="raise",
                           inplace=True)
            self.df[fn.TIMESTAMP] = self.df[fn.TIMESTAMP].astype('datetime64[s]')
            column_order.append(fn.TIMESTAMP)
        
        # Reorder columns
        self.df = self.df[column_order]
        self.headers = list(self.df.columns.values)
        
        assert self.headers[0] == fn.SOURCE, "wrong header"
        assert self.headers[1] == fn.DESTINATION, "wrong header"
        
        if measure:
            self.df[fn.MEASURE] = pd.to_numeric(self.df[fn.MEASURE], errors='coerce')
            # self.df = self.df[self.df[fn.MEASURE] > 0]        
            self.df.dropna(subset=[fn.MEASURE])
        
        self.df = self.df[self.df[fn.SOURCE] != self.df[fn.DESTINATION]]
        
        # Get the set of all nodes (sources, and/or destinations)
        self.set_of_nodes = self.get_node_set()

        # Start creating the output data frame, with one row per node
        self.df_nodes = pd.DataFrame(self.set_of_nodes)
        self.df_nodes.columns = [fn.NODE_ID]
        
        #Assign node colors
        self.node_colors = self.assign_node_color() 

        if measure:
            self.G = nx.from_pandas_edgelist(self.df,
                                             source=fn.SOURCE,
                                             target=fn.DESTINATION,
                                             create_using=nx.DiGraph(),
                                             edge_attr=fn.MEASURE)
                                             
        else:
            self.G = nx.from_pandas_edgelist(self.df,
                                             source=fn.SOURCE,
                                             target=fn.DESTINATION,
                                             create_using=nx.DiGraph())

        nx.set_node_attributes(self.G, self.node_colors, 'color')
        
    def get_node_set(self):
        set_of_unique_sources = set( self.df[fn.SOURCE].unique())
        set_of_unique_destinations = set(self.df[fn.DESTINATION].unique())
        set_nodes = set( set_of_unique_sources |set_of_unique_destinations)
        return(set_nodes)

    def assign_node_color(self):
        color_map = {}

        for node in self.set_of_nodes:
            #Caso seja vértice de origem
            if node in set(self.df[fn.SOURCE]):
                color_map[node] = config.source_node_color
            #Caso seja vértice de destino
            elif node in set(self.df[fn.DESTINATION]):
                color_map[node] = config.destination_node_color
            
        return color_map

