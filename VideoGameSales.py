import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
sales = pd.read_csv('vgchartz-2024.csv')

#DATA EXPLORATION

sales.head()
pd.isnull(sales).sum()
sales.info()

#Find the top 10 least popular games by total sales
x = sales.sort_values('total_sales', ascending=True).head(10)
x[['title', 'total_sales']]

#Find summary statistics for each numeric column
sales.describe().transpose()

#Find the top 10 most popular games by total sales by filtering for all 
#games with total sales greater than 10 million and sorting them in descending order
#then selecting title, total sales, console, and critic score columns
x = sales
y = x[x['total_sales'] > 10].sort_values('total_sales', ascending=False).head(10)
y[['title', 'total_sales', 'console', 'critic_score']]

#Set release date as index and convert to datetime format
sales.set_index('release_date', inplace=True)
sales.index = pd.to_datetime(sales.index, format='mixed', errors='coerce')
sales.head()
#Find the title from the seventh row of the dataset
sales[['title']].iloc[7]


#What genres have the highest total sales globally? 
# Group the data by genre and sum the total sales for each genre, 
# then sort the results in descending order and create a bar chart to visualize the total global sales by genre.
genre_sales = (sales.groupby('genre')['total_sales'].sum().sort_values(ascending=True))
plt.figure(figsize=(10,8))
genre_sales.plot(kind='barh', color = sns.color_palette("mako", len(genre_sales)))
plt.title("Total Global Sales by Genre")
plt.xlabel("Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()
#Sports games have the highest total sales globally, followed by Action and Shooter games.

#Which platforms have the highest total sales and average sales per game?
platform_sales = sales.groupby('console')['total_sales'].sum().sort_values(ascending=False)
platform_avg = sales.groupby('console')['total_sales'].mean().sort_values(ascending=False)

#Create a bar chart to visualize total global sales by platform
platform_total = (sales.groupby('console')['total_sales'].sum().sort_values(ascending=False).head(15).sort_values(ascending=True))
plt.figure(figsize=(10,6))
platform_total.plot(kind='barh', color = sns.color_palette("mako", len(platform_total)))
plt.title("Total Global Revenue by Platform")
plt.xlabel("Total Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()

#Create a bar chart to visualize average sales per game by platform
platform_avg = (sales.groupby('console')['total_sales'].mean().sort_values(ascending=False).head(15).sort_values(ascending=True))
plt.figure(figsize=(10,6))
platform_avg.plot(kind='barh', color = sns.color_palette("mako", len(platform_avg)))
plt.title("Average Sales Per Game by Platform")
plt.xlabel("Average Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()

#We can see that Playstation has greater revenue across all of their consoles than other companies
#however, the average sales per game is higher for Nintendo meaning Playstation has more games with 
# lower sales while Nintendo has fewer games with higher sales on average.


#Total sales by region
regional_totals = sales[['na_sales','pal_sales','jp_sales','other_sales']].sum()
plt.figure(figsize=(8,6))
regional_totals.plot(kind='bar', color = sns.color_palette("mako", len(regional_totals)))
plt.title("Total Video Game Sales by Region")
plt.ylabel("Sales (Millions)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
#We can see that North America has the highest total sales, followed by PAL (Europe and African), Japan, and other regions.

#Which genres are most popular in each region?
regions = ['na_sales','pal_sales','jp_sales', 'other_sales']
for region in regions:
    top_genres = (sales.groupby('genre')[region].sum().sort_values(ascending=False).head(8).sort_values())
    plt.figure(figsize=(8,6))
    top_genres.plot(kind='barh', color = sns.color_palette("mako", len(top_genres)))
    plt.title(f"Top Genres in {region.upper()}")
    plt.xlabel("Sales (Millions)")
    plt.tight_layout()
    plt.show()
# In NA Sports(most popular), Action and Shooter games are the most popular genres. 
# In PAL, Sports, Action(most popular), and Shooter games are also the most popular. 
# In Japan, Role-Playing(most popular), Action, and Sports genres are the most popular. 
# In other regions, Sports(most popular), Action, and Shooter games are the most popular genres.
# Sports games are popular across all regions

#Market share of genres by region in other words, what percentage of sales in each region does each genre account for?
regional_share = sales.groupby('genre')[['na_sales','pal_sales','jp_sales', 'other_sales']].sum()
regional_share = regional_share.div(regional_share.sum())
regional_share.plot(kind='bar', figsize=(12,6))
plt.title("Genre Market Share by Region")
plt.tight_layout()
plt.show()

#Is there a correlation between critic score and total sales? 
#Does a higher critic score lead to higher sales?
sales[['critic_score','total_sales']].corr()
filtered = sales[['critic_score','total_sales']].dropna()
corr_value = filtered['critic_score'].corr(filtered['total_sales'])
print(corr_value)
sns.regplot(x='critic_score', y='total_sales', data=filtered, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title("Critic Score vs Total Sales")
plt.show()
#Critic score and total sales have a weak positive correlation of 0.28, 
#suggesting that while higher critic scores may be associated with higher sales, 
#there are likely other factors influencing sales as well.

#How have total sales changed over time? Where did the industry peak?
yearly_sales = sales.resample('YE')['total_sales'].sum()
plt.figure(figsize=(12,6))
yearly_sales.plot(color='green')
plt.title("Total Industry Sales Over Time")
plt.show()
#The video game industry has seen significant growth over time, with a notable peak around the early 2010s. 
#After that, there is a slight decline, which could be due to various factors such as market saturation or changes in consumer preferences?

sales.reset_index(inplace=True)
#Create column for year and analyze trends in genre popularity over time.
sales['year'] = pd.to_datetime(sales['release_date']).dt.year
#Total sales by genre and year
genre_trend = (sales.groupby(['year','genre'])['total_sales'].sum().reset_index())
#Pivot table to have years as index, genres as columns, and total sales as values
genre_pivot = genre_trend.pivot(index='year', columns='genre', values='total_sales')
#Top genres by total sales globally
top_genres = (sales.groupby('genre')['total_sales'].sum().sort_values(ascending=False).head(5).index)
top_trends = genre_pivot[top_genres]
#Normalize the trends by dividing each genre's sales by its maximum value to compare growth patterns
normalized = top_trends.div(top_trends.max())

plt.figure(figsize=(12,6))
normalized.plot(ax=plt.gca())
plt.title("Normalized Genre Growth Trends")
plt.ylabel("Relative Growth")
plt.tight_layout()
plt.show()
#We can see that racing games had a significant growth in the early 2000s, while sports games have had more consistent growth over time.