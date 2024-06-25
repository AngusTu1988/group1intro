import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib as plt
import plotly.express as px

# Data for males
age_labels = ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "]
male_lower_limits = [2400, 2150, 1850, 1800, 1700, 1650]
male_upper_limits = [2800, 3350, 2700, 2650, 2500, 2150]

# Data for females
female_lower_limits = [2050, 1650, 1450, 1450, 1400, 1300]
female_upper_limits = [2350, 2550, 2100, 2100, 2000, 1700]

# Create DataFrames for male and female data
male_data = {
    'Age': age_labels,
    'Lower Limit': male_lower_limits,
    'Upper Limit': male_upper_limits,
    'Gender': ['Male'] * len(age_labels)
}

female_data = {
    'Age': age_labels,
    'Lower Limit': female_lower_limits,
    'Upper Limit': female_upper_limits,
    'Gender': ['Female'] * len(age_labels)
}

df_male = pd.DataFrame(male_data)
df_female = pd.DataFrame(female_data)

# Combine data into a single DataFrame for plotting
df_combined = pd.concat([df_male, df_female])

# Melt the DataFrame to make it suitable for Altair plotting
df_melted = df_combined.melt(id_vars=['Age', 'Gender'], value_vars=['Lower Limit', 'Upper Limit'], var_name='Type', value_name='Caloric Intake')

# Create a DataFrame for the lines
line_data = []
for idx, row in df_combined.iterrows():
    line_data.append({'Age': row['Age'], 'Caloric Intake': row['Lower Limit'], 'Gender': row['Gender']})
    line_data.append({'Age': row['Age'], 'Caloric Intake': row['Upper Limit'], 'Gender': row['Gender']})
line_df = pd.DataFrame(line_data)

# Create a selection
selection = alt.selection_multi(fields=['Gender'], bind='legend')

# Create a base chart
base = alt.Chart(df_melted).encode(
    x=alt.X('Age:N', title='Age'),
    y=alt.Y('Caloric Intake:Q', title='Caloric Intake (kcal)'),
    color=alt.condition(selection, 'Gender:N', alt.value('lightgray'), scale=alt.Scale(domain=['Male', 'Female'], range=['lightblue', 'pink'])),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    tooltip=['Age', 'Caloric Intake', 'Gender', 'Type']
).add_selection(
    selection
).properties(
    width=600,
    height=400,
    title='Suggested Caloric Intake Range by Age and Gender'    
)

# Create the scatter plot
scatter = base.mark_circle(size=60)

# Create the vertical lines
lines = alt.Chart(line_df).mark_line(size=6).encode(
    x='Age:N',
    y='Caloric Intake:Q',
    color=alt.condition(selection, 'Gender:N', alt.value('lightgray'), scale=alt.Scale(domain=['Male', 'Female'], range=['lightblue', 'pink'])),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    detail='Age:N'
).add_selection(
    selection
)

# Combine the scatter plot and the vertical lines
chart = scatter + lines

# Display the combined chart in Streamlit
st.altair_chart(chart, use_container_width=True)



# Define a function to load and process the data
@st.cache_data
def load_data():
    # Data for males
    male_data = {
        'Age': ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "],
        'Protein (g)': [70, 75, 70, 70, 70, 70],
        'Carbohydrates (g)': [115, 115, 115, 115, 115, 115],
        'Dietary Fiber (g)': [34, 30, 26, 25, 24, 23],
        'Caloric Intake Avg': [2400, 2750, 2275, 2225, 2100, 1900],  # 平均值
        'Vitamin A (μg)': [600, 700, 600, 600, 600, 600],
        'Vitamin D (μg)': [10, 10, 10, 10, 15, 15],
        'Vitamin K (μg)': [75, 75, 120, 120, 120, 120]
    }

    male_df = pd.DataFrame(male_data)
    male_df['Gender'] = 'Male'
    male_df['Fat (g)'] = round((male_df['Caloric Intake Avg'] * 0.25) / 9, 2)

    # Data for females
    female_data = {
        'Age': ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "],
        'Protein (g)': [60, 55, 60, 60, 60, 60],
        'Carbohydrates (g)': [115, 115, 115, 115, 115, 115],
        'Dietary Fiber (g)': [29, 23, 20, 20, 20, 20],
        'Caloric Intake Avg': [2200, 2100, 1775, 1775, 1700, 1500],  # 平均值
        'Vitamin A (μg)': [500, 500, 500, 500, 500, 500],
        'Vitamin D (μg)': [10, 10, 10, 10, 15, 15],
        'Vitamin K (μg)': [75, 75, 90, 90, 90, 90]
    }

    female_df = pd.DataFrame(female_data)
    female_df['Gender'] = 'Female'
    female_df['Fat (g)'] = round((female_df['Caloric Intake Avg'] * 0.25) / 9, 2)

    # Combine data for plotting
    combined_df = pd.concat([male_df, female_df])

    # Create nutrient and vitamin groups
    nutrients = ['Protein (g)', 'Carbohydrates (g)', 'Dietary Fiber (g)', 'Fat (g)']
    vitamins = ['Vitamin A (μg)', 'Vitamin D (μg)', 'Vitamin K (μg)']

    # Melt the DataFrame to make it suitable for Plotly plotting
    melted_df = combined_df.melt(id_vars=['Age', 'Gender'], value_vars=nutrients + vitamins, var_name='Nutrient', value_name='Amount')

    # Sort the DataFrame by Age
    age_order = ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "]
    melted_df['Age'] = pd.Categorical(melted_df['Age'], categories=age_order, ordered=True)
    melted_df = melted_df.sort_values('Age')

    return melted_df, nutrients, vitamins

# Load the data
melted_df, nutrients, vitamins = load_data()

# Create layout with two columns
col1, col2 = st.columns([4, 1])

with col2:
    # Create selection boxes for group and gender in the right column
    group = st.radio("Select Group", ("Nutrients", "Vitamins"))
    gender = st.radio("Select Gender", ("Male", "Female"))

# Filter the data based on the selected group and gender
if group == "Nutrients":
    filtered_df = melted_df[(melted_df['Gender'] == gender) & (melted_df['Nutrient'].isin(nutrients))]
    y_axis_title = 'Amount (g)'
else:
    filtered_df = melted_df[(melted_df['Gender'] == gender) & (melted_df['Nutrient'].isin(vitamins))]
    y_axis_title = 'Amount (μg)'

with col1:
    # Create the grouped bar chart
    fig = px.bar(filtered_df, x='Amount', y='Age', color='Nutrient', orientation='h', barmode='group',
                 color_discrete_map={
                     'Protein (g)': 'lightyellow',  # 米白色
                     'Carbohydrates (g)': 'grey',  # 淡灰色
                     'Dietary Fiber (g)': 'lightgreen',  # 淡綠色
                     'Fat (g)': 'rgb(255, 204, 153)',  # 淡橘色
                     'Vitamin A (μg)': 'royalblue',  # 淡藍色
                     'Vitamin D (μg)': 'rosybrown',  # 淡珊瑚色
                     'Vitamin K (μg)': 'indianred'  # 淡粉色
                 },
                 title=f"{group} Distribution for {gender}",
                 labels={'Amount': y_axis_title})

    # Display the chart in Streamlit
    st.plotly_chart(fig)
