import spacy
import pandas as pd
import re
import numpy as np 
import csv

# Load csv file
col_names = ['position','description']
df = pd.read_csv('job_postings.csv', encoding='latin1', names=col_names)


# load spacy model
nlp = spacy.load('en_core_web_sm')

def extract_lines_with_skills(text):
    pattern  =   r"(?m)^[\s]*([\x95\xb7]|\d+\)|\-|\d+\.)\s*(.*)$"
    # Finding all matches in the text
    matches = re.findall(pattern, text)
    return matches

def extract_noun_phrases(list_text):
    clean_list_np = []
    
    if (len(list_text)>0):
        for line in list_text:
            #print('\nLINE: {}'.format(line[-1]))
            text = line[-1]
            #print(text)
            doc = nlp(text)
            for chunk in doc.noun_chunks:
                clean_np = []
                for token in chunk:
                    if (token.pos_!='PRON' and token.pos_!='DET' and token.text!='(' and token.text!='"' and token.text!='*'):
                        clean_np.append(str(token))
                t1 = " ".join(clean_np)
                
                if (chunk.root.text not in ['that','-','#']):
                    if ((chunk.root.dep_=='dobj') and (chunk.root.pos_!='PROPN')):
                        #new_chunk = chunk.root.head.lemma_ + " " + chunk.text
                        new_chunk = chunk.root.head.lemma_ + " " + t1
                        clean_list_np.append(new_chunk.strip())
                    else:
                        if (len(t1)>0):
                            clean_list_np.append(t1.strip())
    return clean_list_np        
    

# Pre-process text. Extract noun_phrases and add them in a new column
df['description'] = df['description'].str.replace(r'\x96',' ',regex=True)
df['lines_extracted'] = df['description'].apply(extract_lines_with_skills)
df['noun_phrases'] = df['lines_extracted'].apply(extract_noun_phrases) 

# Export to csv
with open('job_posting_noun_phrases.csv', 'w', newline='', encoding='latin1') as file:
     writer = csv.writer(file)     
     writer.writerow(["job_posting_index", "noun_phrase_original","noun_phrase_lowercase","target"])
     for i in range(len(df)):
         if (len(df['noun_phrases'][i])>0): 
             for noun_phrase in df['noun_phrases'][i]:
                     writer.writerow([i, noun_phrase,noun_phrase.lower(),"nan"])
                 
# Remove duplicates 
df2 = pd.read_csv('job_posting_noun_phrases.csv', encoding='latin1')
df2 = df2.drop_duplicates(subset=['noun_phrase_lowercase'],keep='first')
df2.to_excel("list_noun_phrases.xlsx") 




# Load csv file
data2 = pd.read_csv('list_noun_phrases.csv', encoding='latin1')
data_train = data2[~data2['technical_keywords'].isna()]
