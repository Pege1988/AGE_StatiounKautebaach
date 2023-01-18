# AGE Statioun Kautebaach

## Description
This Python script does the following:
1. Extract data from water levels at Station Kautenbach (data from inondation.lu)
2. Add data to csv data file
3. Add data to sql db
4. Send alarm in case of flooding (risk) via e-mail

## TO DO
- Add exception handling
- Improve HTML for e-mail message

## Installation notes
For testing purposes, variable test needs to be True, so that the script runs locally.
Once dev finished, put test to False and store py file on Synology NAS.
For integration testing purposes, run script manually on Synology and check results.
