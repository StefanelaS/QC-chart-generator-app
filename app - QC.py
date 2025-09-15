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

    x_pos = len(initial_data) + 0.02*len(initial_data) # Position text slightly left of the right edge

    ax.text(x_pos, mean, f' Mean = {mean:.2f}', verticalalignment='bottom', color='black', 
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UAL, f' UAL = {UAL:.2f}', verticalalignment='bottom', color='red',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UWL, f' UWL = {UWL:.2f}', verticalalignment='bottom', color='black',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LWL, f' LWL = {LWL:.2f}', verticalalignment='bottom', color='black',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LAL, f' LAL = {LAL:.2f}', verticalalignment='bottom', color='red',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))

    # Set axis limits to create extra space
    ax.set_xticks([])
    ax.set_xlim(0.5, len(initial_data) + 0.23*len(initial_data)) 
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    #plt.tight_layout()
    return fig


def plot_new_data(new_data, initial_data, mean, UAL, UWL, LWL, LAL, x_label, y_label, title):
    """Plot the initial data points with control limits"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Combine initial and new data
    if not isinstance(initial_data, list):
        initial_data = list(initial_data)
    if not isinstance(new_data, list):
        new_data = list(new_data)
    all_data = initial_data + new_data
    
    # Plot initial data points with time steps (blue)
    initial_time_steps = range(1, len(initial_data) + 1)
    ax.plot(initial_time_steps, initial_data, 'bo', markersize=5)
    
    # Plot new data points with time steps (green)
    new_time_steps = range(len(initial_data) + 1, len(all_data) + 1)
    
    # Separate new data points into different categories based on control limits
    green_points = []    # Between UWL and LWL
    orange_points = []   # Between UWL and UAL or between LWL and LAL
    red_points = []      # Above UAL or below LAL

    for i, value in enumerate(new_data):
        if LWL <= value <= UWL:
            green_points.append((new_time_steps[i], value))
        elif (UWL < value <= UAL) or (LAL <= value < LWL):
            orange_points.append((new_time_steps[i], value))
        elif value > UAL or value < LAL:
            red_points.append((new_time_steps[i], value))

    # Plot each category with different colors
    if green_points:
        x_vals, y_vals = zip(*green_points)
        ax.plot(x_vals, y_vals, 'go', markersize=5)
    
    if orange_points:
        x_vals, y_vals = zip(*orange_points)
        ax.plot(x_vals, y_vals, 'o', color='orange', markersize=5)
    
    if red_points:
        x_vals, y_vals = zip(*red_points)
        ax.plot(x_vals, y_vals, 'ro', markersize=5)
    
    # Plot control limits as horizontal lines
    ax.axhline(y=mean, color='black', linestyle='-')
    ax.axhline(y=UAL, color='red', linestyle='--')
    ax.axhline(y=UWL, color='black', linestyle='--')
    ax.axhline(y=LWL, color='black', linestyle='--')
    ax.axhline(y=LAL, color='red', linestyle='--')

    x_pos = len(all_data) + 0.02*len(initial_data)  # Position text slightly left of the right edge

    ax.text(x_pos, mean, f' Mean = {mean:.2f}', verticalalignment='bottom', color='black', 
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UAL, f' UAL = {UAL:.2f}', verticalalignment='bottom', color='red',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, UWL, f' UWL = {UWL:.2f}', verticalalignment='bottom', color='black',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LWL, f' LWL = {LWL:.2f}', verticalalignment='bottom', color='black',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))
    ax.text(x_pos, LAL, f' LAL = {LAL:.2f}', verticalalignment='bottom', color='red',
        bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))

    # Set axis limits to create extra space
    ax.set_xticks([])
    ax.set_xlim(0.5, len(all_data) + 0.23*len(all_data)) 
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    #plt.tight_layout()
    return fig


st.title("📊 QC Chart Generator")
    
st.markdown("""
This app creates QC charts from Excel files.
- **File 1**: Initial data points for calculating control limits
- **File 2**: New data points to monitor against control limits
""")

# Customization inputs - prazno na početku
st.header("Graph customization")
x_label = st.text_input("X-axis Label", "")
y_label = st.text_input("Y-axis Label", "")
title = st.text_input("Plot Title", "")

st.header("Upload Excel file for UAL, UWL, LWL and LAL calculation")
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
st.header("Upload new data Excel file")
new_file = st.file_uploader("Choose second Excel file", type=['xlsx'])

if new_file:
    df2 = pd.read_excel(new_file, header=None)
    new_data = df2.iloc[:, 0].dropna().values
    fig2 = plot_new_data(new_data, initial_data, mean, UAL, UWL, LWL, LAL, x_label, y_label, title)
    st.pyplot(fig2)
























