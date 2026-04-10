# CIS 4930: Introduction to Python

## Project 1: Real World Data Storytelling: Spanish High-Speed Train Tickets

### Group 14 Members:
 - **Gerry Kramer**: gjk22@fsu.edu
 - **Luis Medina**: lcm24d@fsu.edu
 - **Brandon Pina**: bp22c@fsu.edu
 - **Lenoardo Ribera**: lr21k@fsu.edu

## Project Description
This project explores a dataset of Spanish high-speed train (AVE) ticket prices collected in 2019.
Using exploratory data analysis, we investigate how ticket prices vary across train classes, fare types,
routes, and travel times, with the goal of uncovering the key factors that drive pricing in Spain's national rail network.

## Dataset
- **Source** [Spain Public Transportation on Kaggle](https://www.kaggle.com/code/qusaybtoush1990/spain-public-transportation)
- **Format:** CSV
- **Size:** 500,000 rows
- **Key columns:**
  - `origin`, `destination` — departure and arrival cities
  - `start_date`, `end_date` — departure and arrival timestamps
  - `train_type` — type of train service (AVE, ALVIA)
  - `train_class` — class of service (Turista, Preferente)
  - `fare` — fare type (Promo, Flexible)
  - `price` — ticket price in euros
 

### Why this dataset fits the requirements

The dataset contains well over 500 rows and includes multiple numeric columns (`price`, trip duration, hour, month) and multiple categorical columns (`origin`, `destination`, `train_type`, `train_class`, `fare`), making it well suited for group analysis and visualisation. It represents a real-world context — public transportation pricing — with a clear and plausible story to tell.

---

## Research Questions
1. Does fare type (Promo vs Flexible) significantly affect ticket price?
2. Do weekday departures have different average prices compared to weekend departures?
3. How does average ticket price vary across different train classes?
4. What is the distribution of trip durations, and how does it vary by origin city?
5. Which hours and days of the week see the highest volume of train departures?

---

## Repo Structure
```
├── data/
│   ├── raw/
│   │   ├── reduced_spain_data.csv  # reduced data with 500,000 rows
│   │   ├── spaintransportdata.csv  # original raw data with 2.5 million rows
├── figures/
│   ├── bar_plot.png
│   ├── correlation_heatmap.png
│   ├── histogram.png
│   ├── line_plot.png
│   ├── price_by_fare.png
│   └── price_weekday_vs_weekend.png
│   ├── scatter_plot.png
├── notebooks/
│   ├── analysis.ipynb  # Main Jupyter notebook
│   ├── requirements.txt
├── contributions.md  # list of contributions from each group member
└── README.md
```

## Notebook Structure
The main analysis is organized in `analysis.ipynb` following these sections:
 
1. **Data Loading and Initial Inspection** — reading the CSV, checking data types and missing values
2. **Cleaning and Transformation** — handling missing values, type conversions, feature engineering
3. **Descriptive Statistics and Simple EDA** — overall price stats and breakdown by train class
4. **Visualizations and Feature Exploration** — line, bar, scatter, and histogram plots; research questions answered with grouped stats and plots
5. **Summary and Key Findings** — plain-English interpretation of results

---
 
## How to Run
 
1. Clone the repository  
   ```bash
   git clone https://github.com/gerry-kramer/python_p1_RealWorldDataStorytelling.git
   ```
2. Change directory to repo nad activate virtual environment
   ```bash
   cd .\python_p1_RealWorldDataStorytelling\
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r .\notebooks\requirements.txt
   pip install jupyter  # if not already installed
   ```
4. Launch Jupyter Notebook or Jupyter Lab
   ```bash
   jupyter notebook
   # or jupyter lab
   jupyter lab
   ```
5. Open `analysis.ipynb` in Jupyter Notebook or JupyterLab
6. Run all cells from top to bottom (`Kernel` → `Restart & Run All`)
