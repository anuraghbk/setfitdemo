import gradio as gr
import pandas as pd

# Define fixed start and end values for metrics
fixed_metrics = {
    'Metric 1': {'start': 0, 'end': 100},
    'Metric 2': {'start': 20000, 'end': 100000},
    'Metric 3': {'start': 5, 'end': 60},
    'Metric 4': {'start': 0, 'end': 200},
    'Metric 5': {'start': 20, 'end': 80},
    'Metric 6': {'start': 0, 'end': 10},
    'Metric 7': {'start': 0, 'end': 90},
    'Metric 8': {'start': 15, 'end': 45},
    'Metric 9': {'start': 5, 'end': 100},
    'Metric 10': {'start': 30, 'end': 150}
}

# Sample DataFrame with contactid and current metric values
data = {
    'contactid': [1, 2, 3],
    'Metric 1_current': [25, 50, 75],
    'Metric 2_current': [30000, 40, 35],
    'Metric 3_current': [50, 45, 55],
    'Metric 4_current': [75, 100, 125],
    'Metric 5_current': [40, 60, 55],
    'Metric 6_current': [5, 7, 8],
    'Metric 7_current': [70, 65, 75],
    'Metric 8_current': [35, 40, 30],
    'Metric 9_current': [60, 55, 65],
    'Metric 10_current': [90, 85, 2]
}

df = pd.DataFrame(data)

def fetch_metrics(contactid):
    # Debug statement to check input and DataFrame
    print(f"Fetching metrics for contactid: {contactid}")

    # Filter the DataFrame based on contactid
    contactid = int(contactid)
    metrics = df[df['contactid'] == contactid]
    
    # Debug statement to check filtered DataFrame
    print("Filtered DataFrame:")
    print(metrics)

    if metrics.empty:
        return "No data available for this contactid."

    # Extract current values and use fixed start and end values
    current_values = metrics.drop(columns='contactid').iloc[0]
    metric_data = []
    for metric_name in fixed_metrics.keys():
        start = fixed_metrics[metric_name]['start']
        end = fixed_metrics[metric_name]['end']
        current = current_values[f'{metric_name}_current']
        metric_data.append({'name': metric_name, 'start': start, 'end': end, 'current': current})

    return metric_data

def generate_gauges(metric_data):
    if isinstance(metric_data, str):  # Error message
        return metric_data

    gauges_html = ""
    last_metric_value = None
    for metric in metric_data:
        name = metric['name']
        start = metric['start']
        end = metric['end']
        current = metric['current']
        percent = (current - start) / (end - start) * 100
        
        gauges_html += f"""
        <div style="width: 100%; max-width: 200px; margin: 10px; display: inline-block; text-align: center;">
            <div style="font-size: 14px; margin-bottom: 5px;">{name}: {current}</div>
            <div style="position: relative; width: 100%; height: 30px; background: #e0e0e0;">
                <div style="position: absolute; height: 100%; width: {percent}%; background: #76c7c0;"></div>
            </div>
            <div style="font-size: 12px; margin-top: 5px;">
                Start: {start}, End: {end}
            </div>
        </div>
        """
        last_metric_value = current

    # Determine complaint message
    if last_metric_value and last_metric_value > 50:
        complaint_message = "<div style='margin-top: 20px; padding: 10px; background-color: red; color: white; font-weight: bold; text-align: center;'>**Potential complaint**</div>"
    else:
        complaint_message = "<div style='margin-top: 20px; padding: 10px; background-color: light-green; border: 1px solid #ccc; border-radius: 5px; text-align: center;'>**Not a complaint**</div>"
    
    return f'<div style="display: flex; flex-wrap: wrap;">{gauges_html}</div>{complaint_message}'

def update_gauges(contactid):
    metric_data = fetch_metrics(contactid)
    return generate_gauges(metric_data)

with gr.Blocks() as demo:
    gr.Markdown("# Gauges Example")

    with gr.Row():
        text_input = gr.Textbox(
            label="Enter Contact ID",
            placeholder="e.g. 1",
            elem_id="input-box",
            lines=1
        )

    gauge_output = gr.HTML()

    text_input.submit(fn=update_gauges, inputs=text_input, outputs=gauge_output)

    demo.launch()
