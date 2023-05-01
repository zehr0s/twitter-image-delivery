#! /usr/bin/env python3

import os
import json
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

render = False
try:
    from CustomConfig import *
    file_path = log_file_path
    out_path = management_path
except Exception as e:
    render = True
    file_path = "./Logs/info.log"
    out_path = './Management/scripts'

    # Load JSON data from a file
with open(file_path, "r") as file:
    data = json.load(file)

# Parse the timestamps and extract the number of images and status
daily_images_ok = {}
daily_images_error = {}
timestamps_ok = []
timestamps_error = []

for timestamp, entry in data.items():
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    date_str = dt.strftime("%Y-%m-%d")

    if entry["status"] == "OK":
        daily_images_ok[date_str] = daily_images_ok.get(date_str, 0) + entry["images"]
        timestamps_ok.append(dt)
    elif entry["status"] == "ERROR":
        daily_images_error[date_str] = daily_images_error.get(date_str, 0) + entry["images"]
        timestamps_error.append(dt)

# Convert dictionaries to lists for plotting
dates_ok, images_ok = zip(*sorted(daily_images_ok.items()))
dates_error, images_error = zip(*sorted(daily_images_error.items()))

# Convert date strings to datetime objects
dates_ok = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates_ok]
dates_error = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates_error]

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Set the figure background to transparent
fig.patch.set_facecolor('none')
fig.patch.set_alpha(0)

fg_color = '#5D5E62'
# Set the subplots background to transparent
for ax in axs.flat:
    ax.patch.set_facecolor('none')
    ax.patch.set_alpha(0)

    # Set the colors for the dark theme
    ax.spines['bottom'].set_color(fg_color)
    ax.spines['top'].set_color(fg_color)
    ax.spines['right'].set_color(fg_color)
    ax.spines['left'].set_color(fg_color)
    ax.xaxis.label.set_color(fg_color)
    ax.yaxis.label.set_color(fg_color)
    ax.title.set_color(fg_color)
    ax.tick_params(axis='x', colors=fg_color)
    ax.tick_params(axis='y', colors=fg_color)

# Define pastel colors
pastel_green = '#317e7e'
pastel_orange = '#93394e'
# pastel_green = '#1d3232'
# pastel_orange = '#3c2227'

# fig, axs = plt.subplots(2, 2, figsize=(16, 8))
# fig.tight_layout(pad=6.0)

# Bar of Published images per day (status OK)
axs[0, 0].bar(dates_ok, images_ok, color=pastel_green)
axs[0, 0].set_xlabel("Date")
axs[0, 0].set_ylabel("Number of Images")
axs[0, 0].set_title("Published Images per Day (Status OK)")
axs[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
axs[0, 0].tick_params(axis='x', rotation=45)
# axs[0, 0].grid(axis="y")

# Bar of Published images per day (status ERROR)
axs[0, 1].bar(dates_error, images_error, color=pastel_orange)
axs[0, 1].set_xlabel("Date")
axs[0, 1].set_ylabel("Number of Images")
axs[0, 1].set_title("Sum of errors per Day (Status ERROR)")
axs[0, 1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
axs[0, 1].tick_params(axis='x', rotation=45)
# axs[0, 1].grid(axis="y")

# Posts with status OK by timestamp
axs[1, 0].plot(timestamps_ok, [1]*len(timestamps_ok), c=pastel_green, marker='o')
axs[1, 0].set_xlabel("Timestamp")
axs[1, 0].set_title("Posts with Status OK by Timestamp")
axs[1, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
axs[1, 0].tick_params(axis='x', rotation=45)
axs[1, 0].set_yticks([])
# axs[1, 0].legend()
# axs[1, 0].grid()

# Posts with status ERROR by timestamp
axs[1, 1].plot(timestamps_error, [1]*len(timestamps_error), c=pastel_orange, marker='o')
axs[1, 1].set_xlabel("Timestamp")
axs[1, 1].set_title("Posts with Status ERROR by Timestamp")
axs[1, 1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
axs[1, 1].tick_params(axis='x', rotation=45)
axs[1, 1].set_yticks([])
# axs[1, 1].legend()
# axs[1, 1].grid()

plt.tight_layout()
plt.savefig(os.path.join(out_path, 'plt.png'), bbox_inches='tight', transparent=True)

if render:
    plt.show()
