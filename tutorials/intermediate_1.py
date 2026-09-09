import pandas as pd
import re 
import matplotlib.pyplot as plt 

#Reading the csv file into a pandas dataframe
df = pd.read_csv("kaggle_files/fifa21 raw data v2.csv")
print(df.columns)

#Creating a new dataframe to store the cleaned data
my_dataframe = pd.DataFrame()


#Cleaning the Weight column to remove any letters and convert it to float and assigning it to a new column in the my_dataframe
weight = df['Weight'].astype(str).str.replace(r'[a-zA-Z]','',regex=True).astype(float)
my_dataframe['Weight'] = weight
print( f'The cleaned weight values are: \n{weight} and uncleaned values are: \n{df["Weight"]}')

#Cleaning the Height column to remove any letters and convert it to float and assigning it to a new column in the my_dataframe
height = df['Height'].astype(str).str.replace(r'[^0-9]','',regex=True).astype(float)
my_dataframe['Height'] = height
print( f'The cleaned height values are: \n{height} and uncleaned values are: \n{df["Height"]}')

#Cleaning the Joined column to extract the year of joining and convert it to Int64 and assigning it to a new column in the my_dataframe
years_of_play = df['Joined'].astype(str).str.split(',',n=1).str[-1].astype('Int64')
my_dataframe['Years_of_Play'] = years_of_play
print( f'The cleaned years of play values are: \n{years_of_play} and uncleaned values are: \n{df["Joined"]}')

#Calculating the play duration for players who have played for more than 10 years and assigning it to a new column in the my_dataframe
play_duration = years_of_play[(2026 - years_of_play)>10].astype('Int64')
my_dataframe['Play_Duration'] = play_duration
print( f'The play duration values are: \n{play_duration}')

#Adding the play_duration column to the dataframe
df['play_duration']= play_duration


#Calculating the players who have played for more than 10 years and assigning it to a new column in the my_dataframe
players_above_10 = ['Name', 'Joined']
target = 'play_duration'
result = df.loc[df[target].notna(), players_above_10]
my_dataframe[players_above_10] = df.loc[df[target].notna(), players_above_10]
print(f'The players who have played for more than 10 years are: \n{result}')
print(f'The dataframe with the players who have played for more than 10 years are: \n{my_dataframe}')

#function to clean the Wage and Value columns and convert them to raw dilimeter digits equvalent e.g. 1.5M = 1500000, 1.5K = 1500
def raw(x):
    x = str(x).strip().upper()
    currency = x[0]
    value =(x[1:-1])
    multiplier = x[-1]
    if 'K' in x:
        return float(value)*1000
    elif 'M' in x:
        return float(value) *1000000
    else:
        return 
    
#Cleaning the Wage column to remove any letters and convert it to float
wages = df['Wage'].map(raw).astype('float64').dropna()
my_dataframe['Wage'] = wages
print( f'The cleaned wage values are: \n{wages} and uncleaned values are: \n{my_dataframe["Wage"]}')

#Cleaning the Value column to remove any letters and convert it to float
value = df['Value'].map(raw).astype('float64').dropna()
my_dataframe['Value'] = value
print( f'The cleaned value values are: \n{my_dataframe["Value"]} and uncleaned values are: \n{my_dataframe["Value"]}')

#function to clean the star column to remove any letters  returning all digits and convert it to int
def clear_star(x):
    x = str(x).strip()
    x =  re.findall('\\d',x)
    x = ''.join(x)
    return int(x)

#Cleaning the star column to remove any letters and convert it to int
star = df['IR']
star = star.map(clear_star)
my_dataframe['Star'] = star
print(f'The cleaned star values are: \n{my_dataframe["Star"]} and uncleaned values are: \n{df["IR"]}')  


#Plotting the scatter plot of Wages vs Value finding players who are (valuable and have high wages),
#(low wages and low value) , (high wages and low value underpaid) and (low wages and high value overpaid)
plt.scatter(my_dataframe['Wage'],my_dataframe['Value'], alpha=0.5)
plt.title("Valuability of players")
plt.xlabel("Wages")
plt.grid(True)
plt.ylabel("Value")
plt.show()


print(f'The dataframe with the cleaned data is: \n{my_dataframe.dropna()}')
"""
print(f'Is there NaN in Wage column? {my_dataframe["Wage"].isnull().values.any()} and {wages.isnull().values.any()} its shape is {my_dataframe["Wage"].shape} and {wages.shape}')
print(f'Is there NaN in Value column? {my_dataframe["Value"].isnull().values.any()} and {value.isnull().values.any()} its shape is {my_dataframe["Value"].shape} and {value.shape}')
print(f'Is there NaN in Star column? {my_dataframe["Star"].isnull().values.any()} and {star.isnull().values.any()} its shape is {my_dataframe["Star"].shape} and {star.shape}')
print(f'Is there NaN in Weight column? {my_dataframe["Weight"].isnull().values.any()} and {weight.isnull().values.any()} its shape is {my_dataframe["Weight"].shape} and {weight.shape}')
print(f'Is there NaN in Height column? {my_dataframe["Height"].isnull().values.any()} and {height.isnull().values.any()} its shape is {my_dataframe["Height"].shape} and {height.shape}')
print(f'Is there NaN in Years_of_Play column? {my_dataframe["Years_of_Play"].isnull().values.any()} and {years_of_play.isnull().values.any()} its shape is {my_dataframe["Years_of_Play"].shape} and {years_of_play.shape}')
print(f'Is there NaN in Play_Duration column? {my_dataframe["Play_Duration"].isnull().values.any()} and {play_duration.isnull().values.any()} its shape is {my_dataframe["Play_Duration"].shape} and {play_duration.shape}')
print(f'Is there NaN in Name column? {my_dataframe["Name"].isnull().values.any()} and {df["Name"].isnull().values.any()} its shape is {my_dataframe["Name"].shape} and {df["Name"].shape}')
print(f'Is there NaN in Joined column? {my_dataframe["Joined"].isnull().values.any()} and {df['Joined'].isnull().values.any()} its shape is {my_dataframe["Joined"].shape} and {df['Joined'].shape}')
"""
