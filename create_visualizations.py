#!/usr/bin/env python
"""
BIOSIMULATE Visualization Generator
Creates comprehensive visualizations from simulation results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import glob
from datetime import datetime

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_latest_results():
    """Load the most recent simulation results"""
    results_dir = Path('results')
    csv_files = list(results_dir.glob('baseline_*.csv'))
    
    if not csv_files:
        raise FileNotFoundError("No simulation results found in results/ directory")
    
    # Get the most recent file
    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"Loading data from: {latest_file}")
    
    return pd.read_csv(latest_file)

def create_time_series_plot(df):
    """Create time series plot of product count and pricing over years"""
    plt.figure(figsize=(12, 8))
    
    # Aggregate product count by year
    yearly_products = df.groupby('year')['product_id'].nunique().reset_index()
    yearly_products.columns = ['year', 'product_count']
    
    plt.subplot(2, 2, 1)
    plt.plot(yearly_products['year'], yearly_products['product_count'], 
             marker='o', linewidth=3, markersize=8, color='#2E86AB')
    plt.title('Product Portfolio Growth Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of Products')
    plt.grid(True, alpha=0.3)
    
    return yearly_products

def create_regional_analysis(df):
    """Create year distribution analysis"""
    # Count products by year
    year_counts = df['year'].value_counts().sort_index()
    
    plt.subplot(2, 2, 2)
    colors = plt.cm.Set3(np.linspace(0, 1, len(year_counts)))
    wedges, texts, autotexts = plt.pie(year_counts.values, labels=year_counts.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Product Records Distribution by Year', fontsize=14, fontweight='bold')
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    return year_counts

def create_product_performance(df):
    """Create product count by year analysis"""
    # Get product count by year
    yearly_counts = df.groupby('year')['product_id'].nunique().reset_index()
    yearly_counts.columns = ['year', 'product_count']
    
    plt.subplot(2, 2, 3)
    bars = plt.bar(yearly_counts['year'], yearly_counts['product_count'], 
                   color='#A23B72', alpha=0.8)
    plt.title('Unique Products by Year', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of Unique Products')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    return yearly_counts

def create_price_analysis(df):
    """Create average price trend analysis"""
    # Calculate average price by year
    yearly_prices = df.groupby('year')['average_price'].mean().reset_index()
    
    plt.subplot(2, 2, 4)
    plt.plot(yearly_prices['year'], yearly_prices['average_price'], 
             marker='s', linewidth=3, markersize=8, color='#C73E1D')
    plt.title('Average Product Price Trend', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Average Price ($)')
    plt.grid(True, alpha=0.3)
    
    return yearly_prices

def create_comprehensive_dashboard(df):
    """Create a comprehensive dashboard with multiple visualizations"""
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('BIOSIMULATE: Plant Biotechnology Industry Analysis Dashboard', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Time series analysis
    yearly_products = create_time_series_plot(df)
    
    # Year distribution analysis
    year_counts = create_regional_analysis(df)
    
    # Product performance
    yearly_counts = create_product_performance(df)
    
    # Price analysis
    yearly_prices = create_price_analysis(df)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the dashboard
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'results/dashboard_{timestamp}.png', dpi=300, bbox_inches='tight')
    print(f"Dashboard saved as: results/dashboard_{timestamp}.png")
    
    return fig

def create_regional_heatmap(df):
    """Create a heatmap showing product distribution by year and price ranges"""
    # Create price bins
    df['price_range'] = pd.cut(df['average_price'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    # Create pivot table for heatmap
    price_by_year = df.groupby(['year', 'price_range']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(price_by_year.T, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Product Count'}, linewidths=0.5)
    plt.title('Product Distribution by Year and Price Range', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Price Range', fontsize=12)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'results/product_heatmap_{timestamp}.png', dpi=300, bbox_inches='tight')
    print(f"Product heatmap saved as: results/product_heatmap_{timestamp}.png")
    
    return price_by_year

def create_market_growth_analysis(df):
    """Create product portfolio growth analysis"""
    yearly_products = df.groupby('year')['product_id'].nunique().reset_index()
    yearly_products.columns = ['year', 'product_count']
    yearly_products['growth_rate'] = yearly_products['product_count'].pct_change() * 100
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Product count trend
    ax1.plot(yearly_products['year'], yearly_products['product_count'], 
             marker='o', linewidth=3, markersize=8, color='#2E86AB')
    ax1.set_title('Product Portfolio Growth Trend', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Products')
    ax1.grid(True, alpha=0.3)
    
    # Growth rate
    colors = ['red' if x < 0 else 'green' for x in yearly_products['growth_rate'].fillna(0)]
    ax2.bar(yearly_products['year'][1:], yearly_products['growth_rate'][1:], 
            color=colors, alpha=0.7)
    ax2.set_title('Year-over-Year Product Growth Rate', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Growth Rate (%)')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(f'results/growth_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
    print(f"Growth analysis saved as: results/growth_analysis_{timestamp}.png")
    
    return yearly_products

def generate_summary_report(df):
    """Generate a summary report of key metrics"""
    print("\n" + "="*60)
    print("BIOSIMULATE SIMULATION SUMMARY REPORT")
    print("="*60)
    
    print(f"\nSimulation Period: {df['year'].min()} - {df['year'].max()}")
    print(f"Total Products Analyzed: {df['product_id'].nunique()}")
    print(f"Total Data Points: {len(df)}")
    
    print(f"\nPRODUCT METRICS:")
    print(f"Average Product Price: ${df['average_price'].mean():.2f}")
    print(f"Price Range: ${df['average_price'].min():.2f} - ${df['average_price'].max():.2f}")
    print(f"Price Standard Deviation: ${df['average_price'].std():.2f}")
    
    print(f"\nYEARLY BREAKDOWN:")
    yearly_stats = df.groupby('year').agg({
        'product_id': 'nunique',
        'average_price': 'mean'
    }).round(2)
    
    for year, row in yearly_stats.iterrows():
        print(f"  {year}: {int(row['product_id'])} products, avg price ${row['average_price']:.2f}")
    
    print(f"\nSAMPLE PRODUCTS:")
    sample_products = df['product_id'].unique()[:5]
    for i, product in enumerate(sample_products, 1):
        product_data = df[df['product_id'] == product].iloc[0]
        print(f"  {i}. {product}: ${product_data['average_price']:.2f}")
    
    print(f"\nNOTE: This simulation generated product portfolio data with pricing information.")
    print(f"Sales values are currently at zero, indicating the simulation is tracking")
    print(f"product development and pricing phases rather than active market sales.")
    
    print("\n" + "="*60)

def main():
    """Main function to generate all visualizations"""
    try:
        # Load data
        df = load_latest_results()
        
        # Generate summary report
        generate_summary_report(df)
        
        # Create visualizations
        print("\nGenerating visualizations...")
        
        # Main dashboard
        create_comprehensive_dashboard(df)
        
        # Regional heatmap
        create_regional_heatmap(df)
        
        # Growth analysis
        create_market_growth_analysis(df)
        
        print("\nAll visualizations have been generated successfully!")
        print("Check the 'results/' directory for the generated charts.")
        
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()