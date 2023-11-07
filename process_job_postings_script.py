import spacy
import pandas as pd
import re
import numpy as np 
import csv

# Load csv file
col_names = ['position','description']
df = pd.read_csv('job_postings.csv', encoding='latin1', names=col_names)

# pre-processing
df['new_description'] = df['description'].str.replace(r'\.?\n+','. ',regex=True)
df['new_description'] = df['new_description'].str.replace(r'\x95','',regex=True)
df['new_description'] = df['new_description'].str.replace(r'^-\s?','',regex=True)
df['new_description'] = df['new_description'].str.replace(r'^\s?\d\)?\s?\.\s?','',regex=True)
df['new_description'] = df['new_description'].str.replace(r'[\.\.\.]',' ',regex=True)
df['new_description'] = df['new_description'].str.replace(r'"',' ',regex=True)
df['new_description'] = df['new_description'].str.replace(r':',' ',regex=True)
df['new_description'] = df['new_description'].str.replace(r'\*','',regex=True)
df['new_description'] = df['new_description'].str.replace(r'\(',' ',regex=True)
df['new_description'] = df['new_description'].str.replace(r'\)',' ',regex=True)
df['new_description'] = df['new_description'].str.replace(r'\s+',' ',regex=True)

# load spacy model
nlp = spacy.load('en_core_web_sm')

def extract_noun_phrases(text):
    doc = nlp(text) 
    all_noun_phrases = []
    for chunk in doc.noun_chunks:
        elements = []
        for token in chunk:
            if (token.pos_!='PRON' and token.pos_!='DET'):
                elements.append(str(token))
        # list of elements to string
        if (len(elements)>0):
            single_noun_phrase = ' '.join(elements)
            split_np = []
            if (',' in single_noun_phrase):
                split_np = re.split(r'[,]',single_noun_phrase)
                for i in range(len(split_np) - 1):
                    split_np[i] = re.sub(r'^\s+','', split_np[i])
                    split_np[i] = re.sub(r'\s+$','', split_np[i])
                    split_np[i] += " " + chunk.root.text
                split_np[-1] = re.sub(r'^\s*[and]*\s*','',split_np[-1])
                for i in split_np:
                    all_noun_phrases.append(i.lower())
            else:
                # add noun phrase string to total list
                all_noun_phrases.append(single_noun_phrase.lower())
    all_noun_phrases = np.unique(all_noun_phrases)
    return all_noun_phrases


# Pre-process text. Extract noun_phrases and add them in a new column
df['noun_phrases'] = df['new_description'].apply(extract_noun_phrases) 

# Export to csv
with open('job_posting_noun_phrases.csv', 'w', newline='', encoding='latin1') as file:
     writer = csv.writer(file)     
     writer.writerow(["job_posting_index", "noun_phrase"])
     for i in range(len(df)):
         for noun_phrase in df['noun_phrases'][i]:
                 writer.writerow([i, noun_phrase])
                 
# Remove duplicates 
df2 = pd.read_csv('job_posting_noun_phrases.csv', encoding='latin1')
df2 = df2.drop_duplicates(subset=['noun_phrase'],keep='first')
df2.to_excel("list_noun_phrases.xlsx") 