
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Car Sales Analytics",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Sales Analytics Dashboard")
st.caption("Explore vehicle prices, mileage, manufacturers and fuel types.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("car_sales_data (1).csv")

# Load original dataset
df_raw = load_data()

# Create cleaned dataset
df_cleaned = df_raw.drop_duplicates().copy()

# Calculate cleaning metrics
original_records = len(df_raw)
cleaned_records = len(df_cleaned)
duplicates_removed = original_records - cleaned_records

# Display cleaning results
st.subheader("Data Cleaning Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Original Records", f"{original_records:,}")
col2.metric("Cleaned Records", f"{cleaned_records:,}")
col3.metric("Duplicates Removed", f"{duplicates_removed:,}")

# Save cleaned dataset
df_cleaned.to_csv("car_sales_cleaned.csv", index=False)

st.success("Cleaned dataset saved successfully!")

# Use cleaned dataset for dashboard analysis
df = df_cleaned.copy()

# Exploratory Data Analysis

st.header("Exploratory Data Analysis (EDA)")

st.subheader("1. Descriptive Statistics")

# Statistical summary of numerical columns
descriptive_stats = df_cleaned.describe().T

descriptive_stats = descriptive_stats.rename(
    columns={
        "count": "Count",
        "mean": "Mean",
        "std": "Standard Deviation",
        "min": "Minimum",
        "25%": "25th Percentile",
        "50%": "Median",
        "75%": "75th Percentile",
        "max": "Maximum"
    }
)

st.dataframe(
    descriptive_stats.round(2),
    width="stretch"
)

# Correlation Analysis
st.subheader("2. Correlation Analysis")

correlation = df_cleaned[
    ["Engine size", "Year of manufacture", "Mileage", "Price"]
].corr()

fig_corr = px.imshow(
    correlation,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Correlation Between Numerical Variables",
    aspect="auto"
)

st.plotly_chart(fig_corr, width="stretch")

# Correlation Interpretation

st.subheader("Correlation Interpretation")

# Select only the upper triangle to avoid duplicate pairs
upper_triangle = np.triu(
    np.ones(correlation.shape, dtype=bool),
    k=1
)

correlation_pairs = correlation.where(upper_triangle).stack()

if not correlation_pairs.empty:

    strongest_pair = correlation_pairs.abs().idxmax()
    strongest_value = correlation_pairs.loc[strongest_pair]

    st.info(
        f"The strongest correlation is between "
        f"**{strongest_pair[0]}** and **{strongest_pair[1]}**, "
        f"with a correlation coefficient of "
        f"**{strongest_value:.2f}**."
    )

    st.caption(
        "Correlation measures association between variables. "
        "It does not establish causation."
    )
else:
    st.warning("Not enough numerical variables for correlation analysis.")
    
# Sidebar filters
st.divider()
st.sidebar.caption("Explore vehicle prices, mileage and market trends.")
st.sidebar.divider()

st.sidebar.header("Filter Cars")

manufacturers = sorted(df["Manufacturer"].dropna().unique())
selected_manufacturers = st.sidebar.multiselect(
    "Select manufacturers",
    manufacturers,
    default=manufacturers
)

fuel_types = sorted(df["Fuel type"].dropna().unique())
selected_fuels = st.sidebar.multiselect(
    "Select fuel types",
    fuel_types,
    default=fuel_types
)

min_year = int(df["Year of manufacture"].min())
max_year = int(df["Year of manufacture"].max())

selected_years = st.sidebar.slider(
    "Manufacturing year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

min_price = int(df["Price"].min())
max_price = int(df["Price"].max())

selected_price = st.sidebar.slider(
    "Car price range (€)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Apply filters
filtered_df = df[
    df["Manufacturer"].isin(selected_manufacturers)
    & df["Fuel type"].isin(selected_fuels)
    & df["Year of manufacture"].between(
        selected_years[0], selected_years[1]
    )
    & df["Price"].between(
        selected_price[0], selected_price[1]
    )
]

# Dashboard metrics
st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matching Records",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Manufacturers",
    filtered_df["Manufacturer"].nunique()
)

col3.metric(
    "Average Price",
    f"€{filtered_df['Price'].mean():,.0f}"
    if not filtered_df.empty else "N/A"
)

col4.metric(
    "Average Mileage",
    f"{filtered_df['Mileage'].mean():,.0f} km"
    if not filtered_df.empty else "N/A"
)

# Handle empty results
if filtered_df.empty:
    st.warning("No cars match these filters. Please change your selections.")
else:
    # Data preview
    st.subheader("Car Sales Data")
    st.dataframe(filtered_df.head(100), width="stretch")

    # Download Filtered Dataset
    st.subheader("Download Filtered Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_car_sales.csv",
        mime="text/csv"
    )

    # Average price by manufacturer
    st.subheader("Average Price by Manufacturer")

    price_data = (
        filtered_df.groupby("Manufacturer", as_index=False)["Price"]
        .mean()
        .sort_values("Price", ascending=False)
    )

    fig = px.bar(
        price_data,
        x="Manufacturer",
        y="Price",
        color="Manufacturer",
        text_auto=".2s",
        title="Average Vehicle Price by Manufacturer",
        labels={
            "Manufacturer": "Car Manufacturer",
            "Price": "Average Price (€)"
        },
        hover_data={"Price": ":,.2f"}
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average Price: €%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        yaxis=dict(
            tickprefix="€",
            tickformat=",.0f",
            title="Average Price (€)"
        ),
        xaxis_title="Manufacturer",
        showlegend=False,
        margin=dict(t=70, b=40)
    )

    st.plotly_chart(fig, width="stretch")

    # Price distribution
    st.subheader("Vehicle Price Distribution")

    fig2 = px.histogram(
        filtered_df,
        x="Price",
        color="Fuel type",
        nbins=30,
        title="Distribution of Vehicle Prices",
        labels={
            "Price": "Vehicle Price (€)",
            "count": "Number of Vehicles",
            "Fuel type": "Fuel Type"
        },
        hover_data=["Manufacturer"]
    )

    fig2.update_layout(
        xaxis=dict(
            tickprefix="€",
            tickformat=",.0f",
            title="Vehicle Price (€)"
        ),
        yaxis_title="Number of Vehicles",
        legend_title="Fuel Type",
        bargap=0.08
    )

    st.plotly_chart(fig2, width="stretch")

    # Mileage analysis
    st.subheader("Mileage vs Price")

    mileage_sample = filtered_df.sample(
        min(len(filtered_df), 3000),
        random_state=42
    )

    fig3 = px.scatter(
        mileage_sample,
        x="Mileage",
        y="Price",
        color="Manufacturer",
        hover_data=["Model", "Year of manufacture", "Fuel type"],
        title="Relationship Between Vehicle Mileage and Price",
        labels={
            "Mileage": "Mileage (km)",
            "Price": "Vehicle Price (€)",
            "Manufacturer": "Manufacturer"
        },
        opacity=0.65
    )

    fig3.update_layout(
        xaxis=dict(
            tickformat=",.0f",
            title="Mileage (km)"
        ),
        yaxis=dict(
            tickprefix="€",
            tickformat=",.0f",
            title="Vehicle Price (€)"
        ),
        legend_title="Manufacturer",
        hovermode="closest"
    )

    st.plotly_chart(fig3, width="stretch")

    # Business Insights
    st.divider()
    st.subheader("Business Insights")

    if not filtered_df.empty:

        manufacturer_prices = (
            filtered_df.groupby("Manufacturer")["Price"]
            .mean()
            .sort_values(ascending=False)
        )

        fuel_prices = (
            filtered_df.groupby("Fuel type")["Price"]
            .mean()
            .sort_values(ascending=False)
        )

        top_manufacturer = manufacturer_prices.idxmax()
        low_manufacturer = manufacturer_prices.idxmin()

        top_fuel = fuel_prices.idxmax()
        popular_manufacturer = (
            filtered_df["Manufacturer"].value_counts().idxmax()
        )

        average_mileage = filtered_df["Mileage"].mean()

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"**Highest Average Price**\n\n"
                f"{top_manufacturer}: "
                f"€{manufacturer_prices.max():,.0f}"
            )

            st.info(
                f"**Highest Priced Fuel Category**\n\n"
                f"{top_fuel}: €{fuel_prices.max():,.0f}"
            )

            st.info(
                f"**Most Represented Manufacturer**\n\n"
                f"{popular_manufacturer}"
            )

        with col2:
            st.info(
                f"**Lowest Average Price**\n\n"
                f"{low_manufacturer}: "
                f"€{manufacturer_prices.min():,.0f}"
            )

            st.info(
                f"**Average Vehicle Mileage**\n\n"
                f"{average_mileage:,.0f} km"
            )

        # Insight 1: Highest average price manufacturer
        manufacturer_insights = (
            filtered_df.groupby("Manufacturer")["Price"]
            .mean()
            .sort_values(ascending=False)
        )

        top_manufacturer = manufacturer_insights.idxmax()
        top_manufacturer_price = manufacturer_insights.max()

        st.write(
            f"**1. Highest Average Price:** "
            f"{top_manufacturer} has the highest average car price "
            f"at €{top_manufacturer_price:,.0f}."
        )

        # Insight 2: Highest average price fuel type
        fuel_insights = (
            filtered_df.groupby("Fuel type")["Price"]
            .mean()
            .sort_values(ascending=False)
        )

        top_fuel = fuel_insights.idxmax()
        top_fuel_price = fuel_insights.max()

        st.write(
            f"**2. Fuel Type Analysis:** "
            f"{top_fuel} vehicles have the highest average price "
            f"at €{top_fuel_price:,.0f}."
        )

        # Insight 3: Average mileage
        average_mileage = filtered_df["Mileage"].mean()

        st.write(
            f"**3. Mileage Analysis:** "
            f"The average mileage of the selected vehicles is "
            f"{average_mileage:,.0f} km."
        )

    # 2. Manufacturer Distribution
    st.subheader("Vehicle Distribution by Manufacturer")

    manufacturer_counts = (
        filtered_df["Manufacturer"]
        .value_counts()
        .reset_index()
    )

    manufacturer_counts.columns = [
        "Manufacturer",
        "Number of Vehicles"
    ]

    fig4 = px.bar(
        manufacturer_counts,
        x="Manufacturer",
        y="Number of Vehicles",
        color="Manufacturer",
        text="Number of Vehicles",
        title="Number of Vehicles by Manufacturer",
        labels={
            "Manufacturer": "Car Manufacturer",
            "Number of Vehicles": "Number of Vehicles"
        }
    )

    fig4.update_traces(
        textposition="outside",
        hovertemplate=(
            "Manufacturer: %{x}<br>"
            "Vehicles: %{y:,}"
            "<extra></extra>"
        )
    )

    fig4.update_layout(
        xaxis_title="Manufacturer",
        yaxis_title="Number of Vehicles",
        showlegend=False,
        yaxis=dict(tickformat=","),
        margin=dict(t=70, b=40)
    )

    st.plotly_chart(fig4, width="stretch")

    # 3. Fuel Type Distribution
    st.subheader("Vehicle Distribution by Fuel Type")

    fuel_counts = (
        filtered_df["Fuel type"]
        .value_counts()
        .reset_index()
    )

    fuel_counts.columns = [
        "Fuel Type",
        "Number of Vehicles"
    ]

    fig5 = px.pie(
        fuel_counts,
        names="Fuel Type",
        values="Number of Vehicles",
        hole=0.45,
        title="Vehicle Distribution by Fuel Type"
    )

    fig5.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "Fuel Type: %{label}<br>"
            "Vehicles: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig5.update_layout(
        legend_title="Fuel Type",
        margin=dict(t=70, b=40)
    )

    st.plotly_chart(fig5, width="stretch")

    # 4. Average Car Price by Manufacturing Year
    st.subheader("Average Car Price by Manufacturing Year")

    yearly_prices = (
        filtered_df.groupby("Year of manufacture")["Price"]
        .mean()
        .reset_index()
        .sort_values("Year of manufacture")
    )

    fig6 = px.line(
        yearly_prices,
        x="Year of manufacture",
        y="Price",
        markers=True,
        title="Average Vehicle Price Across Manufacturing Years",
        labels={
            "Year of manufacture": "Manufacturing Year",
            "Price": "Average Price (€)"
        }
    )

    fig6.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "Year: %{x}<br>"
            "Average Price: €%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig6.update_layout(
        xaxis_title="Manufacturing Year",
        yaxis=dict(
            tickprefix="€",
            tickformat=",.0f",
            title="Average Price (€)"
        ),
        hovermode="x unified"
    )

    st.plotly_chart(fig6, width="stretch")

        # 5. Average Price by Fuel Type
    st.subheader("Average Car Price by Fuel Type")

    fuel_avg_price = (
        filtered_df.groupby("Fuel type")["Price"]
        .mean()
        .reset_index()
        .sort_values("Price", ascending=False)
    )

    fig7 = px.bar(
        fuel_avg_price,
        x="Fuel type",
        y="Price",
        color="Fuel type",
        text_auto=".2s",
        title="Average Vehicle Price by Fuel Type",
        labels={
            "Fuel type": "Fuel Type",
            "Price": "Average Price (€)"
        }
    )

    fig7.update_traces(
        textposition="outside",
        hovertemplate=(
            "Fuel Type: %{x}<br>"
            "Average Price: €%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig7.update_layout(
        yaxis=dict(
            tickprefix="€",
            tickformat=",.0f",
            title="Average Price (€)"
        ),
        xaxis_title="Fuel Type",
        showlegend=False,
        margin=dict(t=70, b=40)
    )

    st.plotly_chart(fig7, width="stretch")

# Data Quality Checks
st.divider()
st.header("🔎 Data Quality Checks")

# Original dataset quality
original_rows = len(df_raw)
original_missing = int(df_raw.isna().sum().sum())
original_duplicates = int(df_raw.duplicated().sum())

missing_prices = int(df_raw["Price"].isna().sum())
invalid_prices = int((df_raw["Price"].dropna() < 0).sum())
invalid_mileage = int((df_raw["Mileage"].dropna() < 0).sum())

# Cleaned dataset quality
cleaned_rows = len(df_cleaned)
cleaned_missing = int(df_cleaned.isna().sum().sum())

# Original dataset metrics
st.subheader("Original Dataset Quality")

q1, q2, q3 = st.columns(3)

q1.metric("Original Records", f"{original_rows:,}")
q2.metric("Missing Cells", f"{original_missing:,}")
q3.metric("Duplicate Occurrences", f"{original_duplicates:,}")

q4, q5, q6 = st.columns(3)

q4.metric("Missing Prices", f"{missing_prices:,}")
q5.metric("Negative Prices", f"{invalid_prices:,}")
q6.metric("Negative Mileage", f"{invalid_mileage:,}")

# Cleaned dataset metrics
st.subheader("Cleaned Dataset Quality")

c1, c2, c3 = st.columns(3)

c1.metric("Cleaned Records", f"{cleaned_rows:,}")
c2.metric("Missing Cells", f"{cleaned_missing:,}")
c3.metric(
    "Duplicates Remaining",
    f"{int(df_cleaned.duplicated().sum()):,}"
)

# Missing values by column
st.subheader("Missing Values by Column")

missing_by_column = (
    df_raw.isna()
    .sum()
    .rename("Missing Values")
    .reset_index()
)

missing_by_column.columns = ["Column", "Missing Values"]

st.dataframe(
    missing_by_column,
    width="stretch",
    hide_index=True
)

# Duplicate record preview
st.subheader("Duplicate Record Preview")

duplicates = df_raw[df_raw.duplicated(keep=False)]

if duplicates.empty:
    st.success("No exact duplicate rows found.")
else:
    st.warning(
        f"Found {original_duplicates:,} duplicate occurrences "
        "after the first occurrence."
    )

    st.dataframe(
        duplicates.head(20),
        width="stretch",
        hide_index=True
    )

st.caption(
    "Car Sales Analytics | Built with Python, Pandas, Streamlit and Plotly"
)