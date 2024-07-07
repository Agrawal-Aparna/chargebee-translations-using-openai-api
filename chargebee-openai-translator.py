import openai
import pandas as pd
import os
import sys

# Check for the OpenAI API key environment variable
try:
    os.environ["OPENAI_API_KEY"]
except KeyError:
    print('Please set the environment variable OPENAI_API_KEY')
    sys.exit(1)

# Check for the folder path argument
try:
    main_folder_path = sys.argv[1]
    print(f"Main folder path provided: {main_folder_path}")
except IndexError:
    print("Please provide the main folder path as a command-line argument.")
    sys.exit(1)

# OpenAI API configuration
openai.api_base = "https://api.openai.com/v1/"

# Function to translate text using OpenAI with RAG approach
def translate_text(text, desc, translations, target_language='Norwegian'):
    text = str(text) if pd.notnull(text) else ""
    desc = str(desc) if pd.notnull(desc) else ""

    # Check if the text is just a placeholder
    if text in ["{0}", "{1}", "{2}"]:
        return text

    prompt = (
        f"Please translate the following English text to Norwegian:\n\n"
        f"Text: {text}\n\n"
        f"Here are the translations in other languages which might help:\n"
        f"German: {translations.get('de', '')}\n"
        f"Spanish: {translations.get('es', '')}\n"
        f"Portuguese: {translations.get('pt', '')}\n"
        f"French: {translations.get('fr', '')}\n"
        f"Italian: {translations.get('it', '')}\n\n"
        f"Ignore the placeholders in the text like {{0}}, {{1}}, {{2}} etc. when translating.\n\n"
        f"Provide only the translated text in Norwegian."
    )

    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0
    )
    return completion.choices[0].message.content.strip()


# Load language packs from subfolders
def load_language_packs(main_folder_path):
    language_packs = {}
    for folder_name in os.listdir(main_folder_path):
        folder_path = os.path.join(main_folder_path, folder_name)
        if os.path.isdir(folder_path):
            locale = folder_name.lower()  # Assuming folder name is the locale
            print(f"locale path provided: {locale}")
            language_packs[locale] = load_language_pack(folder_path)
    return language_packs

# Load language pack from a specific folder
def load_language_pack(folder_path):
    print(f" inside load_language_pack: {folder_path}")
    df = pd.DataFrame()
    
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")
                if file_name.endswith('.csv'):
                    print(f"file_name csv: {file_name}")
                    ##file_path = os.path.join(folder_path, file_name)
                    print(f"file_path provided: {file_path}")
                    df_temp = pd.read_csv(file_path, encoding='cp1252')
                    df = pd.concat([df, df_temp], ignore_index=True)
    df = df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'))
    return df

# Convert language packs to dictionary for quick lookup
language_packs = load_language_packs(main_folder_path)

# Traverse the directory tree and process each CSV file
main_folder_path_no = main_folder_path + "/no/";
print(f"main_folder_path_no provided: {main_folder_path_no}")
for root, dirs, files in os.walk(main_folder_path_no):
    for file in files:
        print(f"for file in files:: {file}")
        if file.endswith('.csv'):
            print(f"file.endswith('.csv')s:: {file}")
            file_path = os.path.join(root, file)
            # Read the CSV file
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # Rename columns to remove spaces
            df.rename(columns={'reference value': 'reference_value', 'description': 'description', 'value': 'value'}, inplace=True)
            
            # Identify the language based on the folder name
            language_folder = os.path.basename(root).lower()
            
            # Translate each text
            for index, row in df.iterrows():
                reference_value = row['key']
                #print(f"reference_value : {reference_value}")
                if pd.isna(reference_value) or reference_value.strip() == "":
                    #print(f"reference_value provided na or blank: {reference_value}")
                    df.at[index, 'value'] = ""
                else:
                    translations = {}
                    for lang, pack in language_packs.items():
                        translation = pack[pack['key'] == reference_value]['reference_value'].values
                        #print(f"lang provided: {lang}")
                        #print(f"pack provided: {pack}")
                        #print(f"translation provided: {translation}")
                        if len(translation) > 0:
                            translations[lang] = translation[0]
                    #print(f"reference_value provided: {row['reference_value']}")
                    translated_text = translate_text(row['reference_value'], row['description'], translations)
                    #print(f"translated_text provided: {translated_text}")
                    df.at[index, 'value'] = translated_text
            
            # Save the DataFrame to a new CSV file with utf-8-sig BOM encoding
            df.rename(columns={'reference_value': 'reference value', 'description': 'description', 'value': 'value'}, inplace=True)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')

print("Translation completed for all CSV files.")
