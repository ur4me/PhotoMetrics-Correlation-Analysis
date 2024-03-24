# PhotoMetrics-Correlation-Analysis

## Overview
This repository contains a comprehensive analysis workflow that processes image metadata to explore correlations between different photographic metrics. The project is structured into four main steps, each encapsulated in its own Jupyter notebook, and culminates in a detailed correlation analysis report.

## Getting Started
To run this project, you'll need to have [Jupyter Notebook](https://jupyter.org/install) or [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) installed on your machine. Additionally, ensure that you have Python 3.x installed along with the necessary libraries mentioned in each notebook.

### Step 1: Extract JPG Preview Images from DNG Files
- **Notebook**: `step1.ipynb`
- **Description**: This step processes a collection of DNG files to extract embedded JPG preview images.
- **How to Run**: Open `step1.ipynb` in Jupyter Notebook/Lab and execute all cells.

### Step 2: Extract EXIF Metadata
- **Notebook**: `step2.ipynb`
- **Description**: This step extracts EXIF metadata from the DNG or JPG images and caches the metadata for subsequent analysis.
- **How to Run**: After completing Step 1, open `step2.ipynb` and run all cells to extract metadata.

### Step 3: Create HSV/HSL Histograms
- **Notebook**: `step3.ipynb`
- **Description**: Generates HSV/HSL histograms from the JPG images and caches the histogram information.
- **How to Run**: With Steps 1 and 2 completed, open `step3.ipynb` and execute all cells to create the histograms.

### Step 4: Correlation Analysis
- **Notebook**: `step4.ipynb`
- **Description**: Performs a detailed correlation analysis using the extracted metadata and histogram data, exploring relationships between various photographic metrics.
- **How to Run**: Ensure Steps 1 through 3 are completed, then open `step4.ipynb` and run all cells to perform the correlation analysis.

## Correlation Analysis Report
The final output of this project is the **Correlation Analysis Report**, which details the findings from the correlation analysis conducted in Step 4. This report provides insights into the relationships between different photographic metrics and discusses significant correlations identified during the analysis.

- **Report File**: `Correlation Analysis Report.md`

## License
This project is open-source and available under the [MIT License](LICENSE).
