import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# ----------男女各年齡層所需熱量------------
import altair as alt

# Data for males
age_labels = ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "]
male_lower_limits = [2400, 2150, 1850, 1800, 1700, 1650]
male_upper_limits = [2800, 3350, 2700, 2650, 2500, 2150]

# Data for females
female_lower_limits = [2050, 1650, 1450, 1450, 1400, 1300]
female_upper_limits = [2350, 2550, 2100, 2100, 2000, 1700]

# Combine data into a DataFrame
data = {
    'Age': age_labels * 4,
    'Caloric Intake': male_lower_limits + female_lower_limits + male_upper_limits + female_upper_limits,
    'Type': ['Lower Limit'] * len(age_labels) * 2 + ['Upper Limit'] * len(age_labels) * 2,
    'Gender': ['Male'] * len(age_labels) * 2 + ['Female'] * len(age_labels) * 2
}

df = pd.DataFrame(data)

# Sort DataFrame by 'Type' and 'Gender'
df = df.sort_values(by=['Type', 'Gender'])


# Create a selection
selection = alt.selection_multi(fields=['Gender'], bind='legend')

# Create a base chart
base = alt.Chart(df).encode(
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
scatter = base.mark_circle(size=150)

# Display the chart in Streamlit
st.altair_chart(scatter, use_container_width=True)




