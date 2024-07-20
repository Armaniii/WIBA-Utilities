# Hearing Processing Script

The methods used in this script are based on the following paper:
[What Is Being Argued (WIBA)? An Application to Legislative Deliberation in the U.S. Congress](https://arxiv.org/abs/2407.06149v2)




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

## CSV Formatting Requirements

### Input File for Processing (`process` task)

The input CSV file should have the following columns:

- `text`: The column containing the text data to be processed.

### Input File for Selecting Segments (`select` task)

The input CSV file should have the following columns:

- `id`: A unique identifier for each row.
- `text`: The column containing the text data that has been processed into segments.
- `argument_predictions`: Predictions indicating whether each segment is an argument (`Argument`) or not (`Non-argument`).
- `argument_confidence`: Confidence scores for the argument predictions.

## Uploading Processed Hearings to WIBA.dev for WIBA-Detect

After processing your hearings data into overlapping segments using the `process` task, you can upload the `processed_hearings.csv` file to WIBA.dev for argument detection. Follow these steps:

1. Go to [WIBA.dev](https://wiba.dev).
2. Navigate to the "File Upload" section.
3. Select "Upload" button and load the `processed_hearings.csv` file from your local machine.
4. Choose the "WIBA-Detect" mode for argument detection.
5. Once the process is complete, download the results and save them as `selected_segments.csv`.
   
_Note that currently there is no progress bar to indicate the progress of WIBA-Detect, however you can estimate the time to completion by knowing the processing speed is roughly 12 rows/second._

You can then use the `select` task to further process the detected arguments based on confidence scores.



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
