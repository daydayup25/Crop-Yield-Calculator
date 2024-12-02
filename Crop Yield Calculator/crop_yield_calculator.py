#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:11:59 2024

@author: jemilsan
"""

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Initialise the main window
root = tk.Tk()
root.title("Crop Yield and Profit Calculator")
root.geometry("1200x800")

# Define variables to store user inputs
area = tk.DoubleVar()  # Area in hectares
crop_yield = tk.StringVar()  # Yield of the crop
crop_cost = tk.StringVar()  # Cost associated with the crop

# Define available intercropping methods
intercropping_methods = {
    'Row': 'Row',
    'Trap': 'Trap',
    'Guard': 'Guard'
}

# Define primary crop options for each intercropping method
primary_crops = {
    'Row': ["Wheat", "OSR", "Potato"],
    'Trap': ["Wheat", "OSR", "Potato"],
    'Guard': ["Wheat", "Strawberry", "Potato"]
}

# Define crop combinations for each intercropping method
row_combinations = {
    "Wheat": "Beans",
    "OSR": "Beans",  
    "Potato": "Beans"
}

trap_combinations = {
    "Wheat": "Strawberry",
    "OSR": "Strawberry",
    "Potato": "Strawberry"
}

guard_combinations = {
    "Wheat": "OSR",
    "Strawberry": "OSR",
    "Potato": "OSR"
}


# Soil grade factors for nitrogen-fixing and non-nitrogen-fixing crops
soil_factors_nitrogen = {
    "Grade 1": [1.52, 1.62, 1.83, 1.93, 1.95],
    "Grade 2": [1.22, 1.29, 1.46, 1.53, 1.55],
    "Grade 3": [1.01, 1.06, 1.18, 1.23, 1.25],
    "Grade 4": [0.8, 0.82, 0.87, 0.89, 0.9],
    "Grade 5": [0.5, 0.51, 0.54, 0.55, 0.55]
}

soil_factors_non_nitrogen = {
    "Grade 1": [1.51, 1.54, 1.61, 1.64, 1.65],
    "Grade 2": [1.21, 1.24, 1.31, 1.34, 1.35],
    "Grade 3": [1.0, 1.04, 1.11, 1.14, 1.15],
    "Grade 4": [0.8, 0.81, 0.84, 0.85, 0.85],
    "Grade 5": [0.5, 0.51, 0.52, 0.52, 0.52]
}

# Define weather factors for each intercropping method
weather_factors = {
    'Row': [1.09, 1.03, 1.17, 0.92, 1.2],
    'Trap': [1.63, 0.97, 1.03, 0.9, 1.9],
    'Guard': [1.48, 1.41, 1.03, 1.04, 1.12]
}

# Define pesticide factors for each crop and intercropping method
pesticide_factors = {
    'Wheat': {'Row': 0.925, 'Trap': 1.3, 'Guard': 1.325},
    'OSR': {'Row': 0.75, 'Trap': 1.25, 'Guard': 1.0},
    'Potato': {'Row': 0.825, 'Trap': 1.075, 'Guard': 0.95},
    'Strawberry': {'Row': 0.66, 'Trap': 1.06, 'Guard': 0.81}
}

# Area ratios for primary-to-secondary crop allocation in intercropping methods
row_ratios = {
    "Wheat": 8 / 11,  # 8:3 primary-to-secondary ratio
    "OSR": 8 / 11,    # 8:3 primary-to-secondary ratio
    "Potato": 3 / 4,  # 3:1 primary-to-secondary ratio
}

trap_ratio = 0.8  # 80% primary, 20% secondary
guard_ratio = 3 / 5  # 3:2 primary-to-secondary ratio

# Crop data, including average yield per hectare and cost per hectare
crop_types = {
    'Wheat': [8.2, 500],      # 8.2 tonnes/ha, 500 £/ha
    'OSR': [3.4, 650],        # 3.4 tonnes/ha, 650 £/ha
    'Potato': [46, 800],      # 46 tonnes/ha, 800 £/ha
    'Strawberry': [16, 6000], # 16 tonnes/ha, 6000 £/ha
    'Beans': [3, 300]         # 3 tonnes/ha, 300 £/ha
}

# Define prices per tonne for each crop (market prices)
crop_prices = {
    'Wheat': 247,
    'OSR': 471,
    'Potato': 662,
    'Strawberry': 2608,
    'Beans': 310
}

# Additional intercropping costs per hectare for each method
intercropping_costs = {
    'Row': {
        'herb': 125,           # Herbicide cost (£/hectare)
        'labour': 300,         # Labour cost (£/hectare)
        'machine': 225         # Machine cost (£/hectare)
    },
    'Trap': {
        'fertilizer': 200,     # Fertiliser cost (£/hectare)
        'labour': 75,          # Labour cost (£/hectare)
        'machine': 175         # Machine cost (£/hectare)
    },
    'Guard': {
        'fertilizer': 200,     # Fertiliser cost (£/hectare)
        'labour': 75,          # Labour cost (£/hectare)
        'machine': 175         # Machine cost (£/hectare)
    }
}

# Default selections for dropdown menus
selected_intercropping = tk.StringVar(value='Row')
selected_crop = tk.StringVar(value='Wheat')
selected_soil_grade = tk.StringVar(value='Grade 1')


# Function to update the available crop options based on selected intercropping method
def update_crop_options(*args):
    method = selected_intercropping.get()
    options = primary_crops.get(method, [])
    selected_crop.set(options[0])  # Set default to the first option
    crop_menu['menu'].delete(0, 'end')
    for crop in options:
        crop_menu['menu'].add_command(label=crop, command=lambda value=crop: selected_crop.set(value))


# Validate user inputs to ensure they are complete and correct
def validate_inputs():
    if not area.get():
        messagebox.showerror("Error", "Please enter a valid area in hectares.")
        return False
    if selected_crop.get() not in crop_types:
        messagebox.showerror("Error", "Please select a valid crop.")
        return False
    if selected_soil_grade.get() not in soil_factors_nitrogen:
        messagebox.showerror("Error", "Please select a valid soil grade.")
        return False
    if selected_intercropping.get() not in intercropping_methods:
        messagebox.showerror("Error", "Please select a valid intercropping method.")
        return False
    return True

# Calculate the profit for secondary crops based on selected method and crop
def calculate_secondary_profit(area, method, crop):
    if method == "Row":
        secondary_crop = row_combinations.get(crop, None)
    elif method == "Trap":
        secondary_crop = trap_combinations.get(crop, None)
    elif method == "Guard":
        secondary_crop = guard_combinations.get(crop, None)
    else:
        return 0, 0

    if not secondary_crop:
        return 0, 0

    # Calculate secondary yield, cost, revenue, and profit
    secondary_yield = crop_types[secondary_crop][0]
    secondary_cost = crop_types[secondary_crop][1]
    secondary_price = crop_prices[secondary_crop]

    ratio = 1 - (row_ratios.get(crop, 1) if method == "Row" else (trap_ratio if method == "Trap" else guard_ratio))
    allocated_area = area * ratio

    total_yield_secondary = secondary_yield * allocated_area
    total_cost_secondary = secondary_cost * allocated_area
    total_revenue_secondary = total_yield_secondary * secondary_price
    total_profit_secondary = total_revenue_secondary - total_cost_secondary

    return total_profit_secondary
  

# Main function to calculate yield and profit for each year
def calculate_yield():
    if not validate_inputs():
        return
    try:
        area_value = area.get()
        crop = selected_crop.get()
        method = selected_intercropping.get()
        soil_grade = selected_soil_grade.get()

        # Fetch average yield per hectare (EYi)
        EYi = crop_types[crop][0]

        # Determine relevant ratio based on intercropping method
        if method == 'Row':
            relevant_ratio = row_ratios.get(crop, 1)
        elif method == 'Trap':
            relevant_ratio = trap_ratio
        elif method == 'Guard':
            relevant_ratio = guard_ratio
        else:
            relevant_ratio = 1

        # Get soil factors based on nitrogen-fixing or non-nitrogen-fixing crops
        soil_factors = soil_factors_nitrogen if method == 'Row' else soil_factors_non_nitrogen
        soil_factors = soil_factors[soil_grade]

        # Get weather factors and pesticide factors based on intercropping method
        weather = weather_factors[method]
        pesticides = [pesticide_factors[crop][method]] * 5

        # Calculate additional intercropping costs per hectare
        inter_crop_costs = intercropping_costs[method]
        additional_cost_per_hectare = sum(inter_crop_costs.values())

        # Calculate yield per hectare and profit for each year
        historical_yields = []
        profits = []
        for t in range(5):
            # Calculate yield for year t
            Yi_t = (EYi * relevant_ratio) * soil_factors[t] * pesticides[t] * weather[t]
            historical_yields.append(Yi_t)  # Yield per hectare

            # Calculate primary revenue and cost
            primary_revenue = Yi_t * area_value * crop_prices[crop]
            primary_cost = (crop_types[crop][1] * area_value * relevant_ratio) + (additional_cost_per_hectare * area_value)
            primary_profit = primary_revenue - primary_cost

            # Calculate secondary profit
            secondary_profit = calculate_secondary_profit(area_value, method, crop)
            
            # Calculate total profit (primary + secondary crops)
            total_profit = primary_profit + secondary_profit

            profits.append(total_profit)

        # Plot yield and profit graphs
        plot_yield_graph(5, historical_yields)
        plot_profit_graph(5, profits)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Plot yield graph over the years
def plot_yield_graph(years, historical_yields):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, years + 1), historical_yields, color='blue', marker='o', markersize=8)
    ax.set_xlabel("Years")
    ax.set_ylabel("Yield (tonnes per hectare)")
    ax.set_title("Primary Crop Yield Over 5 Years")

    # Set x-axis limits to give more space on the left and right
    ax.set_xlim(0.7, years + 0.3)
    
    # Set y-axis limits to ensure balanced spacing above and below the line
    y_range = max(historical_yields) - min(historical_yields)
    y_min = min(historical_yields) - (y_range * 0.2 if y_range > 0 else 1)
    y_max = max(historical_yields) + (y_range * 0.2 if y_range > 0 else 1)
    ax.set_ylim(y_min, y_max)

    # Plot text labels for yield values, always above the bullet marker
    offset = 0.1  # Offset to move the text above the marker
    for i, yield_val in enumerate(historical_yields):
        # Position label above the marker
        y_pos = yield_val + offset
        ax.text(i + 1, y_pos, f"{yield_val:.2f} t/ha", ha='center', va='bottom', fontsize=11)

    # Tighten the layout to ensure all elements fit well within the figure area
    fig.tight_layout()
    
    # Display the plot in the application window
    canvas = FigureCanvasTkAgg(fig, master=frame_yield)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, pady=20)

# Plot profit graph over the years
def plot_profit_graph(years, profits):
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.35
    x = np.arange(1, years + 1)

    # Set bar colours to green for profit and red for loss
    colors = ['green' if profit >= 0 else 'red' for profit in profits]
    ax.bar(x, profits, width, color=colors, alpha=0.7)
    ax.set_xlabel("Years")
    ax.set_ylabel("Profit (£)")
    ax.set_title("Profit Over 5 Years (Primary + Secondary Crops)")
    ax.set_xlim(0.5, years + 0.5)
    ax.set_ylim(min(profits) * 1.2 if min(profits) < 0 else 0, max(profits) * 1.2)  # Scale y-axis to 20% beyond the min/max profit
    
    # Plot text labels for profit values above each bar
    for i, profit in enumerate(profits):
        ax.text(i + 1, profit, f"£{profit:.2f}", ha='center', va='bottom' if profit >= 0 else 'top', color='black')
    
    # Display the plot in the application window
    canvas = FigureCanvasTkAgg(fig, master=frame_profit)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, pady=20)

# Define the inputs section frame with a grid layout
frame_inputs = tk.Frame(root)
frame_inputs.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="n")

# Inputs Section
tk.Label(frame_inputs, text="Intercropping Method:", fg="black", font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=5, padx=10)
tk.OptionMenu(frame_inputs, selected_intercropping, *intercropping_methods.keys(), command=update_crop_options).grid(row=0, column=1, pady=5, padx=10)

tk.Label(frame_inputs, text="Primary Crop:", fg="black", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=5, padx=10)
crop_menu = tk.OptionMenu(frame_inputs, selected_crop, *primary_crops['Row'])
crop_menu.grid(row=1, column=1, pady=5, padx=10)

tk.Label(frame_inputs, text="Area (ha):", fg="black", font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=5, padx=10)
tk.Entry(frame_inputs, textvariable=area, font=("Arial", 12), width=10).grid(row=2, column=1, pady=5, padx=10)

tk.Label(frame_inputs, text="Soil Grade:", fg="black", font=("Arial", 12)).grid(row=3, column=0, sticky='w', pady=5, padx=10)
tk.OptionMenu(frame_inputs, selected_soil_grade, "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5").grid(row=3, column=1, pady=5, padx=10)

tk.Button(frame_inputs, text="Calculate Yield and Profit", command=calculate_yield, bg="#4CAF50", fg="black", font=("Arial", 12), height=2, width=20).grid(row=4, column=0, columnspan=2, pady=20)

# Frame to display yield and profit graphs
frame_results = tk.Frame(root)
frame_results.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

# Yield Graph Section (left side of frame_results)
frame_yield = tk.Frame(frame_results)
frame_yield.grid(row=0, column=0, padx=20, pady=10)

tk.Label(frame_yield, text="Yield Graph", font=("Arial", 12, "bold"), fg="black").grid(row=0, column=0, pady=5)
canvas_yield = tk.Canvas(frame_yield, width=400, height=300)
canvas_yield.grid(row=1, column=0)

# Profit and Cost Graph Section (right side of frame_results)
frame_profit = tk.Frame(frame_results)
frame_profit.grid(row=0, column=1, padx=20, pady=10)

tk.Label(frame_profit, text="Profit and Cost Graph", font=("Arial", 12, "bold"), fg="black").grid(row=0, column=0, pady=5)
canvas_profit = tk.Canvas(frame_profit, width=400, height=300)
canvas_profit.grid(row=1, column=0)

# Start the main loop to run the GUI
root.mainloop()
