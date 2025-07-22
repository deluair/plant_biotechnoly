#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Plotting functions for visualizing simulation results.

This module provides functions for creating various plots of simulation data.
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union, Any

from biosimulate.utils.file_utils import ensure_directory_exists

logger = logging.getLogger(__name__)

# Set default style
sns.set(style="whitegrid")


def plot_time_series(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                    title: str, output_path: Optional[str] = None,
                    figsize: Tuple[int, int] = (10, 6), 
                    colors: Optional[List[str]] = None,
                    labels: Optional[List[str]] = None,
                    y_label: str = "", x_label: str = "Year",
                    legend_loc: str = "best") -> plt.Figure:
    """Create a time series plot with multiple lines.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_cols: List of column names for y-axis values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the lines (default: None, use default colors)
        labels: List of labels for the lines (default: None, use y_cols)
        y_label: Label for y-axis
        x_label: Label for x-axis
        legend_loc: Location of the legend
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Use column names as labels if not provided
    if labels is None:
        labels = y_cols
    
    # Plot each line
    for i, y_col in enumerate(y_cols):
        color = colors[i] if colors is not None and i < len(colors) else None
        label = labels[i] if i < len(labels) else y_col
        ax.plot(data[x_col], data[y_col], label=label, color=color)
    
    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    
    # Add legend
    ax.legend(loc=legend_loc)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_stacked_area(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                     title: str, output_path: Optional[str] = None,
                     figsize: Tuple[int, int] = (10, 6), 
                     colors: Optional[List[str]] = None,
                     labels: Optional[List[str]] = None,
                     y_label: str = "", x_label: str = "Year",
                     normalize: bool = False) -> plt.Figure:
    """Create a stacked area plot.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_cols: List of column names for y-axis values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the areas (default: None, use default colors)
        labels: List of labels for the areas (default: None, use y_cols)
        y_label: Label for y-axis
        x_label: Label for x-axis
        normalize: Whether to normalize the data to percentages (default: False)
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Use column names as labels if not provided
    if labels is None:
        labels = y_cols
    
    # Extract x values and y values
    x = data[x_col].values
    y_values = [data[col].values for col in y_cols]
    
    # Normalize if requested
    if normalize:
        # Calculate sum of each row
        sums = np.sum(y_values, axis=0)
        # Normalize each column
        y_values = [y / sums * 100 for y in y_values]
        if y_label == "":
            y_label = "Percentage (%)"
    
    # Create stacked area plot
    ax.stackplot(x, y_values, labels=labels, colors=colors)
    
    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    
    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                  title: str, output_path: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6), 
                  color: str = "steelblue",
                  y_label: str = "", x_label: str = "",
                  horizontal: bool = False,
                  sort_values: bool = False) -> plt.Figure:
    """Create a bar chart.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for categories
        y_col: Column name for values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        color: Color for the bars
        y_label: Label for y-axis
        x_label: Label for x-axis
        horizontal: Whether to create a horizontal bar chart (default: False)
        sort_values: Whether to sort by values (default: False)
        
    Returns:
        Matplotlib Figure object
    """
    # Sort data if requested
    if sort_values:
        data = data.sort_values(by=y_col)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create bar chart
    if horizontal:
        ax.barh(data[x_col], data[y_col], color=color)
        ax.set_xlabel(y_label if y_label else y_col)
        ax.set_ylabel(x_label if x_label else x_col)
    else:
        ax.bar(data[x_col], data[y_col], color=color)
        ax.set_xlabel(x_label if x_label else x_col)
        ax.set_ylabel(y_label if y_label else y_col)
    
    # Set title
    ax.set_title(title)
    
    # Rotate x-axis labels if not horizontal
    if not horizontal and len(data) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7, axis='y' if horizontal else 'both')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_grouped_bar_chart(data: pd.DataFrame, x_col: str, y_cols: List[str], 
                          title: str, output_path: Optional[str] = None,
                          figsize: Tuple[int, int] = (12, 6), 
                          colors: Optional[List[str]] = None,
                          labels: Optional[List[str]] = None,
                          y_label: str = "", x_label: str = "") -> plt.Figure:
    """Create a grouped bar chart.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for categories
        y_cols: List of column names for values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the bars (default: None, use default colors)
        labels: List of labels for the bars (default: None, use y_cols)
        y_label: Label for y-axis
        x_label: Label for x-axis
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Use column names as labels if not provided
    if labels is None:
        labels = y_cols
    
    # Calculate positions for grouped bars
    x = np.arange(len(data))
    width = 0.8 / len(y_cols)  # Width of each bar
    
    # Create grouped bars
    for i, y_col in enumerate(y_cols):
        color = colors[i] if colors is not None and i < len(colors) else None
        label = labels[i] if i < len(labels) else y_col
        pos = x - 0.4 + (i + 0.5) * width  # Position of each bar group
        ax.bar(pos, data[y_col], width, label=label, color=color)
    
    # Set x-axis ticks and labels
    ax.set_xticks(x)
    ax.set_xticklabels(data[x_col])
    
    # Set labels and title
    ax.set_xlabel(x_label if x_label else x_col)
    ax.set_ylabel(y_label if y_label else "Value")
    ax.set_title(title)
    
    # Add legend
    ax.legend()
    
    # Rotate x-axis labels if there are many categories
    if len(data) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_heatmap(data: pd.DataFrame, title: str, output_path: Optional[str] = None,
                figsize: Tuple[int, int] = (10, 8), 
                cmap: str = "viridis",
                annot: bool = True,
                fmt: str = ".2f") -> plt.Figure:
    """Create a heatmap.
    
    Args:
        data: DataFrame containing the data (should be a matrix)
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        cmap: Colormap to use
        annot: Whether to annotate cells with values
        fmt: Format string for annotations
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, ax=ax, cbar_kws={'label': 'Value'})
    
    # Set title
    ax.set_title(title)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_scatter(data: pd.DataFrame, x_col: str, y_col: str, 
                title: str, output_path: Optional[str] = None,
                figsize: Tuple[int, int] = (10, 6), 
                color: str = "steelblue",
                y_label: str = "", x_label: str = "",
                add_trendline: bool = False,
                size_col: Optional[str] = None,
                color_col: Optional[str] = None) -> plt.Figure:
    """Create a scatter plot.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis values
        y_col: Column name for y-axis values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        color: Color for the points (ignored if color_col is provided)
        y_label: Label for y-axis
        x_label: Label for x-axis
        add_trendline: Whether to add a linear trendline
        size_col: Column name for point sizes (default: None)
        color_col: Column name for point colors (default: None)
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Determine point sizes if size_col is provided
    sizes = None
    if size_col is not None:
        sizes = data[size_col] * 100  # Scale sizes for visibility
    
    # Create scatter plot
    if color_col is not None:
        scatter = ax.scatter(data[x_col], data[y_col], 
                           s=sizes, 
                           c=data[color_col], 
                           cmap='viridis', 
                           alpha=0.7)
        plt.colorbar(scatter, label=color_col)
    else:
        ax.scatter(data[x_col], data[y_col], 
                 s=sizes, 
                 color=color, 
                 alpha=0.7)
    
    # Add trendline if requested
    if add_trendline:
        z = np.polyfit(data[x_col], data[y_col], 1)
        p = np.poly1d(z)
        ax.plot(data[x_col], p(data[x_col]), "r--", alpha=0.8)
    
    # Set labels and title
    ax.set_xlabel(x_label if x_label else x_col)
    ax.set_ylabel(y_label if y_label else y_col)
    ax.set_title(title)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_pie_chart(data: pd.DataFrame, value_col: str, label_col: str, 
                  title: str, output_path: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 8), 
                  colors: Optional[List[str]] = None,
                  explode: Optional[List[float]] = None,
                  autopct: str = '%1.1f%%') -> plt.Figure:
    """Create a pie chart.
    
    Args:
        data: DataFrame containing the data
        value_col: Column name for values
        label_col: Column name for labels
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the pie slices
        explode: List of values to "explode" slices (default: None)
        autopct: Format string for percentage labels
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create pie chart
    ax.pie(data[value_col], labels=data[label_col], 
          colors=colors, explode=explode, autopct=autopct,
          shadow=True, startangle=90)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Set title
    ax.set_title(title)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_radar_chart(data: pd.DataFrame, categories: List[str], 
                    value_cols: List[str], title: str, 
                    output_path: Optional[str] = None,
                    figsize: Tuple[int, int] = (10, 8), 
                    colors: Optional[List[str]] = None,
                    labels: Optional[List[str]] = None) -> plt.Figure:
    """Create a radar chart (spider plot).
    
    Args:
        data: DataFrame containing the data
        categories: List of category names
        value_cols: List of column names for values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the lines
        labels: List of labels for the lines (default: None, use value_cols)
        
    Returns:
        Matplotlib Figure object
    """
    # Use column names as labels if not provided
    if labels is None:
        labels = value_cols
    
    # Number of categories
    N = len(categories)
    
    # Create angles for each category
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    
    # Make the plot circular by repeating the first angle
    angles += angles[:1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    
    # Plot each value set
    for i, col in enumerate(value_cols):
        # Extract values and repeat the first value to close the loop
        values = data[col].tolist()
        values += values[:1]
        
        # Plot values
        color = colors[i] if colors is not None and i < len(colors) else None
        label = labels[i] if i < len(labels) else col
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=label, color=color)
        ax.fill(angles, values, alpha=0.1, color=color)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Set title
    ax.set_title(title)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def plot_scenario_comparison(data_dict: Dict[str, pd.DataFrame], x_col: str, y_col: str, 
                           title: str, output_path: Optional[str] = None,
                           figsize: Tuple[int, int] = (12, 6), 
                           colors: Optional[List[str]] = None,
                           y_label: str = "", x_label: str = "Year") -> plt.Figure:
    """Create a line plot comparing the same metric across different scenarios.
    
    Args:
        data_dict: Dictionary mapping scenario names to DataFrames
        x_col: Column name for x-axis values
        y_col: Column name for y-axis values
        title: Plot title
        output_path: Path to save the plot (default: None, don't save)
        figsize: Figure size as (width, height) in inches
        colors: List of colors for the lines
        y_label: Label for y-axis
        x_label: Label for x-axis
        
    Returns:
        Matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each scenario
    for i, (scenario, df) in enumerate(data_dict.items()):
        color = colors[i] if colors is not None and i < len(colors) else None
        ax.plot(df[x_col], df[y_col], label=scenario, color=color, linewidth=2)
    
    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label if y_label else y_col)
    ax.set_title(title)
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Tight layout
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path is not None:
        ensure_directory_exists(os.path.dirname(output_path))
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig


def create_dashboard(data_dict: Dict[str, pd.DataFrame], 
                    output_path: str,
                    title: str = "Simulation Results Dashboard") -> None:
    """Create a dashboard with multiple plots.
    
    Args:
        data_dict: Dictionary mapping plot names to DataFrames
        output_path: Path to save the dashboard
        title: Dashboard title
    """
    # Determine number of plots and layout
    n_plots = len(data_dict)
    n_cols = min(3, n_plots)  # Maximum 3 plots per row
    n_rows = (n_plots + n_cols - 1) // n_cols  # Ceiling division
    
    # Create figure
    fig = plt.figure(figsize=(6*n_cols, 5*n_rows))
    fig.suptitle(title, fontsize=16)
    
    # Create each subplot
    for i, (plot_name, plot_data) in enumerate(data_dict.items()):
        ax = fig.add_subplot(n_rows, n_cols, i+1)
        
        # Determine plot type based on data structure
        if isinstance(plot_data, dict) and 'type' in plot_data:
            plot_type = plot_data['type']
            df = plot_data['data']
            
            if plot_type == 'line':
                x_col = plot_data.get('x_col', 'year')
                y_cols = plot_data.get('y_cols', df.columns.tolist())
                y_cols = [col for col in y_cols if col != x_col]  # Exclude x_col
                
                for y_col in y_cols:
                    ax.plot(df[x_col], df[y_col], label=y_col)
                
                ax.set_xlabel(plot_data.get('x_label', x_col))
                ax.set_ylabel(plot_data.get('y_label', ''))
                ax.legend()
                
            elif plot_type == 'bar':
                x_col = plot_data.get('x_col', df.columns[0])
                y_col = plot_data.get('y_col', df.columns[1])
                
                ax.bar(df[x_col], df[y_col])
                ax.set_xlabel(plot_data.get('x_label', x_col))
                ax.set_ylabel(plot_data.get('y_label', y_col))
                
                if len(df) > 5:
                    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
                
            elif plot_type == 'pie':
                value_col = plot_data.get('value_col', df.columns[0])
                label_col = plot_data.get('label_col', df.columns[1])
                
                ax.pie(df[value_col], labels=df[label_col], autopct='%1.1f%%')
                ax.axis('equal')
                
            elif plot_type == 'heatmap':
                sns.heatmap(df, annot=plot_data.get('annot', True), 
                           cmap=plot_data.get('cmap', 'viridis'), ax=ax)
        else:
            # Default to line plot for simple DataFrames
            if 'year' in plot_data.columns:
                x_col = 'year'
                y_cols = [col for col in plot_data.columns if col != 'year']
                
                for y_col in y_cols:
                    ax.plot(plot_data[x_col], plot_data[y_col], label=y_col)
                
                ax.set_xlabel('Year')
                ax.legend()
            else:
                # Just plot all columns
                plot_data.plot(ax=ax)
        
        ax.set_title(plot_name)
        ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Leave space for suptitle
    
    # Save dashboard
    ensure_directory_exists(os.path.dirname(output_path))
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Saved dashboard to {output_path}")