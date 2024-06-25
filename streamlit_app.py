import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# ----------男女各年齡層所需熱量------------
'''
## 各年齡層男女卡路里建議攝取量
'''
# Data for males
age_labels = ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "]
age_positions_male = [-0.2, 0.8, 1.8, 2.8, 3.8, 4.8]
male_lower_limits = [2400, 2150, 1850, 1800, 1700, 1650]
male_upper_limits = [2800, 3350, 2700, 2650, 2500, 2150]

# Data for females
age_positions_female = [0.2, 1.2, 2.2, 3.2, 4.2, 5.2]  # Shift female points slightly to the right
female_lower_limits = [2050, 1650, 1450, 1450, 1400, 1300]
female_upper_limits = [2350, 2550, 2100, 2100, 2000, 1700]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot points and lines for males
ax.scatter(age_labels, male_lower_limits, color='blue', label='Male Lower Limit')
ax.scatter(age_labels, male_upper_limits, color='blue', label='Male Upper Limit')
for i in range(len(age_labels)):
    ax.plot([age_labels[i], age_labels[i]], [male_lower_limits[i], male_upper_limits[i]], 'b-')

# Plot points and lines for females
ax.scatter(age_labels, female_lower_limits, color='red', label='Female Lower Limit')
ax.scatter(age_labels, female_upper_limits, color='red', label='Female Upper Limit')
for i in range(len(age_labels)):
    ax.plot([age_labels[i], age_labels[i]], [female_lower_limits[i], female_upper_limits[i]], 'r-', linewidth=2)

# Annotate points for males
for i, txt in enumerate(male_lower_limits):
    ax.annotate(txt, (age_positions_male[i], male_lower_limits[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, fontweight='bold')
for i, txt in enumerate(male_upper_limits):
    ax.annotate(txt, (age_positions_male[i], male_upper_limits[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, fontweight='bold')

# Annotate points for females
for i, txt in enumerate(female_lower_limits):
    ax.annotate(txt, (age_positions_female[i], female_lower_limits[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, fontweight='bold')
for i, txt in enumerate(female_upper_limits):
    ax.annotate(txt, (age_positions_female[i], female_upper_limits[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, fontweight='bold')

    
ax.set_xlabel('Age')
ax.set_ylabel('Caloric(kcal)')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(age_labels)
# ax.legend(loc='upper right')
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)



