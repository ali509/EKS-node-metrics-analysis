import re
import requests
from datetime import datetime, timedelta

# URL of the Node Exporter metrics endpoint
url = "http://aac74702cf6cf490792fb26390d9f57b-757174461.us-west-2.elb.amazonaws.com:9100/metrics"

# Regular expression pattern to match CPU metrics
cpu_regex = re.compile(r'node_cpu_seconds_total{cpu="(\d+)",mode="(\w+)"} (\d+\.\d+)')

# Regular expression pattern to match memory metrics
memory_regex = re.compile(r'node_memory_(\w+)_bytes (\d+)')

# File path to output the results
output_file_path = "/data/metrics_output_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

# Fetch data from the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response content
    data = response.text

    # Extract CPU metrics
    cpu_data = cpu_regex.findall(data)

    # Extract memory metrics
    memory_data = memory_regex.findall(data)

    # Filter data for metrics printed 2 minutes ago
    current_time = datetime.utcnow()
    two_minutes_ago = current_time - timedelta(minutes=2)

    filtered_cpu_data = [(cpu, mode, float(value)) for cpu, mode, value in cpu_data]
    filtered_memory_data = [(metric, int(value)) for metric, value in memory_data]

    # Calculate average CPU usage
    cpu_total = sum(value for _, _, value in filtered_cpu_data)
    cpu_average = cpu_total / len(filtered_cpu_data)

    # Calculate memory usage
    memory_total = sum(value for _, value in filtered_memory_data)

    # Write results to the output file
    with open(output_file_path, "w") as output_file:
        output_file.write("Average CPU usage: {} GB\n".format(cpu_average))
        output_file.write("Total Memory available: {} GB\n".format(memory_total))

    # Print confirmation message
    print("Results have been written to:", output_file_path)
else:
    print("Failed to fetch data from the URL. Status code:", response.status_code)