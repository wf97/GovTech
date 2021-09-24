Run:
pip install -r requirements.txt

## Section 1: Data Pipelines
In the root directory, run docker-compose up -d
Go to: http://localhost:8080/ to see the dag
processed csv is in the subdirectory /dag/test.csv

## Section 2: Databases
SQL commands for setting up database, tables and queries in init.sql
ER diagram is in the Section_2 subfolder

## Section 3: System Design
You are designing data infrastructure on the cloud for a company whose main business is in processing images. 

The company has a web application which collects images uploaded by customers. The company also has a separate web application which provides a stream of images using a Kafka stream. The company’s software engineers have already some code written to process the images. The company  would like to save processed images for a minimum of 7 days for archival purposes. Ideally, the company would also want to be able to have some Business Intelligence (BI) on key statistics including number and type of images processed, and by which customers.

Produce a system architecture diagram (e.g. Visio, Powerpoint) using any of the commercial cloud providers' ecosystem to explain your design. Please also indicate clearly if you have made any assumptions at any point.

## Section 4: Charts and APIs
In the root directory, run python Section_4/viz.py
Go to: http://127.0.0.1:8050/ to view the visualisation

## Section 5: Machine Learning
Code and comments are in /Section_5/Car.ipynb