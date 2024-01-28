import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json

try:
    from CustomConfig import *
    file_path = os.path.join(log_file_path, 'info.log')
    out_path = management_path
except Exception as e:
    render = True
    file_path = "./Logs/info.log"
    out_path = './Management/scripts'

# Load the log data
with open(file_path) as f:
    data = [json.loads(line) for line in f]

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Reshape the data
reshaped_data = []

for entry in data:
    for key, value in entry.items():
        value['timestamp'] = key
        reshaped_data.append(value)


# Convert the reshaped data to a DataFrame
df = pd.DataFrame(reshaped_data)

# Convert the timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date


# Group by date and status, and sum the number of images
grouped_df = df.groupby(['date', 'status'])['images'].sum().unstack()

# Split the DataFrame into two: one with status 'OK' and one with status 'ERROR'
df_ok = df[df['status'] == 'OK']
df_error = df[df['status'] == 'ERROR']

# Group the data by date and sum the number of images
grouped_ok = df_ok.groupby('date')['images'].sum()
grouped_error = df_error.groupby('date')['images'].sum()
grouped_df = df.groupby(['date', 'status'])['images'].sum().unstack()

# Count the number of 'OK' and 'ERROR' statuses
status_counts = df['status'].value_counts()

# Set a pastel color scheme
pastel_colors = ["#a8e6cf","#dcedc1","#ffd3b6","#ffaaa5","#ff8b94"]

# Create the bar charts with labels
fig, axs = plt.subplots(2, 2, figsize=(18, 12), facecolor='#2b2b2b')

# 'OK' status chart
grouped_ok.plot(kind='bar', ax=axs[0, 0], color=pastel_colors[0], edgecolor='black')
axs[0, 0].set_facecolor('#2b2b2b')
axs[0, 0].set_title('Number of Images Processed by Day (Status: OK)', fontsize=16, color='white')
axs[0, 0].set_xlabel('Date', fontsize=14, color='white')
axs[0, 0].set_ylabel('Number of Images', fontsize=14, color='white')
axs[0, 0].tick_params(colors='white')

# Add labels to 'OK' status chart
for i, v in enumerate(grouped_ok):
    axs[0, 0].text(i, v + 1, int(v), ha='center', va='bottom', fontsize=12, color='white')

try:
    # 'ERROR' status chart
    grouped_error.plot(kind='bar', ax=axs[0, 1], color=pastel_colors[3], edgecolor='black')
    axs[0, 1].set_facecolor('#2b2b2b')
    axs[0, 1].set_title('Number of Images Processed by Day (Status: ERROR)', fontsize=16, color='white')
    axs[0, 1].set_xlabel('Date', fontsize=14, color='white')
    axs[0, 1].set_ylabel('Number of Images', fontsize=14, color='white')
    axs[0, 1].tick_params(colors='white')

    # Add labels to 'ERROR' status chart
    for i, v in enumerate(grouped_error):
        axs[0, 1].text(i, v + 1, int(v), ha='center', va='bottom', fontsize=12, color='white')
except:
    pass
# Combined chart
grouped_df.plot(kind='bar', stacked=True, ax=axs[1, 0], color=pastel_colors[:2], edgecolor='black')
axs[1, 0].set_facecolor('#2b2b2b')
axs[1, 0].set_title('Number of Images Processed by Day (Combined)', fontsize=16, color='white')
axs[1, 0].set_xlabel('Date', fontsize=14, color='white')
axs[1, 0].set_ylabel('Number of Images', fontsize=14, color='white')
axs[1, 0].tick_params(colors='white')

# Add labels to combined chart
for i, v in enumerate(grouped_df.sum(axis=1)):
    axs[1, 0].text(i, v + 1, int(v), ha='center', va='bottom', fontsize=12, color='white')

# Pie chart
import matplotlib
matplotlib.rcParams['text.color'] = 'w'
pie = axs[1, 1].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=pastel_colors[:2])
axs[1, 1].set_facecolor('#2b2b2b')
axs[1, 1].set_title('Status Distribution', fontsize=16, color='white')

#axs[1, 1].pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=pastel_colors[:2])
#axs[1, 1].set_facecolor('#2b2b2b')
#axs[1, 1].set_title('Status Distribution', fontsize=16, color='white')

plt.tight_layout()

# Save the figure as a .png image
plt.savefig(os.path.join(out_path, 'plt.png'))

# Show the figure
# plt.show()
