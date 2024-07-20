# Hearing Processing Script

This script is designed to process and analyze textual data from hearing transcripts. It consists of two main functions:
1. **Processing the file into overlapping text segments**.
2. **Selecting relevant text segments based on argument labels and confidence scores**.

## Installation

1. Ensure you have Python installed (version 3.6+).
2. Install the necessary packages using pip:

```bash
pip install pandas tqdm
```


## Usage

### Command Line Interface

You can run the script from the command line with the following syntax:

```bash
python process_hearings.py <task> <input_file> <output_file> [window_size] [step_size]
```


- `<task>`: The task to perform. Use `process` to process the file into overlapping text segments. Use `select` to select relevant text segments based on argument labels and confidence scores.
- `<input_file>`: The path to the input CSV file containing the hearing transcripts.
- `<output_file>`: The path to save the processed output CSV file.
- `[window_size]` (optional): The size of the overlapping window. Default is 3.
- `[step_size]` (optional): The step size for the sliding window. Default is 1.

### Example

1. **Processing a file into overlapping text segments**:

```bash
python process_hearings.py process hearings.csv processed_hearings.csv 3 1
```

2. **Selecting relevant text segments**:
```bash
python process_hearings.py select processed_hearings.csv selected_hearings.csv 3 
```

## Functions

### `preprocess_text(text)`
Preprocesses the text by removing unwanted characters and formatting.

### `sliding_window_batch(text_list, window_size, step_size)`
Generates overlapping batches of text segments.

### `process_file(input_file, output_file, window_size=3, step_size=1)`
Processes a file with a column called `speech` into overlapping window segments.

### `calculate_segments(input_file, output_file, window_size=3)`
Calculates which segments to keep based on argument and confidence scores.

### `main()`
The main function that parses command-line arguments and calls the appropriate function based on the specified task.
