## This is a simulation project for learning how to stream data into a database and then showcase it on a dashboard.

The dataset is a simulated delivery dataset from Kaggle.
Data streaming is simulated with a Python script that inserts rows into an SQLite database.
Data is processed and analyzed with Pandas.

The dashboard is built with Streamlit. It includes:
    KPI cards (average and p90 delivery times, total orders)
    Distribution of delivery times
    Filters by area, vehicle type and weather
    An interactive map of drop-off locations.

## How to use
1. clone the repo here:
    git clone https://github.com/kasevaj/Data-Engineering-last-mile-logistics.git
    cd Data-Engineering-last-mile-logistics

2. install dependencies:
       npm install    
3. Make sure you have a .env file
4. Start the program
    Frontend -> npm start
    Backend -> npm run dev

## Project structure
Data-Engineering-last-mile-logistics/
-│
-├── backend/ 
-├── frontend/ 
-├── .env
-└── README.md

<img width="545" height="369" alt="image" src="https://github.com/user-attachments/assets/0709d9ab-145d-47a5-9679-88aced7b2370" />

<img width="538" height="415" alt="image" src="https://github.com/user-attachments/assets/e5d9a67e-6dfc-4c84-829a-de75680e335e" />

