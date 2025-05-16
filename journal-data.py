# This gets the journal data from using the doi data and issn 

import requests
import json
import pandas as pd
import os


#load doi data from csv
doi_path = 'MasterData.csv'
# Read the CSV file and extract DOIs
# (Assuming the DOIs are in the first column)
df = pd.read_csv(doi_path)
dois = df.iloc[:, 0].tolist()

#get issn data using doi and crossref api
def get_issn(doi):
    try:
        if not isinstance(doi, str) or doi == '':
            print(f"Invalid DOI format: {doi}")
            raise ValueError("DOI is not a string")
        
        doi = doi.replace('/', '%2F')
        url = f'https://api.crossref.org/works/{doi}'
        
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            message = posts.get('message', {})
            issn_list = message.get('ISSN', [])
            if issn_list:
                return issn_list[0]  # Return the first ISSN if available
            else:
                print(f"No ISSN found for DOI: {doi}")
                return None
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

issn_data = []
# Loop through the DOIs and get the ISSN data
counter = 0
for doi in dois:
    issn = get_issn(doi)
    if issn is not None:
        print(f"ISSN data for DOI {doi}: {issn}")
        issn_data.append({'issn':issn, 'doi': doi})
    else:
        print(f"Failed to get ISSN for DOI: {doi}")
        issn_data.append({'issn':'No info', 'doi': doi})
    counter += 1
    """if counter >= 5:
        break
    """

#get citation scores using issn data and scopus api
def get_citation_score(issn):
    print(f"Getting citation score for ISSN: {issn}")
    try:
        if not isinstance(issn, str) or issn == '':
            print(f"Invalid ISSN format: {issn}")
            raise ValueError("ISSN is not a string")
        
        url = f'https://api.elsevier.com/content/serial/title/issn/{issn}'
        # Load API key from config file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        api_key = config.get('ELS-APIKey')
        headers = {
            'Accept': 'application/json',
            'ELS-APIKey': api_key
        }
        
        response = requests.get(url, headers=headers)

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

# Loop through the ISSN data and get the citation scores
for issn in issn_data:
    citation_score = get_citation_score(issn['issn'])
    if citation_score is not None:
        journal = citation_score.get('serial-metadata-response', {}).get('entry', [{}])[0]
        issn['citation_score'] = f"CiteScore: {journal.get('citeScoreYearInfoList', {}).get('citeScoreCurrentMetric', 'N/A')}"
        print(f"Citation score for ISSN {issn['issn']}: {issn['citation_score']}")
    else:
        print(f"Failed to get citation score for ISSN: {issn['issn']}")
        issn['citation_score'] = ' No info'

#save citation score data to csv with issn and doi
df = pd.DataFrame(issn_data)
df.to_csv('issn_data.csv', index=False)
print("ISSN data saved to issn_data.csv")