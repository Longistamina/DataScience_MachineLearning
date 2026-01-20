"""
NOTE: alive_progress cannot render in jupyter notebooks, but supports python>=3.12 (including 3.13 and 3.14)

1. Installation and Demo:
- Installing the library: pip install alive-progress
- Showing all available styles: showtime()

2. Basic Usage:
- Simple progress bar: alive_bar() context manager
- Manual progress updates: bar()
- Setting titles and text

3. Unknown Mode:
- Progress bar without known total (for loop)
- Progress bar without know total (while loop)
- Unknown mode with title/text

4. Manual Mode:
- Setting progress manually: bar(value)
- Fractional progress: bar(0.5), bar(0.75)

5. Auto-iterating with alive_it:
- Quick iterator adapter: alive_it(items)
- Full adapter mode with customization
- Auto-inferred totals

6. Customization:
- Changing spinner styles: spinner parameter
- Changing bar styles: bar parameter
- Themes: theme parameter
- Custom text and titles

7. Configuration:
- Global configuration: config_handler
- Setting length, spinner, bar, theme globally

8. Advanced Features:
- Calibration and manual control
- Pause and resume
- Stats and throughput display (print without interfering with bar)
- Nested progress bars

9. Real-world Examples:
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

# pip install alive-progress

################################
## Show all available styles ##
################################

from alive_progress.styles import showtime

showtime() # This displays an interactive showcase of all available styles

#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 2. Basic Usage -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

from alive_progress import alive_bar
import time

#########################
## Simple progress bar ##
#########################

items = range(100)

with alive_bar(len(items)) as bar: # Create progress bar for 100 items
    for item in items:
        time.sleep(0.01) # Simulate work
        bar() # Update progress by 1

# Output: |████████████████████████████| 100/100 [100%] in 1.0s (100.00/s)

#############################
## Progress bar with title ##
#############################

with alive_bar(50, title='Processing') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar() # Call bar() to increment by 1

# Output: Processing |██████████████| 50/50 [100%] in 2.5s (20.00/s)

#####################################
## Setting text during processing ##
#####################################

with alive_bar(100, title='Downloading') as bar:
    for i in range(100):
        bar.text(f'-> file {i+1}') # Update the text being displayed
        time.sleep(0.02)
        bar()

# Output: Downloading |████████| 100/100 [100%] in 2.0s -> file 100

##############################
## Custom update increments ##
##############################

with alive_bar(1000) as bar:
    for i in range(10):
        time.sleep(0.1)
        bar(100) # Increment by 100 each time

# Output: |████████████████████████████| 1000/1000 [100%] in 1.0s

#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 3. Unknown Mode ----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###########################################
## Progress bar without total (for loop) ##
###########################################

'''Useful when you don't know how many items you'll process'''

with alive_bar() as bar: # No total specified - unknown mode
    for i in range(50):
        time.sleep(0.05)
        bar() # Just keeps updating, no percentage shown

# Output: |⠋| 50 in 2.5s (20.00/s)

#############################################
## Progress bar without total (while loop) ##
#############################################

with alive_bar() as bar:
    count = 0
    while count < 50: # Continue until condition is met
        time.sleep(0.05)
        count += 1
        bar() # Update progress

# Output: |⠙| 50 in 2.5s (20.00/s)

##################################
## Unknown mode with title/text ##
##################################

with alive_bar(title='Streaming') as bar:
    for i in range(75):
        bar.text(f'-> processing chunk {i+1}')
        time.sleep(0.03)
        bar()

# Output: Streaming |⠙| 75 in 2.3s (32.61/s) -> processing chunk 75

#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 4. Manual Mode -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###############################
## Setting progress manually ##
###############################
'''Instead of incremental updates, set exact progress value'''

with alive_bar(100, manual=True) as bar:
    for i in range(101):
        bar(i/100) # Set progress as fraction (0.0 to 1.0)
        time.sleep(0.02)

# Output: |████████████████████████████| 100.0% [100%] in 2.0s

############################
## Manual mode with steps ##
############################

tasks = ['Init', 'Load', 'Process', 'Save', 'Done']

with alive_bar(len(tasks), manual=True) as bar:
    for i, task in enumerate(tasks):
        bar.text(f'-> {task}')
        time.sleep(1)
        bar((i+1)/len(tasks)) # Set fractional progress

# Output: |█████████████████| 100.0% [100%] in 5.0s -> Done

#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 5. Auto-iterating with alive_it --------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

from alive_progress import alive_it

############################
## Quick iterator adapter ##
############################
'''The simplest way to use alive-progress - just wrap your iterable!'''

items = range(100)

for item in alive_it(items): # <<-- wrapped items
    # process each item
    time.sleep(0.02)

# Output: |████████████████████████████| 100/100 [100%] in 2.0s (50.00/s)

########################################
## alive_it with title and parameters ##
########################################

numbers = range(50)

for num in alive_it(numbers, title='Computing'):
    result = num ** 2 # Process each number
    time.sleep(0.05)

# Output: Computing |████████████████| 50/50 [100%] in 2.5s (20.00/s)

#######################
## Full adapter mode ##
#######################
'''Assign alive_it to a variable to access bar methods'''

items = ['apple', 'banana', 'cherry', 'date', 'elderberry']

bar = alive_it(items, title='Processing Fruits') # <<-- bar with wrapped items

for item in bar: # <<-- iterate on bar
    bar.text(f'-> {item}') # Access bar methods!
    time.sleep(0.5)

# Output: Processing Fruits |████| 5/5 [100%] in 2.5s -> elderberry

##########################
## Auto-inferred totals ##
##########################
'''alive_it automatically infers total from iterables that support len()'''

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # 10 items
my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5} # 5 keys
my_tuple = (10, 20, 30, 40, 50) # 5 items

# Works with lists
for item in alive_it(my_list, title='List'):
    time.sleep(0.1)
# Output: List |████████████████████████████| 10/10 [100%] in 1.0s

# Works with dictionaries
for key in alive_it(my_dict, title='Dict'):
    time.sleep(0.1)
# Output: Dict |████████████████████████████| 5/5 [100%] in 0.5s

# Works with tuples
for item in alive_it(my_tuple, title='Tuple'):
    time.sleep(0.1)
# Output: Tuple |████████████████████████████| 5/5 [100%] in 0.5s

#############################################
## alive_it with generator (unknown total) ##
#############################################
'''For generators, alive_it operates in unknown mode'''

def my_generator():
    for i in range(50):
        yield i

for item in alive_it(my_generator(), title='Generator'):
    time.sleep(0.05)

# Output: Generator |⠋| 50 in 2.5s (20.00/s)

##################################
## alive_it with explicit total ##
##################################
'''Provide total explicitly for generators to get progress percentage'''

def my_generator():
    for i in range(50):
        yield i

for item in alive_it(my_generator(), total=50, title='Generator'):
    time.sleep(0.05)

# Output: Generator |████████████████████████████| 50/50 [100%] in 2.5s

#################################
## alive_it with customization ##
#################################
'''All alive_bar parameters work with alive_it (except manual mode)'''

data = range(75)

bar = alive_it(data, 
               title='Custom Style',
               spinner='dots_waves',
               bar='bubbles',
               theme='smooth')

for item in bar:
    bar.text(f'Processing item {item}')
    time.sleep(0.03)

# Output: Custom Style ⡿ |○○○○○●●●●●| 75/75 [100%] in 2.3s


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 6. Customization ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

######################
## Changing spinner ##
######################

'''Try different spinner styles'''

with alive_bar(50, spinner='dots') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: ⣾ |████████████████████████████| 50/50 [100%] in 2.5s

with alive_bar(50, spinner='classic') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: / |████████████████████████████| 50/50 [100%] in 2.5s

with alive_bar(50, spinner='waves') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: ≋ |████████████████████████████| 50/50 [100%] in 2.5s

########################
## Changing bar style ##
########################
'''Try different bar styles'''

with alive_bar(50, bar='smooth') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓| 50/50 [100%] in 2.5s

with alive_bar(50, bar='classic') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: |==============>| 50/50 [100%] in 2.5s

with alive_bar(50, bar='blocks') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: |▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉| 50/50 [100%] in 2.5s

##################
## Using themes ##
##################
'''Themes combine spinner and bar styles'''

with alive_bar(50, theme='smooth') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: Uses smooth spinner and smooth bar

with alive_bar(50, theme='classic') as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: Uses classic spinner and classic bar

#############################
## Multiple customizations ##
#############################

with alive_bar(100, 
               title='Custom Task',
               spinner='dots_waves',
               bar='bubbles',
               length=20) as bar:
    for i in range(100):
        time.sleep(0.01)
        bar()

# Output: Custom Task ⡿ |○○○○○○○○●●●●●●●●●●●●| 100/100 [100%] in 1.0s


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 7. Configuration ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

from alive_progress import config_handler

##########################
## Global configuration ##
##########################

'''Set default values for all progress bars'''

config_handler.set_global(
    length=40,           # Bar length in characters
    spinner='dots',      # Default spinner
    bar='smooth',        # Default bar style
    theme='smooth'       # Default theme
)

# Now all progress bars will use these settings (no need to specify each time)
with alive_bar(50) as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: Uses the globally configured style

###############################
## Reset to default settings ##
###############################

config_handler.reset()  # Reset all settings to library defaults

####################################
## Per-use configuration override ##
####################################
'''Global settings are overridden by per-use parameters'''

config_handler.set_global(spinner='classic')

with alive_bar(50, spinner='dots') as bar: # This overrides global setting
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: Uses 'dots' spinner, not 'classic'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 8. Advanced Features -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

######################
## Calibration mode ##
######################
'''Control the spinner speed manually'''

with alive_bar(100, calibrate=True) as bar:
    for i in range(100):
        time.sleep(0.01)
        bar()

# Output: Shows calibration metrics for spinner speed

####################
## Dual line mode ##
####################
'''Show stats on separate line'''

with alive_bar(100, dual_line=True, title='Processing') as bar:
    for i in range(100):
        bar.text(f'Item {i+1}')
        time.sleep(0.02)
        bar()

# Output: 
# Processing |████████████████████████████| 100/100 [100%] in 2.0s
# Item 100

######################################################
## Enrich mode (print without interfering with bar) ##
######################################################
'''Show additional statistics'''

with alive_bar(100, enrich_print=False) as bar:
    for i in range(100):
        if i % 20 == 0:
            print(f'Checkpoint {i}') # Print without interfering with bar
        time.sleep(0.02)
        bar()

# Output: Checkpoint messages appear above the progress bar

#########################
## Force terminal mode ##
#########################
'''Force terminal rendering even in non-TTY environments'''

with alive_bar(50, force_tty=True) as bar:
    for i in range(50):
        time.sleep(0.05)
        bar()

# Output: Progress bar renders even in logs/non-interactive shells


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 9. Real-world Examples ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#####################
## File processing ##
#####################

import os

def process_files(directory):
    '''Process all files in a directory with progress bar'''
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    with alive_bar(len(files), title='Processing Files') as bar:
        for filename in files:
            bar.text(f'-> {filename}')
            # Process file here
            time.sleep(0.5) # Simulate processing
            bar()

process_files('.') # Uncomment to run

#########################
## Download simulation ##
#########################

def download_files(urls):
    '''Simulate downloading files with progress tracking'''
    total_size = len(urls) * 1024 * 1024 # Simulate 1MB per file
    
    with alive_bar(total_size, title='Downloading', dual_line=True) as bar:
        downloaded = 0
        for url in urls:
            chunk_size = 1024
            for _ in range(1024): # Simulate 1024 chunks of 1KB
                bar.text(f'-> {url}')
                time.sleep(0.001)
                downloaded += chunk_size
                bar(chunk_size)

urls = ['file.zip', 'images.zip', 'musics.zip']
download_files(urls)

######################
## Batch operations ##
######################

def batch_process(items, batch_size=10):
    '''Process items in batches with progress tracking'''
    total_batches = (len(items) + batch_size - 1) // batch_size
    
    with alive_bar(total_batches, title='Batch Processing') as bar:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            bar.text(f'-> Processing batch {i//batch_size + 1}/{total_batches}')
            # Process batch here
            time.sleep(0.5) # Simulate batch processing
            bar()

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
    
    total_work = sum(stages.values())
    
    with alive_bar(total_work, title='Multi-Stage Task', dual_line=True) as bar:
        for stage_name, work_units in stages.items():
            bar.text(f'==> {stage_name}')
            for i in range(work_units):
                time.sleep(0.1)
                bar()

multi_stage_task()

#############################
## Database query tracking ##
#############################

def query_database(record_ids):
    '''Query database records with progress tracking'''
    with alive_bar(len(record_ids), 
                   title='Querying Database',
                   spinner='dots_waves',
                   bar='smooth') as bar:
        results = []
        for record_id in record_ids:
            bar.text(f'-> Record ID: {record_id}')
            # Simulate database query
            time.sleep(0.05)
            results.append({'id': record_id, 'data': f'data_{record_id}'})
            bar()
        return results

record_ids = range(1, 101)
data = query_database(record_ids)

###########################
## Unknown length stream ##
###########################

def process_stream(stream_generator):
    '''Process a stream of unknown length'''
    with alive_bar(title='Processing Stream') as bar:
        count = 0
        for _ in stream_generator:
            bar.text(f'-> Processed {count+1} items')
            # Process item
            time.sleep(0.05)
            bar()
            count += 1
        return count

def my_generator():
    for i in range(50):
        yield i

total = process_stream(my_generator())
print(f'Total items processed: {total}')


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ Tips and Best Practices ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

'''
1. Always use context manager (with statement) for automatic cleanup
2. Call bar() exactly once per item processed
3. Use alive_it() for simple iterations where you just need basic tracking
4. Use alive_bar() when you need more control (text updates, manual positioning)
5. For unknown totals, omit the total parameter - bar will show indefinite progress
6. Use bar.text() to provide meaningful status updates
7. Remember bar() returns the current count if you need it
8. Use skipped=True for items you're not processing
9. Explore styles with showtime() to find your preferred look
10. Set global config once at the start of your script for consistent styling
'''