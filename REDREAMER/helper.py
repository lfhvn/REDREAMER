import json
import os


ALLOWED_DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def _safe_path(filename):
    """Validate that a file path stays within the allowed data directory."""
    resolved = os.path.realpath(os.path.join(ALLOWED_DATA_DIR, filename))
    if not resolved.startswith(ALLOWED_DATA_DIR):
        raise ValueError(f"Path traversal detected: {filename}")
    return resolved


def load_data(path):
    """
    Load Dataset from File
    """
    input_file = _safe_path(path)
    with open(input_file, "r") as f:
        data = f.read()

    return data


def preprocess_and_save_data(dataset_path, token_lookup, create_lookup_tables):
    """
    Preprocess Text Data
    """
    text = load_data(dataset_path)

    # Ignore notice, since we don't use it for analysing the data
    text = text[81:]

    token_dict = token_lookup()
    for key, token in token_dict.items():
        text = text.replace(key, ' {} '.format(token))

    text = text.lower()
    text = text.split()

    vocab_to_int, int_to_vocab = create_lookup_tables(text)
    int_text = [vocab_to_int[word] for word in text]

    output_path = _safe_path('preprocess.json')
    with open(output_path, 'w') as f:
        json.dump({
            'int_text': int_text,
            'vocab_to_int': vocab_to_int,
            'int_to_vocab': {str(k): v for k, v in int_to_vocab.items()},
            'token_dict': token_dict
        }, f)


def load_preprocess():
    """
    Load the Preprocessed Training data and return them in batches of <batch_size> or less
    """
    input_path = _safe_path('preprocess.json')
    with open(input_path, 'r') as f:
        data = json.load(f)

    int_to_vocab = {int(k): v for k, v in data['int_to_vocab'].items()}
    return data['int_text'], data['vocab_to_int'], int_to_vocab, data['token_dict']


def save_params(params):
    """
    Save parameters to file
    """
    output_path = _safe_path('params.json')
    with open(output_path, 'w') as f:
        json.dump(params, f)


def load_params():
    """
    Load parameters from file
    """
    input_path = _safe_path('params.json')
    with open(input_path, 'r') as f:
        return json.load(f)
