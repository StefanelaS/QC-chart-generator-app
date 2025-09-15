# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:14:38 2024

@author: Korisnik
"""

# load libraries
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Function to load and process the table
def load_excel(file):
    df = pd.read_excel(file)
    df.columns = ['Sample', 'Ratio', 'C']
    
    # Compute the reference ratio dynamically based on all available measurements for the first concentration
    first_concentration = df['C'].iloc[0]
    reference_data = df[df['C'] == first_concentration]
    reference_ratio = reference_data['Ratio'].mean()
    
    # Compute the difference of each "Ratio" from the reference_ratio
    df['Diff'] = df['Ratio'] - reference_ratio
    return df

def calculate_control_limits(initial_data):    
    # Calculate mean and std for the initial window
    mean = np.mean(initial_data)
    std = np.std(initial_data, ddof=1)  # Sample standard deviation
    
    # Calculate control limits
    UAL = mean + 3 * std  # Upper Action Limit
    UWL = mean + 2 * std  # Upper Warning Limit
    LWL = mean - 2 * std  # Lower Warning Limit
    LAL = mean - 3 * std  # Lower Action Limit
    return mean, std, UAL, UWL, LWL, LAL

def plot_initial_data_with_limits(initial_data, mean, UAL, UWL, LWL, LAL):
    """Plot the initial data points with control limits"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot initial data points with time steps
    time_steps = range(1, len(initial_data) + 1)
    ax.plot(time_steps, initial_data, 'bo', markersize=5)
    
    # Plot control limits as horizontal lines
    ax.axhline(y=mean, color='black', linestyle='-')
    ax.axhline(y=UAL, color='red', linestyle='--')
    ax.axhline(y=UWL, color='black', linestyle='--')
    ax.axhline(y=LWL, color='black', linestyle='--')
    ax.axhline(y=LAL, color='red', linestyle='--')

    # Add text labels on the right side of the plot
    x_max = len(initial_data) + 0.5  # Right edge of the plot
    
    ax.text(x_max, mean, f' Mean ({mean:.2f})', verticalalignment='center', color='black')
    ax.text(x_max, UAL, f' UAL ({UAL:.2f})', verticalalignment='center', color='red')
    ax.text(x_max, UWL, f' UWL ({UWL:.2f})', verticalalignment='center', color='black')
    ax.text(x_max, LWL, f' LWL ({LWL:.2f})', verticalalignment='center', color='black')
    ax.text(x_max, LAL, f' LAL ({LAL:.2f})', verticalalignment='center', color='red')
    
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Value')
    ax.set_title('Initial Data with Control Limits')
    ax.legend()


def generate_plot(df):
    
    c = (df['Diff'] - model.intercept_) / model.coef_[0]
    accuracy = (c / df['C']).replace([float('inf'), -float('inf')], None) * 100
    
    new_df = pd.DataFrame({
        'Sample': df['Sample'],
        'Real Ratio': df['Ratio'],
        'Real C': df['C'],
        'Shifted Ratio': df['Diff'],
        'Calculated C': c,
        'Accuracy (%)': accuracy})
    
    return fig
    

def main():
    st.title("📊 QC Chart Generator")
    
    st.markdown("""
    This app creates QC charts from Excel files.
    - **File 1**: Initial data points for calculating control limits
    - **File 2**: New data points to monitor against control limits
    """)
    initial_file = st.file_uploader("Choose first Excel file", type=['xlsx'])

    if initial_file:
        # Load the Excel file - use the first column
        df1 = pd.read_excel(initial_file, header=None)  # No header
        initial_data = df1.iloc[:, 0].dropna().values  # Get first column data

        # Calculate control limits
        mean, std, UAL, UWL, LWL, LAL = calculate_control_limits(initial_data)


