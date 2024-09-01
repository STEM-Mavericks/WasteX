import datetime
import json

def format_timestamp(timestamp):
    """
    Convert a timestamp into a more readable format.
    
    Args:
        timestamp (str): The original timestamp.
    
    Returns:
        str: The formatted timestamp.
    """
    formatted_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return formatted_time.strftime('%b %d, %Y %I:%M %p')

def calculate_average(data):
    """
    Calculate the average value of a list of numbers.
    
    Args:
        data (list of float): The list of numbers.
    
    Returns:
        float: The average value.
    """
    if not data:
        return 0.0
    return sum(data) / len(data)

def process_sensor_data(sensor_data):
    """
    Process raw sensor data for visualization or storage.
    
    Args:
        sensor_data (list of dict): List of sensor data entries, each as a dictionary.
    
    Returns:
        dict: Processed data including formatted timestamps, averages, etc.
    """
    processed_data = []
    total_weight = 0
    
    for entry in sensor_data:
        formatted_entry = {
            'timestamp': format_timestamp(entry['timestamp']),
            'weight': entry['weight'],
            'type': entry['type'],
            'formatted_weight': f"{entry['weight']} kg"
        }
        processed_data.append(formatted_entry)
        total_weight += entry['weight']
    
    average_weight = calculate_average([entry['weight'] for entry in sensor_data])
    
    return {
        'processed_data': processed_data,
        'total_weight': total_weight,
        'average_weight': average_weight
    }

def serialize_data_for_chart(sensor_data):
    """
    Serialize sensor data for use in Chart.js or other front-end libraries.
    
    Args:
        sensor_data (list of dict): List of sensor data entries, each as a dictionary.
    
    Returns:
        str: JSON string of the serialized data.
    """
    timestamps = [entry['timestamp'] for entry in sensor_data]
    weights = [entry['weight'] for entry in sensor_data]
    
    chart_data = {
        'labels': timestamps,
        'datasets': [{
            'label': 'Waste Weight Over Time',
            'data': weights,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    
    return json.dumps(chart_data)
