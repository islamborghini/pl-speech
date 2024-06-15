# pl-speech
 
# Real-Time Speech Translation

This project includes two applications for real-time speech translation:
1. **Polish to English**: Translates Polish speech to English text.
2. **English to Polish**: Translates English speech to Polish text.

## Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/islamborghini/pl-speech.git
    cd your-repository
    ```

2. **Create and activate a virtual environment** (optional but recommended):

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Install the correct version of PyTorch**:

    For CPU-only:

    ```sh
    pip install torch
    ```

    For CUDA support (adjust version as needed):

    ```sh
    pip install torch --extra-index-url https://download.pytorch.org/whl/cu116
    ```

## Running the Applications

### Polish to English

1. **Run the application**:

    ```sh
    python polish_to_english.py
    ```

### English to Polish

1. **Run the application**:

    ```sh
    python english_to_polish.py
    ```

## Notes

- Ensure that your environment is correctly set up and that you have an active internet connection for the translation services to work.
- The applications will automatically remove text that has been displayed for more than 30 seconds to manage memory usage.


## Acknowledgements

- [Whisper](https://github.com/openai/whisper) for speech recognition.
- [Google Translator](https://pypi.org/project/deep-translator/) for translation.
- [PyQt5](https://pypi.org/project/PyQt5/) for the graphical user interface.
