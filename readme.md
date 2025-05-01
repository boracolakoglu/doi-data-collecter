# DOI Data Collector

This project is a Python-based tool for collecting and analyzing data from DOIs (Digital Object Identifiers) using the CrossRef API. It processes a list of DOIs from a CSV file, retrieves metadata, and generates visualizations such as word clouds and year-wise publication counts.

## Features

- Fetch metadata for DOIs using the CrossRef API.
- Save collected metadata to a JSON file.
- Generate a word cloud from titles and abstracts.
- Create a bar chart for year-wise publication counts.

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

1. Place your CSV file containing DOIs in the project directory. Ensure the DOIs are in the first column of the file.
2. Update the `doi_path` variable in the script with the name of your CSV file (e.g., `scopus.csv`).
3. Run the script:
     ```bash
     python script_name.py
     ```
4. The script will:
     - Fetch metadata for each DOI.
     - Save the metadata to `doi_data.json`.
     - Generate a word cloud and save it as `wordcloud.png`.
     - Create a bar chart for year-wise publication counts and save it as `year_wise_publication_counts.png`.

## Output

- `doi_data.json`: Contains the metadata for all processed DOIs.
- `wordcloud.png`: A word cloud visualization of titles and abstracts.
- `year_wise_publication_counts.png`: A bar chart showing the number of publications per year.

## Notes

- The script includes error handling for invalid DOIs and API request failures.
- You can limit the number of DOIs processed by uncommenting and modifying the `coounter` condition in the loop.
- The word cloud and bar chart are saved as image files and not displayed during script execution to avoid blocking.

## License

This project is licensed under the MIT License. See the LICENSE file for details.