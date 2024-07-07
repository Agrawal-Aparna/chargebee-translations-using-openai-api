# Translation Script for Chargebee Language Packs

This repository contains a Python script designed to translate text in Chargebee language pack CSV files from English to Norwegian using the OpenAI API.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.6 or later** installed on your system.
2. Required Python packages:
    - `openai`
    - `pandas`

You can install the necessary packages using pip:


pip install openai pandas


3. An OpenAI API key. You can obtain this key from the OpenAI website.

## Setting Up

1. **Set the OpenAI API Key**:
    Ensure the OpenAI API key is set as an environment variable:


    export OPENAI_API_KEY='your-api-key'
 

2. **Provide the Folder Path**:
    Run the script with the folder path containing the Chargebee language pack CSV files as a command-line argument:

    
    python script_name.py /path/to/folder
  

## Script Overview

The script performs the following steps:

1. **Check for the OpenAI API key environment variable**:
    If the API key is not found, the script exits with an error message.

2. **Check for the folder path argument**:
    If the folder path is not provided as a command-line argument, the script exits with an error message.

3. **OpenAI API Configuration**:
    Sets the base URL for the OpenAI API.

4. **Function to Translate Text**:
    The `translate_text` function takes English text and translates it to Norwegian using a context-aware prompt with the OpenAI API.

5. **Traverse the Directory Tree and Process Each CSV File**:
    For each CSV file in the directory tree:
    - Reads the CSV file into a DataFrame.
    - Renames columns to standardize the format.
    - Translates each text entry using the OpenAI API.
    - Saves the translated DataFrame back to the CSV file with UTF-8 BOM encoding.

## Usage

1. **Run the Script**:
    Execute the script by running the following command in your terminal:

   
    python script_name.py /path/to/folder
  

    Replace `/path/to/folder` with the actual path to your folder containing the Chargebee language pack CSV files.

2. **Translation Process**:
    The script will process each CSV file in the specified folder, translating text from English to Norwegian, and save the results back to the CSV files.

## Chargebee Language Packs

This script is specifically designed to handle Chargebee language packs, which contain various text elements used in the Chargebee platform. The language packs are available in CSV format, typically with columns named `reference value`, `description`, and `value`.

## Notes

- The script expects the CSV files to have columns named `reference value`, `description`, and `value`.
- The script will handle empty rows by keeping them empty in the translated text.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Acknowledgements

This project uses the OpenAI API for translations and relies on the pandas library for data manipulation. Special thanks to Chargebee for providing the language packs.
