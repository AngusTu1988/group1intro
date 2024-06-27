import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib as plt
import plotly.express as px



# Set page configuration
st.set_page_config(
    page_title="Custom Width Streamlit App",
    layout="wide",
)

# Inject custom CSS to control the width
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 800px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Introduction')

'''
## 熱量是什麼？為什麼我們需要熱量？
任何事物的運作都需要能量，也包含生物的運動、心臟跳動、思考、生長發育都需要消耗能量。在營養學上，最主要的熱量單位是大卡（千卡，kcal），熱量來自於三大營養素，醣類、蛋白質與脂肪，醣類與蛋白質一公克可以提供 4 大卡的熱量，脂肪一公克則可提供 9 大卡，每克的酒精則能提供 7 大卡熱量；維生素、礦物質、纖維和水則不會提供我們身體熱量。

攝取的食物，會經過體內一連串複雜的消化過程再轉化為熱量，並維持人體基本代謝，其餘則以肝醣的形式儲存於肝臟、供給肌肉收縮消耗，多出的熱量則以脂肪組織儲存，常在皮下或內臟周圍組織。

'''


'''

'''
tab1, tab2, tab3 = st.tabs(["每日熱量攝取建議量", "脂溶性維生素/微量元素建議攝取量", "維生素B群建議攝取量"])

with tab1:
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
        x=alt.X('Age:N', title='年齡'),
        y=alt.Y('Caloric Intake:Q', title='卡路里攝取量(kcal)'),
        color=alt.condition(selection, 'Gender:N', alt.value('lightgray'), scale=alt.Scale(domain=['Male', 'Female'], range=['lightblue', 'pink'])),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=['Age', 'Caloric Intake', 'Gender', 'Type']
    ).add_selection(
        selection
    ).properties(
        width=600,
        height=400,
        title='每日建議卡路里攝取量(kcal)'    
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
        'Vitamin K (μg)': [75, 75, 120, 120, 120, 120],
        'Vitamin B1 (mg)': [1.3, 1.4, 1.2, 1.2, 1.2, 1.2],
        'Vitamin B2 (mg)': [1.5, 1.6, 1.3, 1.3, 1.3, 1.3],
        'Vitamin B6 (mg)': [1.4, 1.5, 1.5, 1.5, 1.6, 1.6],
        'Vitamin B12 (mg)': [0.024, 0.024, 0.024, 0.024, 0.024, 0.024],
        'Niacin (mg)': [18, 18, 16, 16, 16, 16],
        'Folate (mg)': [400, 400, 400, 400, 400, 400],
        'Choline (mg)': [460, 500, 450, 450, 450, 450],
        'Pantothenic Acid (mg)': [4.5, 5, 5, 5, 5, 5],
        'Calcium (mg)': [1200, 1200, 1000, 1000, 1000, 1000],
        'Phosphorus (mg)': [1000, 1000, 800, 800, 800, 800],
        'Magnesium (mg)': [350, 390, 380, 380, 360, 350],
        'Iron (mg)': [15, 15, 10, 10, 10, 10],
        'Zinc (mg)': [15, 15, 15, 15, 15, 15],
        'Iodine (mg)': [0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
        'Selenium (mg)': [0.05, 0.055, 0.055, 0.055, 0.055, 0.055],
        'Fluoride (mg)': [3, 3, 3, 3, 3, 3],
        'Sodium (mg)': [2300, 2300, 2300, 2300, 2300, 2300],
        'Potassium (mg)': [2800, 2800, 2800, 2800, 2800, 2800]
    }

    male_df = pd.DataFrame(male_data)
    male_df['Gender'] = 'Male'
    male_df['Gender1'] = 'Male '
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
        'Vitamin K (μg)': [75, 75, 90, 90, 90, 90],
        'Vitamin B1 (mg)': [0.1, 1.1, 0.9, 0.9, 0.9, 0.9],
        'Vitamin B2 (mg)': [1.3, 1.2, 1, 1, 1, 1],
        'Vitamin B6 (mg)': [1.3, 1.3, 1.5, 1.5, 1.6, 1.6],
        'Vitamin B12 (mg)': [0.024, 0.024, 0.024, 0.024, 0.024, 0.024],
        'Niacin (mg)': [15, 15, 14, 14, 14, 14],
        'Folate (mg)': [400, 400, 400, 400, 400, 400],
        'Choline (mg)': [380, 370, 390, 390, 390, 390],
        'Pantothenic Acid (mg)': [4.5, 5, 5, 5, 5, 5],
        'Calcium (mg)': [1200, 1200, 1000, 1000, 1000, 1000],
        'Phosphorus (mg)': [1000, 1000, 800, 800, 800, 800],
        'Magnesium (mg)': [320, 330, 320, 320, 310, 300],
        'Iron (mg)': [15, 15, 15, 15, 10, 10],
        'Zinc (mg)': [12, 12, 12, 12, 12, 12],
        'Iodine (mg)': [0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
        'Selenium (mg)': [0.05, 0.055, 0.055, 0.055, 0.055, 0.055],
        'Fluoride (mg)': [3, 3, 3, 3, 3, 3],
        'Sodium (mg)': [2300, 2300, 2300, 2300, 2300, 2300],
        'Potassium (mg)': [2500, 2500, 2500, 2500, 2500, 2500]}
    
    female_df = pd.DataFrame(female_data)
    female_df['Gender'] = 'Female'
    female_df['Gender1'] = 'Female '
    female_df['Fat (g)'] = round((female_df['Caloric Intake Avg'] * 0.25) / 9, 2)


    # Combine data for plotting
    combined_df = pd.concat([male_df, female_df])
    

    # Create nutrient and vitamin groups
    nutrients = ['Protein (g)', 'Carbohydrates (g)', 'Dietary Fiber (g)', 'Fat (g)']
    vitamins = ['Vitamin A (μg)', 'Vitamin D (μg)', 'Vitamin K (μg)']
    b_vitamins = ['Vitamin B1 (mg)', 'Vitamin B2 (mg)', 'Vitamin B6 (mg)', 'Vitamin B12 (mg)', 'Niacin (mg)', 'Folate (mg)', 'Choline (mg)', 'Pantothenic Acid (mg)']
    trace_elements = ['Calcium (mg)', 'Phosphorus (mg)', 'Magnesium (mg)', 'Iron (mg)', 'Zinc (mg)', 'Iodine (mg)', 'Selenium (mg)', 'Fluoride (mg)', 'Sodium (mg)', 'Potassium (mg)']
    

    # Melt the DataFrame to make it suitable for Plotly plotting
    melted_df = combined_df.melt(id_vars=['Age', 'Gender'], value_vars=nutrients + vitamins, var_name='Nutrient', value_name='Amount')
    melted_df1 = combined_df.melt(id_vars=['Age', 'Gender1'], value_vars=b_vitamins + trace_elements, var_name='B Vitamins', value_name='Amount1')

    # Sort the DataFrame by Age
    age_order = ["13 - 15", "16 - 18", "19 - 30", "31 - 50", "51 - 70", "71 - "]
    melted_df['Age'] = pd.Categorical(melted_df['Age'], categories=age_order, ordered=True)
    melted_df = melted_df.sort_values('Age')

    melted_df1['Age'] = pd.Categorical(melted_df1['Age'], categories=age_order, ordered=True)
    melted_df1 = melted_df1.sort_values('Age')

    return melted_df, nutrients, vitamins, b_vitamins, trace_elements, melted_df1


# Load the data
melted_df, nutrients, vitamins, b_vitamins, trace_elements, melted_df1  = load_data()

with tab2:
##########################################################
# Create layout with two columns
    col1, col2= st.columns([3, 1])

    with col2:
        # Create selection boxes for group in the right column
        group = st.radio("Select Group", ("Nutrients", "A/D/E Vitamins"))
        gender = st.radio("Select Gender", ("Male", "Female"))

    # Filter the data based on the selected group
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
                        'Vitamin K (μg)': 'indianred',  # 淡粉色                     
                    },
                    title=f"{group} Distribution for {gender}",
                    labels={'Amount': y_axis_title})
        
        
        fig.update_layout(
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.4,
                yanchor="bottom"            
            )               
            
        )

        # Display the chart in Streamlit
        
        st.plotly_chart(fig)


with tab3:
####################################################################
    col3, col4= st.columns([3, 1])


    with col4:
        # Create selection boxes for group in the right column
        gender1 = st.radio("Select Gender", ("Male ", "Female "))
        group1 = st.radio("Select Group", ("B Vitamin", "Trace Elements"))
        

    # Filter the data based on the selected group
    if group1 == "B Vitamin":
        filtered_df1 = melted_df1[(melted_df1['Gender1'] == gender1) & (melted_df1['B Vitamins'].isin(b_vitamins))]
        y_axis_title1 = 'Amount (mg)[log scale]'
    else:
        filtered_df1 = melted_df1[(melted_df1['Gender1'] == gender1) & (melted_df1['B Vitamins'].isin(trace_elements))]
        y_axis_title1 = 'Amount (mg)[log scale]'


    with col3:
        # Create the grouped bar chart
        fig1 = px.bar(filtered_df1, x='Amount1', y='Age', color='B Vitamins', orientation='h', barmode='group', log_x = True,
                    color_discrete_map={
                        'Vitamin B1 (mg)': 'lightyellow',  # 米白色
                        'Vitamin B2 (mg)': 'grey',  # 淡灰色
                        'Vitamin B6 (mg)': 'lightgreen',  # 淡綠色
                        'Vitamin B12 (mg)': 'rgb(255, 204, 153)',  # 淡橘色
                        'Niacin (mg)': 'royalblue',  # 淡藍色
                        'Folate (mg)': 'rosybrown',  # 淡珊瑚色
                        'Choline (mg)': 'indianred',  # 淡粉色
                        'Pantothenic Acid (mg)': 'gold',  # 金色
                        'Calcium (mg)': 'orange',  # 橙色
                        'Phosphorus (mg)': 'lightcoral',  # 淡珊瑚色
                        'Magnesium (mg)': 'darkred',  # 深红色
                        'Iron (mg)': 'peru',  # 秘鲁色                    
                        'Zinc (mg)': 'teal',  # 水鸭色
                        'Iodine (mg)': 'lightblue',  # 淡蓝色
                        'Selenium (mg)':'red', # 紅色
                        'Fluoride (mg)':'yellow', # 黃色
                        'Sodium (mg)':'green', # 綠色
                        'Potassium (mg)':'purple' # 紫色

                    },
                    title=f"{group1} Distribution for {gender1}",
                    labels={'Amount1': y_axis_title1})
        
        
        fig1.update_layout(
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.6,
                yanchor="bottom"            
            )               
            
        )

        # Display the chart in Streamlit
        
        st.plotly_chart(fig1)




