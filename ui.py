# File: jupyter_notebook_app.ipynb

import ipywidgets as widgets
from IPython.display import display, HTML
import pandas as pd
import numpy as np
import re

# Define CSS for styling
style = """
<style>
    body {
        background-color:#f8f9f9; /* Light blue background color for the page */
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .box {
        width: 45%;
        height: 300px;
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
    }
    .loading-bars {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 10px;
        color: green;
    }
    .loading-bar-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .loading-bar-label {
        width: 40px;
    }
    .right-box-content {
        color: red;
        font-size: 24px;
        display: none;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .right-box-content-false {
        color: green;
        font-size: 24px;
        display: none;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
</style>
"""

# Display the CSS
display(HTML(style))

# Create input box and submit button
input_box = widgets.Text(
    value='',
    placeholder='Enter something',
    description='Input:',
    disabled=False
)
submit_button = widgets.Button(
    description='Submit',
    disabled=False,
    button_style='', 
    tooltip='Click me',
    icon='check'
)


# Create a centered title
title = widgets.Label(
    value='PCI - POTENTIAL COMPLAINT INDICATOR',
    layout=widgets.Layout(font_size='50px', font_weight='bold', text_align='center', margin='10px')
)

# Arrange input box and submit button horizontally and center them
top_center = widgets.HBox([input_box, submit_button], layout=widgets.Layout(justify_content='center', margin='10px'))

# Create rectangular boxes
left_box = widgets.VBox([], layout=widgets.Layout(height='300px', border='1px solid #ccc', padding='10px', margin='10px', visibility='hidden'))


right_box_content = widgets.HTML(
    value='<div class="right-box-content" id="complaint">Potential Complaint</div>',
    layout=widgets.Layout(height='300px', border='1px solid #ccc', padding='10px', margin='10px', visibility='hidden')
)

# Create a dummy dataframe with start and end values for each loading bar
np.random.seed(0)  # For reproducibility
data = {
    'Loading Bar': [f'Loading {i+1}' for i in range(10)],
    'Start Value': np.random.choice(
        [np.random.uniform(0, 10), np.random.uniform(-5, 5), np.random.uniform(0, 1), np.random.uniform(0, 100)], size=10),
    'End Value': np.random.choice(
        [np.random.uniform(0, 10), np.random.uniform(-5, 5), np.random.uniform(0, 1), np.random.uniform(0, 100)], size=10)
}

df = pd.DataFrame(data)

# Create loading bars for the left rectangular box
loading_bars = []
for i in range(10):
    start_value = df.loc[i, 'Start Value']
    end_value = df.loc[i, 'End Value']
    start_label = widgets.Label(value=f"{start_value:.2f}")
    end_label = widgets.Label(value=f"{end_value:.2f}")
    progress_bar = widgets.FloatProgress(
        value=min(start_value, end_value), 
        min=min(start_value, end_value), 
        max=max(start_value, end_value), 
        description=f'Metric {i+1}')
    bar_container = widgets.HBox([start_label, progress_bar, end_label], layout=widgets.Layout(justify_content='space-between'))
    loading_bars.append((start_label, progress_bar, end_label, bar_container))

# Arrange loading bars in a grid format (5 rows, 2 columns)
loading_bars_container = widgets.GridBox([bar[3] for bar in loading_bars], layout=widgets.Layout(grid_template_columns="repeat(2, 1fr)", grid_gap='10px'))

# Add loading bars to the left box
left_box.children = [loading_bars_container]

# Arrange rectangular boxes side by side and center them
rectangular_boxes = widgets.HBox([left_box, right_box_content], layout=widgets.Layout(justify_content='center'))

# Combine all components into the final layout
final_layout = widgets.VBox([title,top_center, rectangular_boxes], layout=widgets.Layout(align_items='center'))

# Display the final layout
display(final_layout)

# Function to update the loading bars based on the dataframe values
def update_loading_bars(b):
      # Make the boxes visible
    left_box.layout.visibility = 'visible'
    right_box_content.layout.visibility = 'visible'
    
    for i, (start_label, progress_bar, end_label, _) in enumerate(loading_bars):
        start_value = df.loc[i, 'Start Value']
        end_value = df.loc[i, 'End Value']
        progress_bar.min = min(start_value, end_value)
        progress_bar.max = max(start_value, end_value)
        progress_bar.value = min(start_value, end_value) * 1.5  # Dummy calculation for the current progress
        start_label.value = f"{start_value:.2f}"
        end_label.value = f"{end_value:.2f}"
    # Show the "Potential Complaint" text

    if bool(re.findall('a',input_box.value.lower())) ==True:
      right_box_content.value = '<div class="right-box-content" style="display: flex;">Potential Complaint</div>'
    else:
      right_box_content.value = '<div class="right-box-content-false" style="display: flex;">Not a Complaint</div>'


# Link the button to the update function
submit_button.on_click(update_loading_bars)
