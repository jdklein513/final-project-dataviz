# final-project-dataviz

MLB Pitcher Scouting Report (Final Project for DSCI590 Data Visualization)

## Synopsis

This project builds an analytics dashboard tracking travel levels before, during, and after the COVID-19 pandemic while gaining insight on the driving factors halting travel recovery in specific areas of the country. 
Although the Bureau of Transportation reports travel statistics directly on their website, there is no readily available dashboard which compares current travel rates directly to pre-COVID rates. In addition, there is also no single source which highlights the relationship between metro status, political voting, demographics, and weather - all effects shown to be associated with higher vaccination rates, case counts, and general apprehension of COVID-19 - on travel recovery. The resulting dashboard demonstrates the recovery rates over time by vaccination rate, average age, and weather patterns, as well as compares travel recovery of metro counties vs. non-metro counties, and democratic vs. republican counties respectively. The project repository contains the supporting code to implement the pipeline within Google Cloud Platform.


## Repo Structure

+ **setup**: includes code to run on local machine to setup python virtual environment and package requirements to pip install into environment.
    + setup.sh: code to run on local machine to setup python virtual environment
    + requirements.txt: package requirements to pip install into environment

+ **data_prep**: stores Python code in jupyter notebooks for extracting data from public APIs and preparing the data needed for the visualization report

    + 00_statcast_data_download: This script loads in MLB statcast data from every MLB registered pitch in 2021. The data is scraped from *baseballsavant.com*. The prepped data is written to the data folder.

    + 01_statcast_data_preparation: This script loads in MLB statcast data from every MLB registered pitch in 2021 from starting pitchers and prepares the data for use in the starting pitcher scouting report. The prepped data is written to the data folder.

+ **notebooks**: stores the Python code in jupyter notebook for the pitcher scouting visualization report.

    + mlb_pitcher_scouting_report: Loads prepped data in from data folder and produces interactive visualization report. When editing the file in jupyter notebook, clicking the Voila nbconvert extension renders the markdown in an interactive session hosted locally on your machine.


+ **output**: store the reports and presentations for the project deliverables.

## How to run

This code assumes you are operating on a Windows OS.

1. Execute the setup.sh script
2. pip install packages from requirements.txt
3. Open data_prep/00_statcast_data_download, change data folder location, and execute each code chunk
4. Open data_prep/01_statcast_data_preparation, change data folder location, and execute each code chunk
5. Open notebooks/mlb_pitcher_scouting_report, execute each code chunk, click Voila extension to host application


## Contributors

* Joel Klein (joeklein@iu.edu)
