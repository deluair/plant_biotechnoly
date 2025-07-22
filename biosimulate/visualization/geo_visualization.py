#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Geographic visualization functions for the BIOSIMULATE project.

This module provides functions for creating geographic visualizations of simulation data.
"""

import os
import logging
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Union, Any

from biosimulate.utils.file_utils import ensure_directory_exists

logger = logging.getLogger(__name__)


def load_world_map() -> gpd.GeoDataFrame:
    """Load a world map GeoDataFrame.
    
    Returns:
        GeoDataFrame with world map data
    """
    try:
        # Try to load from GeoPandas datasets
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        logger.info("Loaded world map from GeoPandas datasets")
        return world
    except Exception as e:
        logger.warning(f"Could not load world map from GeoPandas datasets: {e}")
        logger.info("Attempting to download world map from Natural Earth")
        
        # Try to download from Natural Earth
        try:
            url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
            world = gpd.read_file(url)
            logger.info("Downloaded world map from Natural Earth")
            return world
        except Exception as e:
            logger.error(f"Could not download world map: {e}")
            raise ValueError("Could not load world map. Please check your internet connection or install the required data files.")


def plot_choropleth_map(data: pd.DataFrame, region_col: str, value_col: str,
                       title: str, output_path: Optional[str] = None,
                       cmap: str = "viridis", figsize: Tuple[int, int] = (12, 8),
                       region_map: Optional[Dict[str, str]] = None) -> plt.Figure:
    """Create a choropleth map using Matplotlib and GeoPandas.
    
    Args:
        data: DataFrame containing the data
        region_col: Column name for region identifiers
        value_col: Column name for values to plot
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        cmap: Colormap to use
        figsize: Figure size as (width, height) in inches
        region_map: Dictionary mapping data region identifiers to map region identifiers
        
    Returns:
        Matplotlib Figure object
    """
    # Load world map
    world = load_world_map()
    
    # Create a copy of the data for merging
    plot_data = data.copy()
    
    # Apply region mapping if provided
    if region_map is not None:
        plot_data[region_col] = plot_data[region_col].map(region_map).fillna(plot_data[region_col])
    
    # Merge data with world map
    # Assuming region_col in data matches 'name' in world map
    merged = world.merge(plot_data, left_on='name', right_on=region_col, how='left')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the choropleth map
    merged.plot(column=value_col, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
               legend=True, missing_kwds={'color': 'lightgray'})
    
    # Set title
    ax.set_title(title, fontsize=16)
    
    # Remove axis ticks and labels
    ax.set_axis_off()
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved choropleth map to {output_path}")
    
    return fig


def create_interactive_choropleth(data: pd.DataFrame, region_col: str, value_col: str,
                                title: str, output_path: Optional[str] = None,
                                color_scale: str = "Viridis",
                                hover_data: Optional[List[str]] = None,
                                region_map: Optional[Dict[str, str]] = None,
                                height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive choropleth map using Plotly.
    
    Args:
        data: DataFrame containing the data
        region_col: Column name for region identifiers (ISO-3 country codes)
        value_col: Column name for values to plot
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        color_scale: Colorscale to use
        hover_data: List of column names to show in hover tooltip
        region_map: Dictionary mapping data region identifiers to ISO-3 country codes
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create a copy of the data for mapping
    plot_data = data.copy()
    
    # Apply region mapping if provided
    if region_map is not None:
        plot_data['iso_alpha'] = plot_data[region_col].map(region_map).fillna(plot_data[region_col])
    else:
        plot_data['iso_alpha'] = plot_data[region_col]
    
    # Create the plot
    fig = px.choropleth(
        plot_data,
        locations='iso_alpha',
        color=value_col,
        hover_name=region_col,
        hover_data=hover_data,
        color_continuous_scale=color_scale,
        title=title,
        height=height,
        width=width
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive choropleth map to {output_path}")
    
    return fig


def create_bubble_map(data: pd.DataFrame, lat_col: str, lon_col: str, 
                     size_col: str, title: str, 
                     output_path: Optional[str] = None,
                     color_col: Optional[str] = None,
                     hover_name: Optional[str] = None,
                     hover_data: Optional[List[str]] = None,
                     color_scale: str = "Viridis",
                     size_max: int = 40,
                     height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive bubble map using Plotly.
    
    Args:
        data: DataFrame containing the data
        lat_col: Column name for latitude values
        lon_col: Column name for longitude values
        size_col: Column name for bubble sizes
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        color_col: Column name for bubble colors (default: None)
        hover_name: Column name for hover labels
        hover_data: List of column names to show in hover tooltip
        color_scale: Colorscale to use
        size_max: Maximum bubble size
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.scatter_geo(
        data,
        lat=lat_col,
        lon=lon_col,
        size=size_col,
        color=color_col,
        hover_name=hover_name,
        hover_data=hover_data,
        color_continuous_scale=color_scale,
        size_max=size_max,
        title=title,
        height=height,
        width=width
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive bubble map to {output_path}")
    
    return fig


def create_flow_map(data: pd.DataFrame, origin_lat_col: str, origin_lon_col: str,
                   dest_lat_col: str, dest_lon_col: str, flow_col: str,
                   title: str, output_path: Optional[str] = None,
                   color_col: Optional[str] = None,
                   hover_name: Optional[str] = None,
                   hover_data: Optional[List[str]] = None,
                   color_scale: str = "Viridis",
                   height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive flow map using Plotly.
    
    Args:
        data: DataFrame containing the data
        origin_lat_col: Column name for origin latitude values
        origin_lon_col: Column name for origin longitude values
        dest_lat_col: Column name for destination latitude values
        dest_lon_col: Column name for destination longitude values
        flow_col: Column name for flow values (determines line width)
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        color_col: Column name for line colors (default: None)
        hover_name: Column name for hover labels
        hover_data: List of column names to show in hover tooltip
        color_scale: Colorscale to use
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create figure
    fig = go.Figure()
    
    # Normalize flow values for line width
    max_flow = data[flow_col].max()
    min_flow = data[flow_col].min()
    norm_flow = (data[flow_col] - min_flow) / (max_flow - min_flow) * 10 + 1
    
    # Determine color values if color_col is provided
    if color_col is not None:
        color_vals = data[color_col]
        color_min = color_vals.min()
        color_max = color_vals.max()
        colorscale = px.colors.sequential.get_scale(color_scale)
    else:
        color_vals = None
    
    # Add flow lines
    for i, row in data.iterrows():
        # Get coordinates
        origin_lat = row[origin_lat_col]
        origin_lon = row[origin_lon_col]
        dest_lat = row[dest_lat_col]
        dest_lon = row[dest_lon_col]
        
        # Get flow value for line width
        flow = norm_flow.iloc[i]
        
        # Get color if color_col is provided
        if color_vals is not None:
            color_val = color_vals.iloc[i]
            # Normalize color value
            norm_color = (color_val - color_min) / (color_max - color_min)
            # Get color from colorscale
            color_idx = min(int(norm_color * (len(colorscale) - 1)), len(colorscale) - 1)
            color = colorscale[color_idx][1]
        else:
            color = 'rgba(0, 0, 255, 0.6)'  # Default blue with transparency
        
        # Create hover text
        hover_text = f"{row.get(hover_name, '')}"  # Start with hover_name if provided
        if hover_data is not None:
            for col in hover_data:
                if col in row:
                    hover_text += f"<br>{col}: {row[col]}"
        
        # Add line
        fig.add_trace(go.Scattergeo(
            lon=[origin_lon, dest_lon],
            lat=[origin_lat, dest_lat],
            mode='lines',
            line=dict(
                width=flow,
                color=color
            ),
            opacity=0.7,
            hoverinfo='text',
            text=hover_text
        ))
        
        # Add origin point
        fig.add_trace(go.Scattergeo(
            lon=[origin_lon],
            lat=[origin_lat],
            mode='markers',
            marker=dict(
                size=5,
                color='red',
                opacity=0.7
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add destination point
        fig.add_trace(go.Scattergeo(
            lon=[dest_lon],
            lat=[dest_lat],
            mode='markers',
            marker=dict(
                size=5,
                color='blue',
                opacity=0.7
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=height,
        width=width
    )
    
    # Add colorbar if color_col is provided
    if color_col is not None:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=color_col,
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
        logger.info(f"Saved interactive flow map to {output_path}")
    
    return fig


def create_region_comparison_map(data_dict: Dict[str, pd.DataFrame], 
                               region_col: str, value_col: str,
                               title: str, output_path: Optional[str] = None,
                               color_scale: str = "Viridis",
                               region_map: Optional[Dict[str, str]] = None,
                               height: int = 800, width: int = 1200) -> go.Figure:
    """Create an interactive map comparing the same metric across different scenarios.
    
    Args:
        data_dict: Dictionary mapping scenario names to DataFrames
        region_col: Column name for region identifiers (ISO-3 country codes)
        value_col: Column name for values to plot
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        color_scale: Colorscale to use
        region_map: Dictionary mapping data region identifiers to ISO-3 country codes
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create figure with subplots
    n_scenarios = len(data_dict)
    n_cols = min(3, n_scenarios)  # Maximum 3 maps per row
    n_rows = (n_scenarios + n_cols - 1) // n_cols  # Ceiling division
    
    # Create subplot titles
    subplot_titles = list(data_dict.keys())
    
    # Create figure
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=subplot_titles,
        specs=[[{'type': 'choropleth'} for _ in range(n_cols)] for _ in range(n_rows)],
        horizontal_spacing=0.05,
        vertical_spacing=0.1
    )
    
    # Find global min and max for consistent color scale
    all_values = []
    for df in data_dict.values():
        all_values.extend(df[value_col].dropna().tolist())
    
    global_min = min(all_values)
    global_max = max(all_values)
    
    # Add each scenario as a choropleth map
    for i, (scenario, df) in enumerate(data_dict.items()):
        row = i // n_cols + 1
        col = i % n_cols + 1
        
        # Create a copy of the data for mapping
        plot_data = df.copy()
        
        # Apply region mapping if provided
        if region_map is not None:
            plot_data['iso_alpha'] = plot_data[region_col].map(region_map).fillna(plot_data[region_col])
        else:
            plot_data['iso_alpha'] = plot_data[region_col]
        
        # Add choropleth trace
        fig.add_trace(
            go.Choropleth(
                locations=plot_data['iso_alpha'],
                z=plot_data[value_col],
                colorscale=color_scale,
                zmin=global_min,
                zmax=global_max,
                marker_line_color='white',
                marker_line_width=0.5,
                colorbar=dict(
                    title=value_col,
                    thickness=15,
                    len=0.5,
                    y=0.5,
                    yanchor='middle',
                    x=1.05,
                    xanchor='right'
                ) if i == 0 else None,  # Only show colorbar for first map
                showscale=i == 0  # Only show scale for first map
            ),
            row=row, col=col
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        height=height,
        width=width,
        margin={"r":100, "t":100, "l":20, "b":20}
    )
    
    # Update geo layout for each subplot
    for i in range(1, n_scenarios + 1):
        row = (i - 1) // n_cols + 1
        col = (i - 1) % n_cols + 1
        fig.update_geos(
            projection_type="natural earth",
            showcoastlines=True, coastlinecolor="Black",
            showland=True, landcolor="white",
            showocean=True, oceancolor="lightblue",
            showlakes=True, lakecolor="lightblue",
            fitbounds="locations",
            row=row, col=col
        )
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive region comparison map to {output_path}")
    
    return fig