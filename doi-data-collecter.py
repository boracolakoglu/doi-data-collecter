import requests
import json

def get_posts(doi):
    try:
        if not isinstance(doi, str) or doi == '':
            print(f"Invalid DOI format: {doi}")
            raise ValueError("DOI is not a string")
        
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
    except ValueError as e:
        print('Value error:', e)
        return None

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

#get doi data from excel sheet
doi_path = 'MasterData.csv'
# Read the CSV file and extract DOIs
# (Assuming the DOIs are in the first column)
import pandas as pd
df = pd.read_csv(doi_path)
dois = df.iloc[:, 0].tolist()

doi_info = []

counter = 0
fail = 0

for doi in dois:
    
    print(f'{counter+1}. Processing DOI: {doi}')
    # Replace '/' with '%2F' in the DOI for the API request
    posts = get_posts(doi)

    if posts:
        doi_info.append(posts)
    else:
        print(f'Failed to retrieve posts for DOI: {doi}')
        fail += 1


    #In case you want to limit the number of DOIs processed
    counter += 1
    """
    if counter == 30:
        break
    """

#Save the collected data to a file
save_to_file(doi_info, 'doi_data.json')
print('Data collection complete. DOI data saved to doi_data.json.')

print(f'Total DOIs processed: {counter}')  
print(f'Total DOIs failed: {fail}')
print(f'Failure rate: {fail/counter*100:.2f}%')

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
#Not showing the plot in the new window to avoid blocking the script
#plt.show()
wordcloud.to_file('wordcloud.png')
print('Word cloud saved as wordcloud.png.')

# Create a bar chart for year-wise publication counts
year_counts = {}
for info in doi_info:
    year = info.get('message', {}).get('created', {}).get('date-parts', [[]])[0][0]
    if year:
        year = str(year)
        if year in year_counts:
            year_counts[year] += 1
        else:
            year_counts[year] = 1

# Sort the year counts
sorted_year_counts = dict(sorted(year_counts.items()))
# Create a bar chart
plt.figure(figsize=(10, 5))
plt.bar(sorted_year_counts.keys(), sorted_year_counts.values())
plt.xlabel('Year')
plt.ylabel('Publication Count')
plt.title('Year-wise Publication Counts')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('year_wise_publication_counts.png')
#Not showing the plot in the new window to avoid blocking the script
#plt.show()