import requests
import json

def get_posts(doi):
    try:
        doi = doi.replace('/', '%2F')
        url = f'https://api.crossref.org/works/{doi}'
        
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    
    except requests.exceptions.RequestException as e:
        print('Request failed:', e)
        return None
    except AttributeError as e:
        print('Attribute error:', e)
        return None

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

#get doi data from excel sheet
doi_path = 'scopus.csv'
# Read the CSV file and extract DOIs
# (Assuming the DOIs are in the first column)
import pandas as pd
df = pd.read_csv(doi_path)
dois = df.iloc[:, 0].tolist()

doi_info = []

coounter = 0

for doi in dois:
    
    print(f'{coounter+1}. Processing DOI: {doi}')
    # Replace '/' with '%2F' in the DOI for the API request
    doi = doi.replace('/', '%2F')
    posts = get_posts(doi)

    if posts:
        doi_info.append(posts)
    else:
        print(f'Failed to retrieve posts for DOI: {doi}')

    coounter += 1
    if coounter == 30:
        break

#Save the collected data to a file
save_to_file(doi_info, 'doi_data.json')
print('Data collection complete. DOI data saved to doi_data.json.')


#Create a world cloud from the collected data
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

full_text = ''

for info in doi_info:
    full_text += ' ' + info.get('message', {}).get('title', [''])[0] + ' ' + info.get('message', {}).get('abstract', [''])[0]
    

# Generate a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(full_text)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file('wordcloud.png')
print('Word cloud saved as wordcloud.png.')