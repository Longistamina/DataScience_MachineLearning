"""
NOTE: tqdm only supports python<=3.12, but can render in jupyter notebooks

1. Installation and Demo:
- Installing the library: pip install tqdm
- Basic demonstration

2. Basic Usage:
- Simple progress bar: tqdm() wrapper
- Setting descriptions
- Manual progress updates

3. Unknown Mode:
- Progress bar without known total (for loop)
- Progress bar without known total (while loop)
- Unknown mode with dynamic text

4. Manual Mode:
- Direct control with update()
- Setting progress with n parameter

5. Context Manager Usage:
- Using tqdm as context manager
- Manual updates with context manager

6. Auto-detection with tqdm.auto:
- Automatic environment detection
- Notebook vs terminal handling
- Best practices for libraries

7. Customization:
- Changing bar format
- Colors and styling
- Custom bar characters
- Units and scaling

8. Advanced Features:
- Nested progress bars
- Postfix (dynamic text)
- Writing without interference
- Disable/enable conditionally

9. Writing Custom Formats:
- Format parameters
- Custom bar templates

10. Real-world Examples:
- File processing
- Data downloading
- Batch operations

Tips and Best Practices
"""


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 1. Installation and Demo -------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

################
## Installing ##
################

# pip install tqdm

####################
## Quick examples ##
####################

from tqdm import tqdm
import time

# Simplest usage
for i in tqdm(range(100)):
    time.sleep(0.02)

# Output: 100%|██████████| 100/100 [00:01<00:00, 99.00it/s]


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 2. Basic Usage -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

from tqdm import tqdm
import time

#########################
## Simple progress bar ##
#########################

items = range(100)
for item in tqdm(items):  # Wrap iterable with tqdm
    time.sleep(0.02)  # Simulate work

# Output: 100%|██████████| 100/100 [00:01<00:00, 99.00it/s]

###################################
## Progress bar with description ##
###################################

for i in tqdm(range(50), desc='Processing'):
    time.sleep(0.05)

# Output: Processing: 100%|██████████| 50/50 [00:02<00:00, 20.00it/s]

#####################################
## Setting description dynamically ##
#####################################

pbar = tqdm(range(100), desc='Downloading')
for i in pbar:
    pbar.set_description(f'Downloading file {i+1}')
    time.sleep(0.02)

# Output: Downloading file 100: 100%|██████████| 100/100 [00:02<00:00, 50.00it/s]

##############################
## Showing additional stats ##
##############################

for i in tqdm(range(50), desc='Processing', unit='items'):
    time.sleep(0.05)

# Output: Processing: 100%|██████████| 50/50 items [00:02<00:00, 20.00items/s]

########################
## Disabling progress ##
########################

# Useful for production/logging scenarios
for i in tqdm(range(50), disable=True):
    time.sleep(0.05)

# Output: No progress bar shown

########################
## With position/color ##
########################

for i in tqdm(range(50), desc='Task', colour='green'):
    time.sleep(0.05)

# Output: Task: 100%|██████████| 50/50 [00:02<00:00, 20.00it/s] (in green)


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 3. Unknown Mode ----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###########################################
## Progress bar without total (for loop) ##
###########################################
'''Useful when you don't know how many items you'll process'''

items_processed = 0
pbar = tqdm(desc='Processing')  # No total specified - unknown mode
for i in range(50):
    time.sleep(0.05)
    pbar.update(1)  # Just keeps updating, no percentage shown
    items_processed += 1
pbar.close()

# Output: Processing: 50it [00:02, 20.00it/s]

#############################################
## Progress bar without total (while loop) ##
#############################################
'''Continue processing until condition is met'''

pbar = tqdm(desc='Waiting')
count = 0
while count < 50:  # Continue until condition is met
    time.sleep(0.05)
    count += 1
    pbar.update(1)  # Update progress
pbar.close()

# Output: Waiting: 50it [00:02, 20.00it/s]

#######################################
## Unknown mode with context manager ##
#######################################
'''Using with statement for automatic cleanup'''

with tqdm(desc='Streaming') as pbar:
    count = 0
    while count < 75:
        pbar.set_postfix_str(f'chunk {count+1}')
        time.sleep(0.03)
        pbar.update(1)
        count += 1

# Output: Streaming: 75it [00:02, 32.61it/s] chunk 75

####################################
## Unknown mode with dynamic text ##
####################################
'''Show processing details without knowing total'''

pbar = tqdm(desc='Processing Stream')
for i in range(60):
    pbar.set_postfix(items=i+1, status='processing')
    time.sleep(0.04)
    pbar.update(1)
pbar.close()

# Output: Processing Stream: 60it [00:02, 25.00it/s, items=60, status=processing]

#################################
## Unknown mode with generator ##
#################################
'''Process a generator of unknown length'''

def my_generator():
    i = 0
    while i < 50:
        yield i
        i += 1

# Wrap generator - tqdm counts items as they're yielded
for item in tqdm(my_generator(), desc='Generator'):
    time.sleep(0.05)

# Output: Generator: 50it [00:02, 20.00it/s]

#################################
## Unknown to known transition ##
#################################
'''Start without total, then set it when known'''

pbar = tqdm(desc='Scanning')
count = 0
while count < 30:
    time.sleep(0.05)
    pbar.update(1)
    count += 1

# Now we know the total
pbar.total = 100  # Set total mid-way
pbar.refresh()

while count < 100:
    time.sleep(0.05)
    pbar.update(1)
    count += 1
pbar.close()

# Output: Transitions from indefinite to definite progress


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 4. Manual Mode -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###########################
## Manual initialization ##
###########################
'''Create progress bar and update manually'''

pbar = tqdm(total=100)
for i in range(100):
    time.sleep(0.01)
    pbar.update(1)  # Manually update by 1
pbar.close()  # Always close when done

# Output: 100%|██████████| 100/100 [00:01<00:00, 99.00it/s]

##############################
## Custom update increments ##
##############################

pbar = tqdm(total=1000)
for i in range(10):
    time.sleep(0.1)
    pbar.update(100)  # Increment by 100 each time
pbar.close()

# Output: 100%|██████████| 1000/1000 [00:01<00:00, 990.10it/s]

###############################
## Setting position directly ##
###############################

pbar = tqdm(total=100)
for i in range(0, 101, 10):
    pbar.n = i  # Set current position
    pbar.refresh()  # Refresh display
    time.sleep(0.2)
pbar.close()

# Output: 100%|██████████| 100/100 [00:02<00:00, 50.00it/s]

######################
## Reset capability ##
######################

pbar = tqdm(total=50)
for i in range(50):
    pbar.update(1)
    time.sleep(0.02)
pbar.reset()  # Reset to beginning
for i in range(50):
    pbar.update(1)
    time.sleep(0.02)
pbar.close()

# Output: Resets and counts again from 0

#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. Context Manager Usage ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###################################
## Using tqdm as context manager ##
###################################
'''Automatically handles cleanup'''

with tqdm(total=100) as pbar:
    for i in range(100):
        time.sleep(0.01)
        pbar.update(1)

# Output: 100%|██████████| 100/100 [00:01<00:00, 99.00it/s]

###############################
## With description and text ##
###############################

with tqdm(total=100, desc='Processing') as pbar:
    for i in range(100):
        pbar.set_postfix_str(f'file_{i}.txt')
        time.sleep(0.01)
        pbar.update(1)

# Output: Processing: 100%|██████████| 100/100 [00:01<00:00, 99.00it/s] file_99.txt

########################################
## Unknown total with context manager ##
########################################
'''When you don't know the total in advance'''

with tqdm(desc='Streaming') as pbar:
    for i in range(50):
        time.sleep(0.05)
        pbar.update(1)

# Output: Streaming: 50it [00:02, 20.00it/s]

##############################
## Manual mode with context ##
##############################

tasks = ['Init', 'Load', 'Process', 'Save', 'Done']
with tqdm(total=len(tasks), desc='Pipeline') as pbar:
    for task in tasks:
        pbar.set_description(f'Pipeline: {task}')
        time.sleep(1)
        pbar.update(1)

# Output: Pipeline: Done: 100%|██████████| 5/5 [00:05<00:00, 1.00it/s]

#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 6. Customization ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#######################
## Custom bar format ##
#######################

'''Customize the progress bar appearance'''

for i in tqdm(range(50), 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
    time.sleep(0.05)

# Output: 50/50| (simplified format)

##################
## Color themes ##
##################

# Available colors: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'

for i in tqdm(range(50), desc='Red Bar', colour='red'):
    time.sleep(0.05)
# Output: Red Bar: 100%|██████████| 50/50 [00:02<00:00, 20.00it/s] (in red)

for i in tqdm(range(50), desc='Blue Bar', colour='#0000FF'):
    time.sleep(0.05)
# Output: Blue Bar: 100%|██████████| 50/50 [00:02<00:00, 20.00it/s] (in blue)

###########################
## Custom bar characters ##
###########################

for i in tqdm(range(50), ascii=True):  # Use ASCII characters
    time.sleep(0.05)
# Output: 100%|##########| 50/50 [00:02<00:00, 20.00it/s]

for i in tqdm(range(50), ascii='>='):  # Custom ASCII characters
    time.sleep(0.05)
# Output: 100%|>>>>>>>>>>| 50/50 [00:02<00:00, 20.00it/s]

#######################
## Units and scaling ##
#######################
'''Use human-readable units'''

for i in tqdm(range(1000), 
              unit='B',  # Bytes
              unit_scale=True):  # Auto-scale (KB, MB, etc.)
    time.sleep(0.001)
# Output: 100%|██████████| 1.00K/1.00K B [00:01<00:00, 990B/s]

for i in tqdm(range(1000000), 
              unit='',
              unit_scale=True,
              unit_divisor=1000):
    pass
# Output: 100%|██████████| 1.00M/1.00M [00:00<00:00, 999.00K/s]

###################
## Custom length ##
###################

for i in tqdm(range(50), ncols=100):  # 100 character width
    time.sleep(0.05)
# Output: Wider progress bar

for i in tqdm(range(50), ncols=50):  # 50 character width
    time.sleep(0.05)
# Output: Narrower progress bar

####################
## Leave or clear ##
####################

# Leave the progress bar after completion
for i in tqdm(range(50), leave=True):
    time.sleep(0.05)
# Output: Bar remains visible after completion

# Clear the progress bar after completion
for i in tqdm(range(50), leave=False):
    time.sleep(0.05)
# Output: Bar disappears after completion

####################
## Smoothing rate ##
####################

for i in tqdm(range(100), smoothing=0.1):  # More responsive
    time.sleep(0.01)
# Output: Speed adapts quickly to changes

for i in tqdm(range(100), smoothing=0.9):  # More stable
    time.sleep(0.01)
# Output: Speed changes slowly


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 7. Auto-detection with tqdm.auto -------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#####################################
## Automatic environment detection ##
#####################################
'''tqdm.auto automatically chooses the best progress bar for your environment'''

from tqdm.auto import tqdm  # Note: .auto instead of regular import
import time

# This will use tqdm.tqdm in terminal/console
# This will use tqdm.notebook.tqdm in Jupyter notebooks
# This will use tqdm.gui.tqdm in GUI environments

for i in tqdm(range(100)):
    time.sleep(0.01)

# Output (Terminal): 100%|██████████| 100/100 [00:01<00:00, 99.00it/s]
# Output (Notebook): Interactive HTML widget with colored bar

########################
## Why use tqdm.auto? ##
########################
'''
tqdm.auto automatically detects:
- Jupyter Notebook/Lab → uses rich HTML widget
- IPython console → uses text-based progress bar
- Standard terminal → uses text-based progress bar
- Non-TTY environment → uses minimal output or disabled

This is especially useful for:
1. Writing library code that works in any environment
2. Sharing code between notebooks and scripts
3. Avoiding manual environment detection
'''

#######################
## Using with trange ##
#######################

from tqdm.auto import trange  # Auto version of trange

for i in trange(50, desc='Processing'):
    time.sleep(0.05)

# Output: Automatically adapts to environment


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 8. Advanced Features -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##########################
## Nested progress bars ##
##########################
'''Multiple progress bars at once'''

from tqdm import trange

for i in trange(3, desc='Outer', position=0):
    for j in trange(50, desc='Inner', position=1, leave=False):
        time.sleep(0.01)

# Output:
# Outer: 100%|██████████| 3/3 [00:04<00:00, 1.33s/it]
# Inner: 100%|██████████| 50/50 [00:00<00:00, 99.00it/s]

############################
## Postfix (dynamic text) ##
############################
'''Add dynamic metadata to the progress bar'''

pbar = tqdm(range(100))
for i in pbar:
    pbar.set_postfix(loss=0.5/(i+1), accuracy=i/100)
    time.sleep(0.02)
# Output: 100%|██████████| 100/100 [00:02<00:00, 50.00it/s, loss=0.005, accuracy=0.99]

# Dictionary postfix
pbar = tqdm(range(50))
for i in pbar:
    pbar.set_postfix({'batch': i, 'learning_rate': 0.001})
    time.sleep(0.05)
# Output: 100%|██████████| 50/50 [00:02<00:00, 20.00it/s, batch=49, learning_rate=0.001]

##################################
## Writing without interference ##
##################################
'''Print messages without breaking the progress bar'''

for i in tqdm(range(100), desc='Processing'):
    if i % 20 == 0:
        tqdm.write(f'Checkpoint at iteration {i}')
    time.sleep(0.02)

# Output: Messages appear above the progress bar

###########################
## Disable conditionally ##
###########################
'''Control visibility based on environment'''

import sys

# Disable if not in terminal
for i in tqdm(range(50), disable=not sys.stdout.isatty()):
    time.sleep(0.05)

# Disable based on verbosity flag
verbose = False
for i in tqdm(range(50), disable=not verbose):
    time.sleep(0.05)

#####################
## Monitoring rate ##
#####################
'''Track rate of processing'''

for i in tqdm(range(100), miniters=1, mininterval=0):
    time.sleep(0.01)
# Output: Shows every single update (slower but more accurate)

for i in tqdm(range(100), miniters=10, mininterval=1):
    time.sleep(0.01)
# Output: Updates only every 10 iterations or 1 second

###################
## Initial value ##
###################

pbar = tqdm(total=100, initial=50)  # Start at 50%
for i in range(50):
    pbar.update(1)
    time.sleep(0.02)
pbar.close()

# Output: Starts at 50/100 and goes to 100/100


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 9. Writing Custom Formats --------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#########################
## Custom bar template ##
#########################
'''Create completely custom format strings'''

# Available format parameters:
# {l_bar} - left part (desc, percentage, bar)
# {bar} - the bar itself
# {r_bar} - right part (current/total, elapsed, rate)
# {n} - current iteration
# {total} - total iterations
# {percentage} - percentage complete
# {elapsed} - elapsed time
# {remaining} - remaining time (if available)
# {rate} - iteration rate
# {postfix} - postfix dict
# {desc} - description

for i in tqdm(range(50), 
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n}/{total}'):
    time.sleep(0.05)
# Output: Processing: 100%|██████████| 50/50

for i in tqdm(range(50), 
              bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
    time.sleep(0.05)
# Output: Custom two-part bar display

#####################
## Minimal display ##
#####################

for i in tqdm(range(50), 
              bar_format='{n_fmt}/{total_fmt}'):
    time.sleep(0.05)

# Output: 50/50

######################
## Detailed display ##
######################

for i in tqdm(range(50), 
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n}/{total} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'):
    time.sleep(0.05)

# Output: Full detailed information


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 10. Real-world Examples ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#####################
## File processing ##
#####################

import os

def process_files(directory):
    '''Process all files in a directory with progress bar'''
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    for filename in tqdm(files, desc='Processing Files'):
        # Process file here
        time.sleep(0.5)  # Simulate processing

process_files('.')  # Uncomment to run

#########################
## Download simulation ##
#########################

def download_files(urls):
    '''Simulate downloading files with progress tracking'''
    for url in tqdm(urls, desc='Downloading', unit='file'):
        chunk_size = 1024
        total_size = 1024 * 1024  # 1MB per file
        
        with tqdm(total=total_size, desc=f'  {url}', 
                  unit='B', unit_scale=True, 
                  leave=False, position=1) as pbar:
            for _ in range(total_size // chunk_size):
                time.sleep(0.001)
                pbar.update(chunk_size)

urls = ['file.zip', 'images.zip', 'music.zip']
download_files(urls)

######################
## Batch operations ##
######################

def batch_process(items, batch_size=10):
    '''Process items in batches with progress tracking'''
    total_batches = (len(items) + batch_size - 1) // batch_size
    
    for i in tqdm(range(0, len(items), batch_size), 
                  desc='Batch Processing',
                  total=total_batches):
        batch = items[i:i + batch_size]
        # Process batch here
        time.sleep(0.5)  # Simulate batch processing

items = list(range(100))
batch_process(items, batch_size=10)

#########################
## Multi-stage process ##
#########################

def multi_stage_task():
    '''Complex task with multiple stages'''
    stages = {
        'Initialization': 20,
        'Data Loading': 30,
        'Processing': 40,
        'Validation': 25,
        'Saving': 15
    }
    
    for stage_name, work_units in stages.items():
        for i in tqdm(range(work_units), 
                      desc=f'{stage_name}',
                      leave=True):
            time.sleep(0.1)

multi_stage_task()

#############################
## Database query tracking ##
#############################

def query_database(record_ids):
    '''Query database records with progress tracking'''
    results = []
    
    for record_id in tqdm(record_ids, 
                          desc='Querying Database',
                          unit='record',
                          colour='cyan'):
        # Simulate database query
        time.sleep(0.05)
        results.append({'id': record_id, 'data': f'data_{record_id}'})
    
    return results

record_ids = range(1, 101)
data = query_database(record_ids)

########################
## Pandas integration ##
########################

import pandas as pd

# Register tqdm with pandas
tqdm.pandas(desc='Processing Rows')

# Create sample dataframe
df = pd.DataFrame({'value': range(1000)})

# Apply function with progress bar
result = df['value'].progress_apply(lambda x: x ** 2)

# Output: Processing Rows: 100%|██████████| 1000/1000 [00:01<00:00, 990.10it/s]

#######################
## Stream processing ##
#######################

def process_stream(stream_generator):
    '''Process a stream of unknown length'''
    processed = []
    
    for item in tqdm(stream_generator, desc='Processing Stream'):
        # Process item
        time.sleep(0.05)
        processed.append(item * 2)
    
    return processed

def my_generator():
    for i in range(50):
        yield i

result = process_stream(my_generator())

###########################
## Concurrent processing ##
###########################

from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    time.sleep(0.1)
    return item * 2

items = range(50)

# Single-threaded with tqdm
results = [process_item(item) for item in tqdm(items, desc='Sequential')]

# Multi-threaded with tqdm
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(tqdm(executor.map(process_item, items), 
                        total=len(items),
                        desc='Parallel'))

# Output: Shows progress for parallel operations

########################
## Large file reading ##
########################

def read_large_file(filename, total_size):
    '''Read large file with progress bar'''
    with open(filename, 'rb') as f:
        with tqdm(total=total_size, 
                  unit='B', 
                  unit_scale=True,
                  desc=filename) as pbar:
            chunk_size = 8192
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                pbar.update(len(chunk))

# read_large_file('large_file.dat', 1024*1024*100)  # 100MB file


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ Tips and Best Practices ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

'''
1. Use tqdm() directly on iterables for simplest usage
2. Use context manager (with statement) for manual mode to ensure cleanup
3. Always call close() if not using context manager
4. Use tqdm.write() instead of print() to avoid breaking the bar
5. Set disable=True in production/non-interactive environments
6. Use unit and unit_scale for byte/file operations
7. Set leave=False for nested bars to avoid clutter
8. Use colour parameter for visual distinction between multiple bars
9. Adjust miniters and mininterval for performance vs responsiveness
10. Use set_postfix() to show dynamic statistics like loss/accuracy
11. For pandas operations, use tqdm.pandas() for seamless integration
12. Use position parameter for multiple simultaneous progress bars
13. Set ncols to control bar width for different terminal sizes
14. Use smoothing parameter to control rate calculation stability
15. For unknown totals, omit the total parameter and use update() manually
16. For while loops with unknown iterations, create pbar without total and update in loop
17. You can dynamically set pbar.total later if the total becomes known
18. USE tqdm.auto.tqdm FOR LIBRARY CODE - it automatically adapts to any environment
19. tqdm.auto detects Jupyter notebooks and uses rich HTML widgets automatically
20. Import from tqdm.auto for code that needs to work in both scripts and notebooks
'''