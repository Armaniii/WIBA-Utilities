import pandas as pd
import re
import sys
import tqdm

def preprocess_text(text):
    """Preprocess text by removing unwanted characters and formatting."""
    return text.lower().strip()

def sliding_window_batch(text_list, window_size, step_size):
    """Generate overlapping batches of text segments."""
    for i in range(0, len(text_list) - window_size + 1, step_size):
        yield text_list[i:i + window_size]

def process_file(input_file, output_file, window_size=3, step_size=1):
    """Process a file with a column called speech into overlapping window segments."""
    hearings = pd.read_csv(input_file)
    hearings['id'] = hearings.index
    hearings['processed_text'] = hearings['text'].apply(preprocess_text)

    texts = []
    ids = []

    for index, row in tqdm.tqdm(hearings.iterrows(), total=hearings.shape[0]):
        text = row['processed_text']
        id = row['id']

        sentences = re.split(r'(?<!\bMr)(?<!\bMrs)(?<!\bDr)(?<!\bMs)(?<!\bProf)(?<=\.|\?|\!)\s', text)
        text_list = [sentence.strip() for sentence in sentences]

        for batch in sliding_window_batch(text_list, window_size, step_size):
            segment_text = " ".join(batch)
            texts.append(segment_text)
            ids.append(id)

    df = pd.DataFrame({'id': ids, 'text': texts})
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

def calculate_segments(input_file, output_file, window_size=3):
    """Calculate which segments to keep based on argument and confidence scores."""
    df = pd.read_csv(input_file)
    segments_dict = {id: [] for id in df['id'].unique()}
    # map argument predictions "Argument to 1 AND Non-argument to 0"
    df['agrument_predictions'] = df['argument_predictions'].map({'Argument': 1, 'Non-argument': 0})

    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        id = row['id']
        start_index = index
        end_index = start_index + window_size
        confidence = row['argument_confidence']
        label = row['agrument_predictions']
        text = row['text']

        if label == 1:
            overlap_found = False

            for existing_segment in segments_dict[id]:
                existing_start, existing_end, existing_confidence = existing_segment['range']

                if (start_index < existing_end and end_index > existing_start):
                    overlap_found = True
                    if confidence > existing_confidence:
                        existing_segment['range'] = (start_index, end_index, confidence)
                        existing_segment['text'] = text
                    break

            if not overlap_found:
                segments_dict[id].append({'range': (start_index, end_index, confidence), 'label': label, 'text': text})

    data = []
    for id, segments in segments_dict.items():
        for segment in segments:
            data.append({'id': id, 'start_index': segment['range'][0], 'end_index': segment['range'][1], 'confidence': segment['range'][2], 'label': segment['label'], 'text': segment['text']})

    segments_df = pd.DataFrame(data)
    segments_df.to_csv(output_file, index=False)
    print(f"Selected segments saved to {output_file}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python process_hearings.py <task> <input_file> <output_file> [window_size] [step_size]")
        sys.exit(1)

    task = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    window_size = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    step_size = int(sys.argv[5]) if len(sys.argv) > 5 else 1

    if task == "process":
        process_file(input_file, output_file, window_size, step_size)
    elif task == "select":
        calculate_segments(input_file, output_file, window_size)
    else:
        print("Invalid task. Use 'process' to process file or 'select' to select segments.")
        sys.exit(1)

if __name__ == '__main__':
    main()
