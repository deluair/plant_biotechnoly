#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Network visualization functions for the BIOSIMULATE project.

This module provides functions for creating network visualizations of simulation data.
"""

import os
import logging
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Union, Any, Callable

from biosimulate.utils.file_utils import ensure_directory_exists

logger = logging.getLogger(__name__)


def create_network_graph(nodes: pd.DataFrame, edges: pd.DataFrame,
                        title: str, output_path: Optional[str] = None,
                        node_size_col: Optional[str] = None,
                        node_color_col: Optional[str] = None,
                        edge_weight_col: Optional[str] = None,
                        node_label_col: Optional[str] = None,
                        layout: str = 'spring',
                        figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
    """Create a network graph visualization using NetworkX and Matplotlib.
    
    Args:
        nodes: DataFrame containing node data with at least an 'id' column
        edges: DataFrame containing edge data with 'source' and 'target' columns
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        node_size_col: Column name for node sizes (default: None, uniform size)
        node_color_col: Column name for node colors (default: None, uniform color)
        edge_weight_col: Column name for edge weights (default: None, uniform weight)
        node_label_col: Column name for node labels (default: None, no labels)
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 'spectral', 'random')
        figsize: Figure size as (width, height) in inches
        
    Returns:
        Matplotlib Figure object
    """
    # Create a graph
    G = nx.Graph()
    
    # Add nodes
    for _, node in nodes.iterrows():
        node_id = node['id']
        node_attrs = {col: node[col] for col in nodes.columns if col != 'id'}
        G.add_node(node_id, **node_attrs)
    
    # Add edges
    for _, edge in edges.iterrows():
        source = edge['source']
        target = edge['target']
        edge_attrs = {col: edge[col] for col in edges.columns if col not in ['source', 'target']}
        G.add_edge(source, target, **edge_attrs)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Determine layout positions
    if layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.spring_layout(G)  # Default to spring layout
    
    # Determine node sizes
    if node_size_col is not None and node_size_col in nodes.columns:
        # Normalize sizes for better visualization
        sizes = nodes[node_size_col].values
        node_sizes = 100 + 1000 * (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-10)
    else:
        node_sizes = 300  # Default size
    
    # Determine node colors
    if node_color_col is not None and node_color_col in nodes.columns:
        node_colors = nodes[node_color_col].values
    else:
        node_colors = 'skyblue'  # Default color
    
    # Determine edge weights
    if edge_weight_col is not None and edge_weight_col in edges.columns:
        # Normalize weights for better visualization
        weights = edges[edge_weight_col].values
        edge_widths = 1 + 5 * (weights - weights.min()) / (weights.max() - weights.min() + 1e-10)
    else:
        edge_widths = 1.0  # Default width
    
    # Draw the network
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7, edge_color='gray')
    nodes_drawn = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    
    # Add node labels if specified
    if node_label_col is not None and node_label_col in nodes.columns:
        labels = {node['id']: str(node[node_label_col]) for _, node in nodes.iterrows()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')
    
    # Add colorbar if node colors are from a numeric column
    if node_color_col is not None and node_color_col in nodes.columns and nodes[node_color_col].dtype in [np.float64, np.int64]:
        plt.colorbar(nodes_drawn, ax=ax, label=node_color_col)
    
    # Set title and remove axis
    ax.set_title(title, fontsize=16)
    ax.axis('off')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved network graph to {output_path}")
    
    return fig


def create_interactive_network(nodes: pd.DataFrame, edges: pd.DataFrame,
                             title: str, output_path: Optional[str] = None,
                             node_size_col: Optional[str] = None,
                             node_color_col: Optional[str] = None,
                             edge_weight_col: Optional[str] = None,
                             node_hover_cols: Optional[List[str]] = None,
                             edge_hover_cols: Optional[List[str]] = None,
                             layout: str = 'spring',
                             height: int = 800, width: int = 1000) -> go.Figure:
    """Create an interactive network graph visualization using Plotly.
    
    Args:
        nodes: DataFrame containing node data with at least an 'id' column
        edges: DataFrame containing edge data with 'source' and 'target' columns
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        node_size_col: Column name for node sizes (default: None, uniform size)
        node_color_col: Column name for node colors (default: None, uniform color)
        edge_weight_col: Column name for edge weights (default: None, uniform weight)
        node_hover_cols: List of column names to show in node hover tooltip
        edge_hover_cols: List of column names to show in edge hover tooltip
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 'spectral', 'random')
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create a graph
    G = nx.Graph()
    
    # Add nodes
    for _, node in nodes.iterrows():
        node_id = node['id']
        node_attrs = {col: node[col] for col in nodes.columns if col != 'id'}
        G.add_node(node_id, **node_attrs)
    
    # Add edges
    for _, edge in edges.iterrows():
        source = edge['source']
        target = edge['target']
        edge_attrs = {col: edge[col] for col in edges.columns if col not in ['source', 'target']}
        G.add_edge(source, target, **edge_attrs)
    
    # Determine layout positions
    if layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.spring_layout(G)  # Default to spring layout
    
    # Extract node positions
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    # Determine node sizes
    if node_size_col is not None and node_size_col in nodes.columns:
        # Normalize sizes for better visualization
        sizes = nodes[node_size_col].values
        node_sizes = 10 + 50 * (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-10)
    else:
        node_sizes = 15  # Default size
    
    # Determine node colors
    if node_color_col is not None and node_color_col in nodes.columns:
        node_colors = nodes[node_color_col].values
        colorscale = 'Viridis'
    else:
        node_colors = 'rgba(31, 119, 180, 0.8)'  # Default color
        colorscale = None
    
    # Create node hover text
    node_hover_text = []
    for _, node in nodes.iterrows():
        hover_text = f"ID: {node['id']}"
        if node_hover_cols is not None:
            for col in node_hover_cols:
                if col in node and col != 'id':
                    hover_text += f"<br>{col}: {node[col]}"
        node_hover_text.append(hover_text)
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_hover_text,
        marker=dict(
            size=node_sizes,
            color=node_colors,
            colorscale=colorscale,
            line=dict(width=1, color='rgba(50, 50, 50, 0.8)')
        )
    )
    
    # Create edge traces
    edge_traces = []
    
    # Determine edge weights
    if edge_weight_col is not None and edge_weight_col in edges.columns:
        # Normalize weights for better visualization
        weights = edges[edge_weight_col].values
        edge_widths = 1 + 5 * (weights - weights.min()) / (weights.max() - weights.min() + 1e-10)
    else:
        edge_widths = [1.0] * len(edges)  # Default width
    
    # Create edge hover text
    edge_hover_text = []
    for _, edge in edges.iterrows():
        hover_text = f"Source: {edge['source']}<br>Target: {edge['target']}"
        if edge_hover_cols is not None:
            for col in edge_hover_cols:
                if col in edge and col not in ['source', 'target']:
                    hover_text += f"<br>{col}: {edge[col]}"
        edge_hover_text.append(hover_text)
    
    # Create edge traces
    for i, (_, edge) in enumerate(edges.iterrows()):
        source = edge['source']
        target = edge['target']
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        
        edge_trace = go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(width=edge_widths[i], color='rgba(150, 150, 150, 0.6)'),
            hoverinfo='text',
            text=edge_hover_text[i]
        )
        
        edge_traces.append(edge_trace)
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace],
                   layout=go.Layout(
                       title=dict(
                           text=title,
                           y=0.95,
                           x=0.5,
                           xanchor='center',
                           yanchor='top',
                           font=dict(size=16)
                       ),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       height=height,
                       width=width
                   ))
    
    # Add colorbar if node colors are from a numeric column
    if node_color_col is not None and node_color_col in nodes.columns and nodes[node_color_col].dtype in [np.float64, np.int64]:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=node_color_col,
                thickness=15,
                len=0.5,
                xanchor="left",
                x=0.05
            )
        )
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive network graph to {output_path}")
    
    return fig


def create_community_network(nodes: pd.DataFrame, edges: pd.DataFrame,
                           community_col: str, title: str, 
                           output_path: Optional[str] = None,
                           node_size_col: Optional[str] = None,
                           edge_weight_col: Optional[str] = None,
                           node_label_col: Optional[str] = None,
                           layout: str = 'spring',
                           figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
    """Create a network graph visualization with community detection using NetworkX and Matplotlib.
    
    Args:
        nodes: DataFrame containing node data with at least 'id' and community_col columns
        edges: DataFrame containing edge data with 'source' and 'target' columns
        community_col: Column name for community assignments
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        node_size_col: Column name for node sizes (default: None, uniform size)
        edge_weight_col: Column name for edge weights (default: None, uniform weight)
        node_label_col: Column name for node labels (default: None, no labels)
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 'spectral', 'random')
        figsize: Figure size as (width, height) in inches
        
    Returns:
        Matplotlib Figure object
    """
    # Create a graph
    G = nx.Graph()
    
    # Add nodes with community information
    for _, node in nodes.iterrows():
        node_id = node['id']
        community = node[community_col]
        node_attrs = {col: node[col] for col in nodes.columns if col not in ['id']}
        G.add_node(node_id, community=community, **node_attrs)
    
    # Add edges
    for _, edge in edges.iterrows():
        source = edge['source']
        target = edge['target']
        weight = edge[edge_weight_col] if edge_weight_col and edge_weight_col in edge else 1.0
        G.add_edge(source, target, weight=weight)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Determine layout positions
    if layout == 'spring':
        pos = nx.spring_layout(G, weight='weight' if edge_weight_col else None)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G, weight='weight' if edge_weight_col else None)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.spring_layout(G, weight='weight' if edge_weight_col else None)  # Default to spring layout
    
    # Get communities
    communities = nx.get_node_attributes(G, 'community')
    unique_communities = set(communities.values())
    
    # Create a color map for communities
    cmap = plt.cm.get_cmap('tab20', len(unique_communities))
    community_colors = {comm: cmap(i) for i, comm in enumerate(unique_communities)}
    
    # Determine node sizes
    if node_size_col is not None and node_size_col in nodes.columns:
        # Normalize sizes for better visualization
        sizes = nodes[node_size_col].values
        node_sizes = 100 + 1000 * (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-10)
        node_size_dict = {node['id']: size for _, node, size in zip(nodes.index, nodes.itertuples(), node_sizes)}
    else:
        node_size_dict = {node: 300 for node in G.nodes()}  # Default size
    
    # Determine edge weights
    if edge_weight_col is not None and edge_weight_col in edges.columns:
        # Normalize weights for better visualization
        weights = edges[edge_weight_col].values
        edge_widths = 1 + 5 * (weights - weights.min()) / (weights.max() - weights.min() + 1e-10)
    else:
        edge_widths = 1.0  # Default width
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='gray')
    
    # Draw nodes for each community
    for comm in unique_communities:
        # Get nodes in this community
        comm_nodes = [node for node, node_comm in communities.items() if node_comm == comm]
        
        # Get sizes for these nodes
        comm_node_sizes = [node_size_dict[node] for node in comm_nodes]
        
        # Draw nodes for this community
        nx.draw_networkx_nodes(G, pos, nodelist=comm_nodes, node_size=comm_node_sizes,
                              node_color=[community_colors[comm]] * len(comm_nodes),
                              label=f"Community {comm}", alpha=0.8)
    
    # Add node labels if specified
    if node_label_col is not None and node_label_col in nodes.columns:
        labels = {node['id']: str(node[node_label_col]) for _, node in nodes.iterrows()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')
    
    # Add legend
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1)
    
    # Set title and remove axis
    ax.set_title(title, fontsize=16)
    ax.axis('off')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved community network graph to {output_path}")
    
    return fig


def create_bipartite_network(nodes1: pd.DataFrame, nodes2: pd.DataFrame, edges: pd.DataFrame,
                           title: str, output_path: Optional[str] = None,
                           node_size_col: Optional[str] = None,
                           edge_weight_col: Optional[str] = None,
                           node_label_col: Optional[str] = None,
                           figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
    """Create a bipartite network graph visualization using NetworkX and Matplotlib.
    
    Args:
        nodes1: DataFrame containing first set of node data with at least an 'id' column
        nodes2: DataFrame containing second set of node data with at least an 'id' column
        edges: DataFrame containing edge data with 'source' and 'target' columns
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        node_size_col: Column name for node sizes (default: None, uniform size)
        edge_weight_col: Column name for edge weights (default: None, uniform weight)
        node_label_col: Column name for node labels (default: None, no labels)
        figsize: Figure size as (width, height) in inches
        
    Returns:
        Matplotlib Figure object
    """
    # Create a bipartite graph
    B = nx.Graph()
    
    # Add nodes with bipartite attribute
    for _, node in nodes1.iterrows():
        node_id = node['id']
        node_attrs = {col: node[col] for col in nodes1.columns if col != 'id'}
        B.add_node(node_id, bipartite=0, **node_attrs)  # bipartite=0 for first set
    
    for _, node in nodes2.iterrows():
        node_id = node['id']
        node_attrs = {col: node[col] for col in nodes2.columns if col != 'id'}
        B.add_node(node_id, bipartite=1, **node_attrs)  # bipartite=1 for second set
    
    # Add edges
    for _, edge in edges.iterrows():
        source = edge['source']
        target = edge['target']
        weight = edge[edge_weight_col] if edge_weight_col and edge_weight_col in edge else 1.0
        B.add_edge(source, target, weight=weight)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get node sets
    nodes_set1 = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
    nodes_set2 = set(B) - nodes_set1
    
    # Create bipartite layout
    pos = nx.bipartite_layout(B, nodes_set1)
    
    # Determine node sizes
    if node_size_col is not None:
        # Create a mapping of node id to size
        size_map = {}
        
        # Add sizes for first set of nodes
        if node_size_col in nodes1.columns:
            sizes1 = nodes1[node_size_col].values
            norm_sizes1 = 100 + 1000 * (sizes1 - sizes1.min()) / (sizes1.max() - sizes1.min() + 1e-10)
            for node_id, size in zip(nodes1['id'], norm_sizes1):
                size_map[node_id] = size
        else:
            for node_id in nodes1['id']:
                size_map[node_id] = 300  # Default size
        
        # Add sizes for second set of nodes
        if node_size_col in nodes2.columns:
            sizes2 = nodes2[node_size_col].values
            norm_sizes2 = 100 + 1000 * (sizes2 - sizes2.min()) / (sizes2.max() - sizes2.min() + 1e-10)
            for node_id, size in zip(nodes2['id'], norm_sizes2):
                size_map[node_id] = size
        else:
            for node_id in nodes2['id']:
                size_map[node_id] = 300  # Default size
        
        # Get sizes for each set
        node_sizes1 = [size_map.get(node, 300) for node in nodes_set1]
        node_sizes2 = [size_map.get(node, 300) for node in nodes_set2]
    else:
        node_sizes1 = 300  # Default size
        node_sizes2 = 300  # Default size
    
    # Determine edge weights
    if edge_weight_col is not None and edge_weight_col in edges.columns:
        # Normalize weights for better visualization
        weights = edges[edge_weight_col].values
        edge_widths = 1 + 5 * (weights - weights.min()) / (weights.max() - weights.min() + 1e-10)
    else:
        edge_widths = 1.0  # Default width
    
    # Draw edges
    nx.draw_networkx_edges(B, pos, width=edge_widths, alpha=0.5, edge_color='gray')
    
    # Draw nodes
    nx.draw_networkx_nodes(B, pos, nodelist=list(nodes_set1), node_size=node_sizes1,
                          node_color='skyblue', label='Set 1', alpha=0.8)
    nx.draw_networkx_nodes(B, pos, nodelist=list(nodes_set2), node_size=node_sizes2,
                          node_color='lightgreen', label='Set 2', alpha=0.8)
    
    # Add node labels if specified
    if node_label_col is not None:
        # Create a mapping of node id to label
        label_map = {}
        
        # Add labels for first set of nodes
        if node_label_col in nodes1.columns:
            for _, node in nodes1.iterrows():
                label_map[node['id']] = str(node[node_label_col])
        
        # Add labels for second set of nodes
        if node_label_col in nodes2.columns:
            for _, node in nodes2.iterrows():
                label_map[node['id']] = str(node[node_label_col])
        
        # Draw labels
        nx.draw_networkx_labels(B, pos, labels=label_map, font_size=10, font_color='black')
    
    # Add legend
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1)
    
    # Set title and remove axis
    ax.set_title(title, fontsize=16)
    ax.axis('off')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved bipartite network graph to {output_path}")
    
    return fig


def create_network_metrics_visualization(G: nx.Graph, title: str, 
                                        output_path: Optional[str] = None,
                                        figsize: Tuple[int, int] = (15, 10)) -> plt.Figure:
    """Create a visualization of network metrics using NetworkX and Matplotlib.
    
    Args:
        G: NetworkX Graph object
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        
    Returns:
        Matplotlib Figure object
    """
    # Create figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle(title, fontsize=16)
    
    # 1. Degree distribution
    degrees = [d for n, d in G.degree()]
    axs[0, 0].hist(degrees, bins=20, alpha=0.7, color='skyblue')
    axs[0, 0].set_title('Degree Distribution')
    axs[0, 0].set_xlabel('Degree')
    axs[0, 0].set_ylabel('Count')
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)
    
    # 2. Centrality measures
    # Calculate centrality measures
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    eigenvector = nx.eigenvector_centrality_numpy(G)
    
    # Create a DataFrame for centrality measures
    centrality_df = pd.DataFrame({
        'Node': list(G.nodes()),
        'Betweenness': list(betweenness.values()),
        'Closeness': list(closeness.values()),
        'Eigenvector': list(eigenvector.values())
    })
    
    # Sort by betweenness centrality
    centrality_df = centrality_df.sort_values('Betweenness', ascending=False).head(20)
    
    # Plot centrality measures
    centrality_df.plot(x='Node', y=['Betweenness', 'Closeness', 'Eigenvector'], 
                      kind='bar', ax=axs[0, 1], alpha=0.7)
    axs[0, 1].set_title('Centrality Measures (Top 20 Nodes)')
    axs[0, 1].set_xlabel('Node')
    axs[0, 1].set_ylabel('Centrality Value')
    axs[0, 1].tick_params(axis='x', rotation=90)
    axs[0, 1].grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # 3. Clustering coefficient distribution
    clustering = nx.clustering(G)
    axs[1, 0].hist(list(clustering.values()), bins=20, alpha=0.7, color='lightgreen')
    axs[1, 0].set_title('Clustering Coefficient Distribution')
    axs[1, 0].set_xlabel('Clustering Coefficient')
    axs[1, 0].set_ylabel('Count')
    axs[1, 0].grid(True, linestyle='--', alpha=0.7)
    
    # 4. Network statistics
    stats = [
        f"Nodes: {G.number_of_nodes()}",
        f"Edges: {G.number_of_edges()}",
        f"Density: {nx.density(G):.4f}",
        f"Average Clustering: {nx.average_clustering(G):.4f}",
        f"Average Shortest Path: {nx.average_shortest_path_length(G) if nx.is_connected(G) else 'N/A (Disconnected)'}",
        f"Diameter: {nx.diameter(G) if nx.is_connected(G) else 'N/A (Disconnected)'}",
        f"Average Degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}",
        f"Number of Connected Components: {nx.number_connected_components(G)}"
    ]
    
    # Turn off axis for the statistics subplot
    axs[1, 1].axis('off')
    axs[1, 1].set_title('Network Statistics')
    
    # Add statistics as text
    y_pos = 0.9
    for stat in stats:
        axs[1, 1].text(0.1, y_pos, stat, fontsize=12)
        y_pos -= 0.1
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for suptitle
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved network metrics visualization to {output_path}")
    
    return fig