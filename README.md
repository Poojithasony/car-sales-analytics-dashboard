# 🚗 Car Sales Analytics Dashboard

An interactive data analytics project developed using Python, Pandas, Streamlit and Plotly to explore vehicle prices, mileage, manufacturers, fuel types and manufacturing trends.

## 📌 Project Overview

The Car Sales Analytics Dashboard provides an interactive way to explore and analyse a used-car dataset containing 50,000 original records.

The project focuses on data cleaning, exploratory data analysis (EDA), statistical analysis, data visualisation and business insight generation.

Users can apply interactive filters to investigate different segments of the dataset and understand patterns in vehicle pricing and distribution.

## 🎯 Project Objectives

- Analyse vehicle price patterns across manufacturers.
- Explore the relationship between vehicle mileage and price.
- Compare average prices across fuel types.
- Examine manufacturing-year trends.
- Understand the distribution of vehicles by manufacturer and fuel type.
- Identify correlations between numerical variables.
- Perform data cleaning and data-quality validation.
- Present findings through an interactive dashboard.

## 🛠️ Technologies and Tools

| Technology | Purpose |
|---|---|
| Python | Programming and data analysis |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Plotly Express | Interactive data visualisations |
| Streamlit | Interactive dashboard development |

## 📊 Dashboard Features
### 1. Interactive Filters
- Manufacturer selection
- Fuel type selection
- Manufacturing year range
- Vehicle price range

### 2. Key Performance Indicators (KPIs)
- Matching vehicle records
- Number of manufacturers
- Average vehicle price
- Average vehicle mileage

### 3. Exploratory Data Analysis
- Descriptive statistical summary
- Correlation heatmap
- Correlation interpretation

### 4. Data Visualisations
- Average vehicle price by manufacturer
- Vehicle price distribution
- Mileage vs. price scatter plot
- Vehicle distribution by manufacturer
- Vehicle distribution by fuel type
- Average vehicle price by manufacturing year
- Average vehicle price by fuel type

### 5. Business Insights
The dashboard automatically generates insights based on the selected filters, including:
- Manufacturer with the highest average vehicle price
- Manufacturer with the lowest average vehicle price
- Fuel type with the highest average vehicle price
- Most represented manufacturer
- Average mileage of selected vehicles

### 6. Data Quality and Cleaning
- Identification and removal of duplicate records
- Missing-value analysis
- Duplicate-record verification
- Negative price validation
- Negative mileage validation
- Export of the cleaned dataset

### 7. Data Export
Users can download the filtered vehicle records as a CSV file.

## 📸 Dashboard Screenshots

### 1. Dashboard Overview
![Dashboard Overview](Screenshots/01_dashboard_overview.png)

### 2. Correlation Analysis
![Correlation Analysis](Screenshots/05_Correlation.png)

### 3. Vehicle Price Distribution
![Price Distribution](Screenshots/06_Vehicle%20price%20ditribution.png)

### 4. Manufacturing Year Analysis
![Manufacturing Year](Screenshots/11_Average%20car%20price%20by%20manufacturing%20year.png)

### 5. Mileage Analysis
![Mileage Analysis](Screenshots/07_Mileage.png)

### 6. Business Insights
![Business Insights](Screenshots/08_Business%20Insights.png)

## 🧹 Data Preparation and Methodology

The project follows these analytical steps:

1. Load the original vehicle dataset using Pandas.
2. Inspect the dataset and examine numerical statistics.
3. Identify and remove exact duplicate records.
4. Generate a cleaned dataset.
5. Perform exploratory data analysis.
6. Calculate correlations between numerical variables.
7. Build interactive visualisations.
8. Generate business insights based on selected filters.
9. Validate data quality.

## 🔍 Correlation Analysis

The correlation heatmap examines relationships between:

- Engine size
- Year of manufacture
- Mileage
- Price

Correlation values help identify the direction and strength of linear relationships. Correlation does not establish causation.

## 🚀 Installation and Setup

### Prerequisites
- Python installed
- Visual Studio Code (recommended)

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project folder

```bash
cd car_sales_streamlit
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

### Step 5: Open the application

Open the local URL provided in your terminal, usually:

```text
http://localhost:8501
```

## 📁 Project Structure

```text
car_sales_streamlit/
│
├── app.py
├── car_sales_data (1).csv
├── car_sales_cleaned.csv
├── requirements.txt
└── README.md
```

## 💡 Skills Demonstrated

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Descriptive statistics
- Correlation analysis
- Data visualisation
- Interactive dashboard development
- Data-quality validation
- Business insight generation
- Python and Pandas

## 👩‍💻 Author

**MSc Data Science, AI & Digital Business Student**

**Project:** Car Sales Analytics Dashboard

**Technical Stack:** Python | Pandas | NumPy | Plotly | Streamlit