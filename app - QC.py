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

def plot_initial_data(initial_data, mean, UAL, UWL, LWL, LAL, x_label, y_label, title):
    """Plot the initial data points with control limits"""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot initial data points with time steps
    time_steps = range(1, len(initial_data) + 1)
    ax.plot(time_steps, initial_data, 'bo', markersize=5)
    
    # Plot control limits as horizontal lines
    ax.axhline(y=mean, color='black', linestyle='-')
    ax.axhline(y=UAL, color='red', linestyle='--')
    ax.axhline(y=UWL, color='black', linestyle='--')
    ax.axhline(y=LWL, color='black', linestyle='--')
    ax.axhline(y=LAL, color='red', linestyle='--')

    x_pos = len(initial_data) - 0.2  # Position text slightly left of the right edge

    ax.text(x_pos, mean, f' Mean ({mean:.2f})', verticalalignment='center', color='black', 
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UAL, f' UAL ({UAL:.2f})', verticalalignment='center', color='red',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UWL, f' UWL ({UWL:.2f})', verticalalignment='center', color='black',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LWL, f' LWL ({LWL:.2f})', verticalalignment='center', color='black',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LAL, f' LAL ({LAL:.2f})', verticalalignment='center', color='red',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    return fig

    

st.title("📊 QC Chart Generator")
    
st.markdown("""
This app creates QC charts from Excel files.
- **File 1**: Initial data points for calculating control limits
- **File 2**: New data points to monitor against control limits
""")

# Customization inputs - prazno na početku
st.header("Graph Customization")
x_label = st.text_input("X-axis Label", "")
y_label = st.text_input("Y-axis Label", "")
title = st.text_input("Plot Title", "")

initial_file = st.file_uploader("Choose first Excel file", type=['xlsx'])

if initial_file:
    # Load the Excel file - use the first column
    df1 = pd.read_excel(initial_file, header=None)  # No header
    initial_data = df1.iloc[:, 0].dropna().values  # Get first column data

    # Calculate control limits
    mean, std, UAL, UWL, LWL, LAL = calculate_control_limits(initial_data)
    fig1 = plot_initial_data(initial_data, mean, UAL, UWL, LWL, LAL, x_label, y_label, title)
    st.pyplot(fig1)

# Upload second Excel file (for next step)
st.header("Upload New Data Excel File")
new_file = st.file_uploader("Choose second Excel file", type=['xlsx'])

if new_file:
    df2 = pd.read_excel(new_file, header=None)
    new_data = df2.iloc[:, 0].dropna().values







