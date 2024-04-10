#!/usr/bin/python


import random
import pandas as pd
import json
import os
import shutil

### Visitors Mappings

# List of locations in the museum
locations = ["entrance", "hall1", "hall2", "hall3", "shop", "rest", "edge", "metaverse"]

periods = [90, 90, 90]

Weekday = "Sunday"
Week = "02"

day = Weekday + "_" + Week


# Define time periods and corresponding visitor limits
time_periods = {
    "8am to 11am": 25,
    "11am to 3pm": 55,
    "3pm to 7pm": 40
}


random.seed(42)

# Initialize an empty list to store results
results = []

# Function to simulate visitors distribution for a given time period
def simulate_visitors(time_period, visitor_limit):
    # Randomly distribute visitors across locations
    visitors_distribution = {}
    total_visitors = 0
    for location in locations:
        if location == "metaverse":
            # For metaverse, randomly allocate remaining visitors
            remaining_visitors = visitor_limit - total_visitors
            visitors_distribution[location] = random.randint(0, remaining_visitors)
        else:
            visitors_distribution[location] = random.randint(0, min(10, visitor_limit - total_visitors))
        total_visitors += visitors_distribution[location]

    # Append results for the current time period
    for location, visitors in visitors_distribution.items():
        results.append({"Time Period": time_period, "Location": location, "Visitors": visitors})

# Main simulation loop
for time_period, visitor_limit in time_periods.items():
    simulate_visitors(time_period, visitor_limit)

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Print the DataFrame
# print(df)

# # Update JSON files for each location
# locations = ["edge", "hall1"]

# for location in locations:
#     # Load the JSON file
#     json_path = f"./{location}/componentsConfig.json"
#     with open(json_path, 'r') as f:
#         data = json.load(f)

#     # Update the visitors data
#     data["visitors"]["periods"] = df[df["Location"] == location]["Visitors"].tolist()
#     data["visitors"]["nbpeople"] = df[df["Location"] == location]["Visitors"].tolist()

#     # Write the updated JSON back to the file
#     with open(json_path, 'w') as f:
#         json.dump(data, f, indent=4)

# print("JSON files updated successfully.")

# Update JSON files for each location
# locations = ["edge", "hall1"]
# periods = [5, 7, 4]


# Create folders
create_folder = ["entrance", "hall1", "hall2", "hall3", "shop", "rest", "edge", "metaverse"]
cwd = os.getcwd()

# for folder in create_folder:
#     if not os.path.exists(cwd + "/results/" + folder):
#         os.makedirs(cwd + "/results/" + folder)



for location in locations:
    # Load the JSON file
    json_path = f"{cwd}/deployments/{location}/componentsConfig.json"
    
    with open(json_path, 'r') as f:
        file_content = f.read()
        # print("Content of", json_path)
        # print(file_content)

    try:
        data = json.loads(file_content)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        continue

    # Update the visitors data
    # data["visitors"]["periods"] = df[df["Location"] == location]["Visitors"].tolist()
    data["visitors"]["nbpeople"] = df[df["Location"] == location]["Visitors"].tolist()
    data["visitors"]["periods"] = periods

    # Write the updated JSON back to the file
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"componentsConfig for {location} updated successfully.")

print("ComponentsConfig JSON files updated successfully.")

random.seed(42)

#### Device Update

# List of locations in the museum
# locations = ["entrance", "hall1", "hall2", "hall3", "shop", "rest", "edge", "metaverse"]
# locations = ["edge", "hall1"]

# Function to generate random values for the devices, virtualsensors, and applications
def generate_random_values():
    return random.randint(1, 2)

# Iterate over each location
for location in locations:
    # Load the JSON template
    # json_template_path = f"./{location}/deployment.json"
    json_template_path = f"{cwd}/deployments/{location}/deployment.json"
    with open(json_template_path, 'r') as template_file:
        data = json.load(template_file)

    # Replace {location} with the actual location
    data["location"] = location

    # Assign random numbers to devices
    data["devices"] = {key: generate_random_values() for key in data["devices"]}

    # Assign random numbers to virtualsensors
    data["virtualsensors"] = {key: generate_random_values() for key in data["virtualsensors"]}

    # Assign random numbers to applications
    data["applications"] = {key: generate_random_values() for key in data["applications"]}

    # Write the updated JSON back to the file
    updated_json_path = f"{cwd}/deployments/{location}/deployment.json"
    with open(updated_json_path, 'w') as updated_file:
        json.dump(data, updated_file, indent=4)

    print(f"deployment for {location} updated successfully.")

print("Deployment JSON files updated successfully.")

# Initialize lists to store sums for each location
locations_sum = []
devices_sum = []
virtualsensors_sum = []
applications_sum = []

# Iterate over each location
for location in locations:
    # Load the updated JSON file
    updated_json_path = f"{cwd}/deployments/{location}/deployment.json"
    with open(updated_json_path, 'r') as updated_file:
        data = json.load(updated_file)

    # Calculate sum of values for devices, virtualsensors, and applications
    devices_sum.append(sum(data["devices"].values()))
    virtualsensors_sum.append(sum(data["virtualsensors"].values()))
    applications_sum.append(sum(data["applications"].values()))
    locations_sum.append(location)

# Create a DataFrame to show the sums
df_sums = pd.DataFrame({
    "Location": locations_sum,
    "Devices Sum": devices_sum,
    "Virtualsensors Sum": virtualsensors_sum,
    "Applications Sum": applications_sum
})

# Print the DataFrame
# print(df_sums)





# Define the directory path


cwd = os.getcwd()
date_dir = os.path.join(cwd, "date")

# Check if the date directory exists and remove it if it does
if os.path.exists(date_dir):
    shutil.rmtree(date_dir)
    print(f"Directory '{date_dir}' removed successfully.")
else:
    print(f"Directory '{date_dir}' does not exist.")

# Create the date directory
if not os.path.exists(date_dir):
    os.makedirs(date_dir)
    print(f"Directory '{date_dir}' created successfully.")

# Create the day directory inside the date directory
day_dir = os.path.join(date_dir, day)
if not os.path.exists(day_dir):
    os.makedirs(day_dir)
    print(f"Directory '{day_dir}' created successfully.")

# Define the CSV file paths
device_csv_path = os.path.join(day_dir, "devices.csv")
visitor_csv_path = os.path.join(day_dir, "visitor_maps.csv")

# Save the DataFrame as CSV
df_sums.to_csv(device_csv_path, index=False)
df.to_csv(visitor_csv_path, index=False)

print(f"CSV file saved successfully at: {device_csv_path}")
print(f"CSV file saved successfully at: {visitor_csv_path}")



