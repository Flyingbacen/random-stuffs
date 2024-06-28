"""import random
heads, tails, headflip, tailflip, flips = 0, 1, 0, 0, 0

while True:
    flip = random.randint(0, 1)
    if flip == heads:
        headflip += 1
        tailflip = 0
        flips += 1
        if headflip == 24:
            print(f"1 in {2**24} chance of flipping 24 heads in a row " + str(flips))
            break
    elif flip == tails:
        tailflip += 1
        headflip = 0
        flips += 1
        if tailflip == 24:
            print(f"1 in {2**24} chance of flipping 24 tails in a row " + str(flips))
            break

This is the original script I had, then later turned into a graph.
"""

import random
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

heads, tails = 0, 1
flips_to_success = []
averages = []  
iterations = 2000  # Total iterations to run
check_interval = 100 # Calculate average every x iterations
num_bars = 20



def run_simulation():
    flips, headflip, tailflip = 0, 0, 0
    while True:
        flip = random.randint(heads, tails)
        flips += 1
        if flip == heads:
            headflip += 1
            tailflip = 0
            if headflip == 24:
                print(len(flips_to_success)+1)
                return flips
        else:
            tailflip += 1
            headflip = 0
            if tailflip == 24:
                print(len(flips_to_success)+1)
                return flips

for i in range(1, iterations + 1):
    flips_required = run_simulation()
    flips_to_success.append(flips_required)
    if i % check_interval == 0:
        average_flips = sum(flips_to_success[-check_interval:]) / check_interval
        averages.append(average_flips)

x_values = np.arange(1, num_bars + 1)
bar_values = []

data_length = len(averages)
group_size = data_length // num_bars

if group_size == 0:
    group_size = 1

for i in range(0, data_length, group_size):
    group = averages[i:i+group_size]
    avg = sum(group) / len(group)
    bar_values.append(avg)

if data_length % num_bars != 0:
    last_group = averages[-(data_length % num_bars):]
    last_avg = sum(last_group) / len(last_group)
    bar_values[-1] = (bar_values[-1] * len(last_group) + last_avg * (data_length % num_bars)) / (len(last_group) + (data_length % num_bars))

def standard_format(x, pos):
    return f'{x / 1_000_000:.2f} million'

x_values = range(check_interval, iterations + 1, check_interval)
plt.bar(x_values, averages, width=check_interval*0.8)
plt.xlabel('Iteration')
plt.ylabel('Average Flips to Success')
plt.title('Average Number of Flips Required to Get 24 Heads or Tails in a Row')
plt.grid(True, axis='x')
formatter = FuncFormatter(standard_format)
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()