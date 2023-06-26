import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Sedia Payung Sebelum Hujan, Tapi Kapan?')
st.subheader('An analysis of climate change that happens in Indonesia')
st.write('by Nafis Azizi Riza, Computer Science, Universitas Indonesia')
st.markdown("---")

st.header('Background')
"""The dry season lasts from April to September, and the rainy season is from October to March,
according to textbooks for elementary schools. However, the BMKG  states that the wet season runs 
from November to April, and the dry season from May to October. There is difference about the time
of the season between BMKG and the literature that we taught in elementary. Also we frequently get
rain during the dry season, so this analysis will demonstrate how long each season lasts in Indonesia.
Rainfall and climate change are intimately intertwined, thus this analysis will take climate change into 
account as well as explore for any intriguing connections."""

# -------------------------------------------DATA PREPARATION-----------------------------------------------
# 
df_ina = pd.read_csv('dataset/ina/df_ina.csv', encoding='unicode_escape')

rename = {"Jan":'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',\
         'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',\
         'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

for lab, row in df_ina.iterrows():
    df_ina.loc[lab, 'month'] = rename[row['month']]

# read the csv files and merge them altogether
mean_temp = pd.read_csv('dataset/mean_temp/mean_temp.csv', encoding='unicode_escape')
max_temp = pd.read_csv('dataset/max_temp/max_temp.csv', encoding='unicode_escape')
min_temp = pd.read_csv('dataset/min_temp/min_temp.csv', encoding='unicode_escape')
precipitation = pd.read_csv('dataset/precipitation/precipitation.csv', encoding='unicode_escape')

df_region = mean_temp.copy()
df_region['max_temp'] = max_temp['max_temp']
df_region['min_temp'] = min_temp['min_temp']
df_region['precipitation'] = precipitation['precipitation']

for lab, row in df_region.iterrows():
    df_region.loc[lab, 'month'] = rename[row['month']]

# -------------------------------------------DATA PREPARATION-----------------------------------------------

st.header('Analysis')

# TEMPREATURE AND RAINFALL 1901 - 2021
st.subheader('Temperature and Rainfall (1901-2021)')
# Visualization
df_ina_group = df_ina.groupby('month').mean().drop('year', axis=1)
plt.figure(figsize=(12, 6))
ax1 = sns.barplot(data=df_ina_group, x=df_ina_group.index, y='precipitation', palette='rocket')
plt.ylim(150,300) 
plt.ylabel('precipitation (mm)')
ax2 = ax1.twinx()
sns.lineplot(data=df_ina_group.loc[:,['mean_temp', 'max_temp', 'min_temp']],\
                   markers=True, ax=ax2, markersize=10,palette='viridis')
plt.ylim(20,33)
plt.ylabel('temperature (celsius)')
label  = [mth[3:] for mth in df_ina_group.index.unique()]
ax1.set_xticklabels(label)
plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left', borderaxespad=0)
st.pyplot(plt.gcf())

"""According to BMKG, the wet season occurs between November and April, leaving May through October typically 
dry. In Indonesia, the average monthly temperature ranges from 25 to 26 degrees Celsius all year long. The 
most recent climatology, 1901–2021, shows that the average monthly rainfall varies significantly. The dry 
season, from June to September, is when there is the least amount of rain; the average monthly rainfall in 
June and July is between 160 and 180 mm. While the highest rainfall occurs in December to March, between 255 
and 290 mm. The hypothesis remains to be proven correct because rainfall still occurs between May and October 
(around 210 mm-230 mm), even though it is the dry season."""


# HIGHEST/LOWEST TEMP AND RAINFALL
st.subheader('Region With Highest/Lowest Temperature and Rainfall')
temp_tab, prp_tab = st.tabs(['Temperature', 'Precipitation'])
df_region_group = df_region.groupby('province_name').mean().drop('year', axis=1)

# Temperature
with temp_tab:
    st.subheader('Average Temperature for Each Region in Indonesia (1901-2021)')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_region_group, x=df_region_group.index, y='mean_temp',\
            order=df_region_group.sort_values('mean_temp').index, palette='rocket')
    plt.ylim(23,28)
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    """Indonesia's capital, Jakarta, has an average temperature of 27 degrees Celsius, making it the 
    warmest region. While Sulawesi Barat, with an average temperature of 23.9 degrees Celsius, is the 
    coldest region."""

# Precipitation
with prp_tab:
    st.subheader('Average Precipitation for Each Region in Indonesia (1901-2021)')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_region_group, x=df_region_group.index, y='precipitation',\
            order=df_region_group.sort_values('precipitation').index, palette='rocket')
    plt.ylim(140,285)
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    """The heaviest rainfall throughout the year occurs in Papua and Kalimantan Barat, in around 
    275 mm. While the least region to rain is Nusa Tenggara Barat, Nusa Tenggara Timur, and Sulawesi 
    Tengah between 148 mm and 150 mm."""



# RAINFALL COMPARISON
st.subheader('Rainfall Comparison Between 1901-1910 and 2012-2021')
# VISUALIZATION
df_first = df_ina[(df_ina['year'] >= 1901) & (df_ina['year'] <= 1910)]
df_first = df_first.groupby('month').mean()
df_last = df_ina[(df_ina['year'] >= 2012) & (df_ina['year'] <= 2021)]
df_last = df_last.groupby('month').mean()
df_merge = pd.concat([df_first, df_last])
df_merge['year'] = df_merge['year'].replace({1905.5:'1901-1910', 2016.5:'2012-2021'})
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=df_merge, x=df_merge.index,hue='year',\
                  y='precipitation', palette='rocket')
plt.ylim(150,310)
label  = [mth[3:] for mth in df_ina_group.index.unique()]
ax.set_xticklabels(label)
st.pyplot(plt.gcf())

"""The pattern of the rainfall from the first decade (1901-1910) and the last decade (2012-2021) 
doesn't have a lot of differences. The main difference that notice is the gap value between the lowest 
rainfall at august and heaviest rainfall at december. This leaving a question in mind. See next figure!"""

prp_gap = df_merge.groupby('year').mean()
prp_gap['prp_max'] = df_merge.groupby('year').max()['precipitation']
prp_gap['prp_min'] = df_merge.groupby('year').min()['precipitation']
prp_gap['prp_gap'] = prp_gap['prp_max'] - prp_gap['prp_min']
plt.figure(figsize=(12, 6))
sns.barplot(data=prp_gap, x=prp_gap.index, y='prp_gap',palette='rocket')
plt.ylim(100,140)
st.pyplot(plt.gcf())

"""By subtracting the maximum value with the minimum value of each decade. The gap between the first 
and second decade is pretty high. Means, that in the last decade, during the dry season, it rains less 
and during the peak of rainfall, the heaviest the rain compared to the first decade."""


st.subheader('Average Temperature from 1901-2021')
df_avg_annual = df_ina.groupby('year').mean()
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_avg_annual, x=df_avg_annual.index, y='mean_temp',color='red')
st.pyplot(plt.gcf())
"""Temperature trend seems to remain constant from 1901 to 1980. Starting from 1980, the average annual 
temperature raising until 2021, having the highest average temperature at 2012 in 25.99 degree celsius."""


st.subheader('Fun Facts - Correlation With Other Factors')
"""To find the correlation between temperature and precipitation, I gathered additional data related to 
access to electricity (% to population), forest area (% of land area), CO2 emissions (metric tons per 
capita), individuals using the internet (% of population), and total population. It seems that 
precipitation does not have any correlation with the other variables."""

# data prep
addi = pd.read_excel('dataset/additional/additional.xlsx')
df_avg_annual = df_ina.groupby('year').mean()
df_avg_annual = df_avg_annual.merge(addi, left_on=df_avg_annual.index, right_on='year')
df_avg_annual = df_avg_annual[df_avg_annual['year']>=2000]

# data viz
plt.figure(figsize=(12,12))
sns.heatmap(df_avg_annual.corr(), annot=True)
st.pyplot(plt.gcf())

corr = st.selectbox(
     'Select variables to see the correlation',
     ('Electricity vs Mean Temperature', 'Forest area vs Mean Temperature',
     'CO2 Emission vs Mean Temperature', 'Internet vs Mean Temperature',
     'Population vs Mean Temperature', 'Electricity vs Forest Area',
     'Electricity vs CO2 Emission', 'Electricity vs Internet',
     'Electricity vs Population'))

if corr == 'Electricity vs Mean Temperature':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='electricity', y='mean_temp')
    st.pyplot(plt.gcf())
elif corr == 'Forest area vs Mean Temperature':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='forest_area', y='mean_temp')
    st.pyplot(plt.gcf())
elif corr == 'CO2 Emission vs Mean Temperature':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='co2_emissio', y='mean_temp')
    st.pyplot(plt.gcf())
elif corr == 'Internet vs Mean Temperature':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='internet', y='mean_temp')
    st.pyplot(plt.gcf())
elif corr == 'Population vs Mean Temperature':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='population', y='mean_temp')
    st.pyplot(plt.gcf())
elif corr == 'Electricity vs Forest Area':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='electricity', y='forest_area')
    st.pyplot(plt.gcf())
elif corr == 'Electricity vs CO2 Emission':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='electricity', y='co2_emission')
    st.pyplot(plt.gcf())
elif corr == 'Electricity vs Internet':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='electricity', y='internet')
    st.pyplot(plt.gcf())
elif corr == 'Electricity vs Population':
    plt.figure(figsize=(12, 6))
    sns.regplot(data=df_avg_annual, x='electricity', y='population')
    st.pyplot(plt.gcf())


st.header('Conclusion')
"""1. The wet season occurs between November and April, leaving May through October typically dry. Although, rain can still be found during the dry season.
2. Highest rainfall occurs in December, while lowest rainfall happens in July.
3. Papua is the region with the highest rainfall, while Nusa Tenggara Barat is the lowest region to have rain.
4. Jakarta is the warmest region, and Sulawesi Barat is the coldest region.
5. There is a pretty high precipitation gap between 1901-19010 and 2012-2021. In the last decade, during the dry season, it rains less and during the peak of rainfall, the heaviest the rain compared to the first decade.
6. Temperature trend seems to remain constant from 1901 to 1980. Starting from 1980, the average annual temperature raising until 2021.
7. There is strong positive correlation between year and average temperature.
8. Electricity, CO2 emission, and population also have strong positive correlation to average temperature.
9. Forest area has very strong negative correlation with average temperature, while internet has very strong positive correlation with average temperature.
"""
