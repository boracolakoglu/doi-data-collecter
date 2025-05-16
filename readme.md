# DOI Data Collector

This project is a Python-based toolkit for collecting, enriching, and analyzing metadata from DOIs (Digital Object Identifiers) using the CrossRef and Scopus APIs. It supports extracting journal and citation information, as well as generating visualizations from publication data.

## Features

- Fetch metadata for DOIs using the CrossRef API.
- Save collected metadata to a JSON file.
- Generate a word cloud from publication titles and abstracts.
- Create a bar chart for year-wise publication counts.
- **Extract ISSN and citation metrics for journals using DOIs and the Scopus API.**
- **Save enriched journal and citation data to CSV for further analysis.**

## Requirements

- Python 3.x
- Required Python libraries:
    - `requests`
    - `pandas`
    - `json`
    - `wordcloud`
    - `matplotlib`

Install the required libraries using:
```bash
pip install requests pandas wordcloud matplotlib
```

## Usage

### 1. Collect DOI Metadata

1. Place your CSV file containing DOIs in the project directory. Ensure the DOIs are in the first column of the file (e.g., `MasterData.csv`).
2. Update the `doi_path` variable in `doi-data-collecter.py` if needed.
3. Run the collector script:
    ```bash
    python doi-data-collecter.py
    ```
4. The script will:
    - Fetch metadata for each DOI from CrossRef.
    - Save the metadata to `doi_data.json`.
    - Generate a word cloud (`wordcloud.png`) from titles and abstracts.
    - Create a bar chart (`year_wise_publication_counts.png`) for publication counts by year.

### 2. Enrich with Journal and Citation Data

1. Ensure you have a `config.json` file with your Scopus API key:
    ```json
    {
      "ELS-APIKey": "YOUR_SCOPUS_API_KEY"
    }
    ```
2. Run the journal data enrichment script:
    ```bash
    python journal-data.py
    ```
3. The script will:
    - Read DOIs from your CSV file.
    - For each DOI, fetch the ISSN using the CrossRef API.
    - For each ISSN, fetch citation metrics (e.g., CiteScore) from the Scopus API.
    - Save the combined data (DOI, ISSN, citation score) to `issn_data.csv`.

## Output

- `doi_data.json`: Metadata for all processed DOIs.
- `wordcloud.png`: Word cloud of publication titles and abstracts.
- `year_wise_publication_counts.png`: Bar chart of publication counts per year.
- `issn_data.csv`: Table with DOI, ISSN, and citation score for each entry.

## Notes

- The scripts include error handling for invalid DOIs, missing ISSNs, and API request failures.
- You can limit the number of DOIs processed by uncommenting and modifying the counter condition in the loop.
- The word cloud and bar chart are saved as image files and not displayed during script execution.
- The Scopus API requires a valid API key in `config.json`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.