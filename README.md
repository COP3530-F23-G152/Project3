# NYC Taxi Trip Data Retrieval

## Overview

This README provides instructions on how to download trip record data from the New York City Taxi and Limousine Commission (TLC) website. The data is available in Parquet format for yellow taxis, green taxis, and commercial taxis. Additionally, you can download the corresponding shapes file to enhance the geographical analysis of the taxi trip data.

## Steps to Retrieve Data

### 1. Access TLC Trip Record Data Page

Visit the [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) page.

### 2. Select Taxi Type

Choose the type of taxi data you are interested in: yellow, green, or commercial taxis. Click on the respective link to navigate to the download page for that specific dataset.

- Yellow Taxis: [Yellow Taxi Trip Records](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- Green Taxis: [Green Taxi Trip Records](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- Commercial Taxis: [Commercial Taxi Trip Records](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

### 3. Download Parquet File

On the download page for the selected taxi type, look for the Parquet data file section. Click on the provided link to download the Parquet file containing the trip records. Save the file to your local machine.

### 4. Download Shapes File

Scroll down to the bottom of the TLC Trip Record Data page to find the shapes file section. Click on the link to download the shapes file corresponding to the taxi trip data. Save the file to your local machine.

### 5. Download Lookup File

Scroll down to the bottom of the TLC Trip Record Data page to find the shapes file section. Click on the link titled "Taxi Zone Lookup Table (CSV)". Sive this file to your local machine.

## Data Usage Notes

- Ensure that you comply with the terms of use and licensing agreements associated with the NYC TLC data.
- The data is provided in Parquet format, a columnar storage format. You may need appropriate tools or libraries to analyze and manipulate the data.

## Usage

This program was designed to be flexible and support all data available from the new york data as well as other data in the same format.
To use this program you must therefor explicitly pass it the data you would like to load.
This can be done as follows:
```python3 main.py [path to lookup file] [path to shape file] [path to trip data file]```
