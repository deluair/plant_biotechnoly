#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Interactive visualization functions for the BIOSIMULATE project.

This module provides functions for creating interactive visualizations of simulation data.
"""

import os
import logging
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional, Union, Any, Callable

from biosimulate.utils.file_utils import ensure_directory_exists

logger = logging.getLogger(__name__)


def create_line_plot(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                    title: str, output_path: Optional[str] = None,
                    y_label: str = "", x_label: str = "Year",
                    color_discrete_map: Optional[Dict[str, str]] = None,
                    height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive line plot with multiple lines.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_cols: List of column names for y-axis values
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_discrete_map: Dictionary mapping series names to colors
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Melt the DataFrame to long format for Plotly Express
    df_melted = data.melt(id_vars=[x_col], value_vars=y_cols, 
                         var_name='Series', value_name='Value')
    
    # Create the plot
    fig = px.line(df_melted, x=x_col, y='Value', color='Series',
                 title=title, labels={'Value': y_label, x_col: x_label},
                 color_discrete_map=color_discrete_map,
                 height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        yaxis_title=y_label if y_label else 'Value',
        legend_title_text='Series',
        hovermode='x unified'
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_area_plot(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                    title: str, output_path: Optional[str] = None,
                    y_label: str = "", x_label: str = "Year",
                    color_discrete_map: Optional[Dict[str, str]] = None,
                    stacked: bool = True,
                    height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive area plot.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_cols: List of column names for y-axis values
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_discrete_map: Dictionary mapping series names to colors
        stacked: Whether to create a stacked area plot (default: True)
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Melt the DataFrame to long format for Plotly Express
    df_melted = data.melt(id_vars=[x_col], value_vars=y_cols, 
                         var_name='Series', value_name='Value')
    
    # Create the plot
    fig = px.area(df_melted, x=x_col, y='Value', color='Series',
                 title=title, labels={'Value': y_label, x_col: x_label},
                 color_discrete_map=color_discrete_map,
                 groupnorm='fraction' if stacked else None,
                 height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        yaxis_title=y_label if y_label else 'Value',
        legend_title_text='Series',
        hovermode='x unified'
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                    title: str, output_path: Optional[str] = None,
                    y_label: str = "", x_label: str = "",
                    color_col: Optional[str] = None,
                    color_discrete_map: Optional[Dict[str, str]] = None,
                    height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive bar chart.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for categories
        y_col: Column name for values
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_col: Column name for bar colors (default: None)
        color_discrete_map: Dictionary mapping color values to colors
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.bar(data, x=x_col, y=y_col, color=color_col,
                title=title, 
                labels={y_col: y_label if y_label else y_col, 
                        x_col: x_label if x_label else x_col},
                color_discrete_map=color_discrete_map,
                height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label if x_label else x_col,
        yaxis_title=y_label if y_label else y_col,
        hovermode='closest'
    )
    
    # Add grid for y-axis only
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_grouped_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                           color_col: str, title: str, 
                           output_path: Optional[str] = None,
                           y_label: str = "", x_label: str = "",
                           color_discrete_map: Optional[Dict[str, str]] = None,
                           barmode: str = 'group',
                           height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive grouped bar chart.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for categories
        y_col: Column name for values
        color_col: Column name for grouping
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_discrete_map: Dictionary mapping group names to colors
        barmode: Bar mode ('group' or 'stack')
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.bar(data, x=x_col, y=y_col, color=color_col,
                title=title, barmode=barmode,
                labels={y_col: y_label if y_label else y_col, 
                        x_col: x_label if x_label else x_col},
                color_discrete_map=color_discrete_map,
                height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label if x_label else x_col,
        yaxis_title=y_label if y_label else y_col,
        legend_title_text=color_col,
        hovermode='closest'
    )
    
    # Add grid for y-axis only
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_heatmap(data: pd.DataFrame, title: str, 
                  output_path: Optional[str] = None,
                  x_label: str = "", y_label: str = "",
                  colorscale: str = "Viridis",
                  height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive heatmap.
    
    Args:
        data: DataFrame containing the data (should be a matrix)
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        x_label: Label for x-axis
        y_label: Label for y-axis
        colorscale: Colorscale for the heatmap
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.imshow(data, 
                   labels=dict(x=x_label, y=y_label, color="Value"),
                   x=data.columns if x_label else None,
                   y=data.index if y_label else None,
                   color_continuous_scale=colorscale,
                   height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_scatter_plot(data: pd.DataFrame, x_col: str, y_col: str, 
                       title: str, output_path: Optional[str] = None,
                       y_label: str = "", x_label: str = "",
                       color_col: Optional[str] = None,
                       size_col: Optional[str] = None,
                       hover_data: Optional[List[str]] = None,
                       add_trendline: bool = False,
                       height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive scatter plot.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_col: Column name for y-axis values
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_col: Column name for point colors (default: None)
        size_col: Column name for point sizes (default: None)
        hover_data: List of column names to show in hover tooltip
        add_trendline: Whether to add a linear trendline
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.scatter(data, x=x_col, y=y_col, 
                    color=color_col, size=size_col,
                    hover_data=hover_data,
                    trendline='ols' if add_trendline else None,
                    title=title,
                    labels={y_col: y_label if y_label else y_col, 
                            x_col: x_label if x_label else x_col},
                    height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label if x_label else x_col,
        yaxis_title=y_label if y_label else y_col,
        hovermode='closest'
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_pie_chart(data: pd.DataFrame, value_col: str, name_col: str, 
                    title: str, output_path: Optional[str] = None,
                    color_discrete_map: Optional[Dict[str, str]] = None,
                    height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive pie chart.
    
    Args:
        data: DataFrame containing the data
        value_col: Column name for values
        name_col: Column name for labels
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        color_discrete_map: Dictionary mapping names to colors
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create the plot
    fig = px.pie(data, values=value_col, names=name_col,
                title=title,
                color_discrete_map=color_discrete_map,
                height=height, width=width)
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        hovermode='closest'
    )
    
    # Update traces
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_scenario_comparison(data_dict: Dict[str, pd.DataFrame], x_col: str, y_col: str, 
                             title: str, output_path: Optional[str] = None,
                             y_label: str = "", x_label: str = "Year",
                             color_discrete_map: Optional[Dict[str, str]] = None,
                             height: int = 600, width: int = 900) -> go.Figure:
    """Create an interactive line plot comparing the same metric across different scenarios.
    
    Args:
        data_dict: Dictionary mapping scenario names to DataFrames
        x_col: Column name for x-axis values
        y_col: Column name for y-axis values
        title: Plot title
        output_path: Path to save the plot as HTML (default: None, don't save)
        y_label: Label for y-axis
        x_label: Label for x-axis
        color_discrete_map: Dictionary mapping scenario names to colors
        height: Plot height in pixels
        width: Plot width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Create figure
    fig = go.Figure()
    
    # Add each scenario as a line
    for scenario, df in data_dict.items():
        color = color_discrete_map.get(scenario) if color_discrete_map else None
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=scenario,
            line=dict(color=color) if color else None
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
        xaxis_title=x_label,
        yaxis_title=y_label if y_label else y_col,
        hovermode='x unified',
        height=height,
        width=width
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        fig.write_html(output_path)
        logger.info(f"Saved interactive plot to {output_path}")
    
    return fig


def create_interactive_dashboard(plots: List[Dict[str, Any]], 
                               title: str, 
                               output_path: str,
                               rows: int = None, cols: int = 2,
                               height: int = 1200, width: int = 1200) -> go.Figure:
    """Create an interactive dashboard with multiple plots.
    
    Args:
        plots: List of dictionaries with plot specifications
            Each dictionary should have:
            - 'title': Plot title
            - 'type': Plot type ('line', 'bar', 'scatter', 'pie', 'heatmap')
            - 'data': DataFrame or dictionary with plot data
            - Other plot-specific parameters
        title: Dashboard title
        output_path: Path to save the dashboard as HTML
        rows: Number of rows (default: None, calculated based on number of plots)
        cols: Number of columns (default: 2)
        height: Dashboard height in pixels
        width: Dashboard width in pixels
        
    Returns:
        Plotly Figure object
    """
    # Calculate number of rows if not provided
    if rows is None:
        rows = (len(plots) + cols - 1) // cols  # Ceiling division
    
    # Create subplot grid
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[plot['title'] for plot in plots],
        vertical_spacing=0.1,
        horizontal_spacing=0.05
    )
    
    # Add each plot to the dashboard
    for i, plot_spec in enumerate(plots):
        row = i // cols + 1
        col = i % cols + 1
        
        plot_type = plot_spec['type']
        data = plot_spec['data']
        
        if plot_type == 'line':
            # For line plots
            x_col = plot_spec.get('x_col', 'year')
            y_cols = plot_spec.get('y_cols', [])
            
            if isinstance(data, pd.DataFrame):
                for y_col in y_cols:
                    fig.add_trace(
                        go.Scatter(x=data[x_col], y=data[y_col], name=y_col, mode='lines'),
                        row=row, col=col
                    )
            elif isinstance(data, dict):
                # Assume it's a scenario comparison
                for scenario, df in data.items():
                    y_col = plot_spec.get('y_col', df.columns[1])
                    fig.add_trace(
                        go.Scatter(x=df[x_col], y=df[y_col], name=scenario, mode='lines'),
                        row=row, col=col
                    )
        
        elif plot_type == 'bar':
            # For bar plots
            x_col = plot_spec.get('x_col', data.columns[0])
            y_col = plot_spec.get('y_col', data.columns[1])
            
            fig.add_trace(
                go.Bar(x=data[x_col], y=data[y_col], name=y_col),
                row=row, col=col
            )
        
        elif plot_type == 'scatter':
            # For scatter plots
            x_col = plot_spec.get('x_col', data.columns[0])
            y_col = plot_spec.get('y_col', data.columns[1])
            color_col = plot_spec.get('color_col')
            
            if color_col and color_col in data.columns:
                for color_val in data[color_col].unique():
                    subset = data[data[color_col] == color_val]
                    fig.add_trace(
                        go.Scatter(x=subset[x_col], y=subset[y_col], 
                                 name=f"{color_val}", mode='markers'),
                        row=row, col=col
                    )
            else:
                fig.add_trace(
                    go.Scatter(x=data[x_col], y=data[y_col], mode='markers'),
                    row=row, col=col
                )
        
        elif plot_type == 'pie':
            # For pie charts
            value_col = plot_spec.get('value_col', data.columns[0])
            name_col = plot_spec.get('name_col', data.columns[1])
            
            fig.add_trace(
                go.Pie(values=data[value_col], labels=data[name_col]),
                row=row, col=col
            )
        
        elif plot_type == 'heatmap':
            # For heatmaps
            fig.add_trace(
                go.Heatmap(z=data.values, x=data.columns, y=data.index,
                         colorscale=plot_spec.get('colorscale', 'Viridis')),
                row=row, col=col
            )
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'y':0.99,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        height=height,
        width=width,
        showlegend=True
    )
    
    # Save dashboard
    ensure_directory_exists(os.path.dirname(output_path))
    fig.write_html(output_path)
    logger.info(f"Saved interactive dashboard to {output_path}")
    
    return fig