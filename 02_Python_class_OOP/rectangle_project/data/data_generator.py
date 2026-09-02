import json
import random
from pathlib import Path

from loguru import logger

# Randomly select 20 file numbers to be corrupted
corrupted_indices = random.sample(range(1, 201), 20)
logger.info(f"Corrupted files will be: {sorted(corrupted_indices)}")

corruption_types = [
    lambda x: str(x),  # Convert number to string
    lambda x: "abc",   # Non-numeric string
    lambda x: "?$#%",  # Special characters
    lambda x: "",      # Empty string
    lambda x: None,    # Null value
    lambda x: "12.34.56",  # Invalid number format
    lambda x: "infinity",  # Invalid numeric string
    lambda x: "-",     # Just a minus sign
    lambda x: "1.2.3", # Multiple decimal points
    lambda x: "NaN",   # Not a Number string
]

# Generate all 200 files
for i in range(1, 201):
    # Generate random dimensions between 1.0 and 100.0
    length = round(random.uniform(1.0, 100.0), 1)
    width = round(random.uniform(1.0, 100.0), 1)
    
    # Check if this file should be corrupted
    if i in corrupted_indices:
        # Decide which field(s) to corrupt
        corrupt_length = random.choice([True, False])
        corrupt_width = random.choice([True, False])
        
        # Ensure at least one field is corrupted
        if not corrupt_length and not corrupt_width:
            corrupt_length = True
        
        if corrupt_length:
            corruption_func = random.choice(corruption_types)
            length = corruption_func(length)
        
        if corrupt_width:
            corruption_func = random.choice(corruption_types)
            width = corruption_func(width)
    
    data = {
        "length": length,
        "width": width
    }
    
    filename = f"rectangle_{i}.json"
    filepath = Path("02_Python_class_OOP/rectanble_project/data").joinpath(filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

logger.info(f"Generated 200 rectangle files (180 valid, 20 corrupted)")
logger.info("Corrupted files are randomly distributed among rectangle_1.json to rectangle_200.json")

# Print some examples of corrupted files
logger.info("\nExamples of some corrupted files:")
sample_corrupted = random.sample(corrupted_indices, min(5, len(corrupted_indices)))
for i in sample_corrupted:
    filepath = Path("02_Python_class_OOP/rectanble_project/data").joinpath(f'rectangle_{i}.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
    logger.error(f"rectangle_{i}.json: {data}")
