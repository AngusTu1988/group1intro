import streamlit as st
import pandas as pd
import altair as alt

# 男女各年齡層每日所需卡路里-----
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

# ---------------------------------------------------------------





