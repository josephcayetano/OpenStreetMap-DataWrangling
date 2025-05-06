# Open Street Map - Data Wrangling
### Overview
This project cleans and explores OpenStreetMap data for St. Petersburg, Florida, focusing on standardizing street names and postal codes, importing the data into a SQLite database, and analyzing patterns using SQL queries.

### Data Wrangling - OpenStreetMap data for St. Petersburg, Florida
- Audits and corrects inconsistencies in street names and postal codes for uniform formatting.
- Converts raw OpenStreetMap XML data into a structured SQLite database with separate tables for nodes, ways, and tags.
- Analyzes user contributions and geographic data to extract insights like the most common religions, unique users, and editing trends.



### Files
1. README.md - A file describing other files in this repository.

2. audit.py - Python script to audit street names and postal codes in the sample file "petersburg_sample.osm" file.

3. create_sample.py - Python script to get a sample from "petersburg.osm" file. Also includes functions to find unique k attributes and their values.

4. db_tables.py - Python script to create the sqlite database and its tables.

5. fix.py - Python script to update street names and postal codes into a correct format in the "petersburg.osm" file.

6. get_users.py - Python script to get and count users in the "petersburg.osm" file.

7. map_parser.py - Python script to count tag elements in the "petersburg.osm" file.

8. tags.py - Python script to check the K attribute format.

9. pdf_final.pdf - A PDF file containing the data wrangling process of a city's Open Street Map File.

10. petersburg_sample.osm - sample part of St. Petersburg, Florida.

MAP AREA: St. Petersburg, Florida, United States: https://www.openstreetmap.org/relation/118894
Background: As of 2020, St. Petersburg is the 5th most populous city in Florida with a population over 250,000.
