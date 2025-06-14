import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Data Explorer", layout="wide")

# Title
st.title("📺 Netflix Titles Data Explorer")

# File uploader
uploaded_file = st.file_uploader("Upload 'netflix_titles.csv' file", type="csv")

# Load data function with caching
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)

    # Drop rows missing crucial data
    df.dropna(subset=["type", "title"], inplace=True)

    # Safely convert 'date_added' to datetime
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    return df

# If file is uploaded
if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Load and clean the data
    df = load_data(uploaded_file)

    # Show raw data
    if st.checkbox("Show raw data"):
        st.write(df)

    # Sidebar filters
    st.sidebar.header("Filter Data")
    type_filter = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
    country_filter = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique(), default=None)

    # Apply filters
    filtered_df = df[df['type'].isin(type_filter)]
    if country_filter:
        filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df)

    # Plotting section
    st.subheader("Visualize Data")

    numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    date_col = 'date_added' if 'date_added' in filtered_df.columns else None

    plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Histogram", "Boxplot"])
    col1 = st.selectbox("X-axis", options=filtered_df.columns)
    col2 = st.selectbox("Y-axis (for Boxplot)", options=numeric_cols + ["None"], index=len(numeric_cols))

    # Create plot
    if plot_type and col1:
        fig, ax = plt.subplots(figsize=(10, 5))

        if plot_type == "Bar Chart":
            filtered_df[col1].value_counts().nlargest(20).plot(kind='bar', ax=ax)
            ax.set_ylabel("Count")

        elif plot_type == "Histogram" and col1 in numeric_cols:
            sns.histplot(data=filtered_df, x=col1, bins=30, kde=True, ax=ax)

        elif plot_type == "Boxplot" and col2 != "None":
            sns.boxplot(data=filtered_df, x=col1, y=col2, ax=ax)

        st.pyplot(fig)
    else:
        st.warning("Please select valid columns for the plot.")

    # Footer
    st.markdown("---")
    st.markdown("🎬 Built with Streamlit")

else:
    st.warning("Please upload the 'netflix_titles.csv' file to proceed.")
