# 🎮 Video Game Sales Analysis

Welcome to my video game sales analysis project. I'll show how I used Python to explore over 64,000 video game records from Kaggle. We'll cover everything from loading the data to generating insights and visualizations. By the end, you'll see how to perform a complete exploratory data analysis (EDA) on a real-world dataset.

---

## 📖 Table of Contents
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Setup & Requirements](#setup--requirements)
- [Step 1: Load and Explore the Data](#step-1-load-and-explore-the-data)
- [Step 2: Top and Bottom Games](#step-2-top-and-bottom-games)
- [Step 3: Working with Dates](#step-3-working-with-dates)
- [Step 4: Global Sales by Genre](#step-4-global-sales-by-genre)
- [Step 5: Platform Performance](#step-5-platform-performance)
- [Step 6: Regional Sales Analysis](#step-6-regional-sales-analysis)
- [Step 7: Genre Popularity by Region](#step-7-genre-popularity-by-region)
- [Step 8: Critic Score vs. Sales](#step-8-critic-score-vs-sales)
- [Step 9: Sales Over Time (Industry Trend)](#step-9-sales-over-time-industry-trend)
- [Step 10: Genre Trends Over Time](#step-10-genre-trends-over-time)
- [Key Insights](#key-insights)

---

## Introduction
As a sophomore interested in data analytics, I wanted to work on a project that combined my love for video games with real data skills. This project analyzes video game sales data from the 1970s to 2024, answering questions like:
- Which genres sell the most globally?
- How do different platforms compare?
- What are the regional preferences (NA, PAL, Japan, etc.)?
- Do critic scores actually drive sales?
- How has the industry evolved over time?

I used Python with **pandas** for data manipulation, **matplotlib** and **seaborn** for visualizations. The result is a series of charts and insights that tell the story of the video game market.

---

## Dataset
The data comes from [Kaggle](https://www.kaggle.com/datasets/siddharth0935/video-game-sales) It includes:
- `title`: Game name
- `console`: Platform (e.g., PS4, Xbox, Nintendo Switch)
- `genre`: Game genre (Action, Sports, RPG, etc.)
- `publisher`: Company that published the game
- `release_date`: Date the game was released
- `critic_score`: Metacritic score (if available)
- `total_sales`: Global sales in millions
- Regional sales: `na_sales`, `pal_sales` (Europe/Africa), `jp_sales`, `other_sales`

## Setup & Requirements
Make sure you have Python 3.8+ installed. Then install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn
```

## Step 1: Load and Explore the Data

We start by importing libraries and loading the CSV.

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sales = pd.read_csv('vgchartz-2024.csv')
```
--
```
sales.head()
pd.isnull(sales).sum()   # Check missing values
sales.info()              # Data types and non-null counts
```
Here we identify null values and get a overview of the dataset

## Step 2: Top and Bottom Games

We sort by `total_sales` to see the least and most popular games.

Least popular (bottom 10):

```
x = sales.sort_values('total_sales', ascending=True).head(10)
x[['title', 'total_sales']]
```

Most popular (top 10):

```
y = sales[sales['total_sales'] > 10].sort_values('total_sales', ascending=False).head(10)
y[['title', 'total_sales', 'console', 'critic_score']]
```

## Step 3: Working with Dates

To analyze trends over time, we need proper datetime handling.

```
# Set release_date as the index
sales.set_index('release_date', inplace=True)
sales.index = pd.to_datetime(sales.index, format='mixed', errors='coerce')
sales.head()
```

Now the index is a datetime, which enables resampling and time-based slicing.

We also look at a specific row to confirm:

```
sales[['title']].iloc[7]
```

## Step 4: Global Sales by Genre

We group by genre and sum total sales, then plot a horizontal bar chart.

```
genre_sales = sales.groupby('genre')['total_sales'].sum().sort_values(ascending=True)

plt.figure(figsize=(10,8))
genre_sales.plot(kind='barh', color=sns.color_palette("mako", len(genre_sales)))
plt.title("Total Global Sales by Genre")
plt.xlabel("Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()
```
Insight: Sports games lead, followed by Action and Shooter. This makes sense given the popularity of annual franchises like FIFA and Call of Duty.

## Step 5: Platform Performance

We compare platforms by total revenue and average sales per game. We visualize this use horizontal bar charts. 

Total revenue per platform (top 15):

```
platform_total = sales.groupby('console')['total_sales'].sum().sort_values(ascending=False).head(15).sort_values(ascending=True)

plt.figure(figsize=(10,6))
platform_total.plot(kind='barh', color=sns.color_palette("mako", len(platform_total)))
plt.title("Total Global Revenue by Platform")
plt.xlabel("Total Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()
```

Average sales per game (top 15):

```
platform_avg = sales.groupby('console')['total_sales'].mean().sort_values(ascending=False).head(15).sort_values(ascending=True)

plt.figure(figsize=(10,6))
platform_avg.plot(kind='barh', color=sns.color_palette("mako", len(platform_avg)))
plt.title("Average Sales Per Game by Platform")
plt.xlabel("Average Sales (Millions)")
plt.ylabel("")
plt.tight_layout()
plt.show()
```

Observation: PlayStation consoles dominate in total revenue, but Nintendo platforms (like N64, GameCube) have higher average sales per game. This suggests Nintendo releases fewer titles but each becomes a blockbuster, while PlayStation has a larger library with more varied success.


## Step 6: Regional Sales Analysis

Which region buys the most games overall?

```
regional_totals = sales[['na_sales','pal_sales','jp_sales','other_sales']].sum()

plt.figure(figsize=(8,6))
regional_totals.plot(kind='bar', color=sns.color_palette("mako", len(regional_totals)))
plt.title("Total Video Game Sales by Region")
plt.ylabel("Sales (Millions)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

```

Result: North America is the largest market, followed by PAL (Europe/Africa), Japan, and then other regions.

## Step 7: Genre Popularity by Region

Do different regions prefer different genres? We loop through each region and plot the top 8 genres.

```
regions = ['na_sales','pal_sales','jp_sales', 'other_sales']
for region in regions:
    top_genres = sales.groupby('genre')[region].sum().sort_values(ascending=False).head(8).sort_values()
    plt.figure(figsize=(8,6))
    top_genres.plot(kind='barh', color=sns.color_palette("mako", len(top_genres)))
    plt.title(f"Top Genres in {region.upper()}")
    plt.xlabel("Sales (Millions)")
    plt.tight_layout()
    plt.show()

```

Key findings:

NA & PAL: Sports, Action, Shooter dominate.

Japan: Role-Playing (RPG) is #1, with Action and Sports also popular.

Other regions: Similar to NA/PAL.

We also compute market share percentages:

```
regional_share = sales.groupby('genre')[['na_sales','pal_sales','jp_sales','other_sales']].sum()
regional_share = regional_share.div(regional_share.sum())
regional_share.plot(kind='bar', figsize=(12,6))
plt.title("Genre Market Share by Region")
plt.tight_layout()
plt.show()
```

This confirms that certain regions like certain genres more than others. For example, Japan seems to enjoy RPGs more than any other genre

## Step 8: Critic Score vs. Sales

Is there a correlation between critic scores and total sales?

```
filtered = sales[['critic_score','total_sales']].dropna()
corr_value = filtered['critic_score'].corr(filtered['total_sales'])
print(f"Correlation: {corr_value:.2f}")

sns.regplot(x='critic_score', y='total_sales', data=filtered, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title("Critic Score vs Total Sales")
plt.show()
```

Result: A weak positive correlation of about 0.28. So while good reviews help, they aren't the main driver—franchise popularity, marketing, and release timing likely matter more.

## Step 9: Sales over Time (Industry trend)

We use the datetime index to resample by year and sum total sales.

```
yearly_sales = sales.resample('YE')['total_sales'].sum()

plt.figure(figsize=(12,6))
yearly_sales.plot(color='green')
plt.title("Total Industry Sales Over Time")
plt.show()
```

Insight: The industry grew steadily, peaked around the early 2010s, then slightly declined. This may reflect the console cycle (PS3/Xbox 360/Wii era) and market saturation.

## Step 10: Genre Trends Over Time

To see how each genre's popularity evolved, we need to reset the index and extract the year.

```
sales.reset_index(inplace=True)
sales['year'] = pd.to_datetime(sales['release_date']).dt.year
```

Then we group by year and genre, pivot, and focus on the top 5 genres globally.

```
genre_trend = sales.groupby(['year','genre'])['total_sales'].sum().reset_index()
genre_pivot = genre_trend.pivot(index='year', columns='genre', values='total_sales')

top_genres = sales.groupby('genre')['total_sales'].sum().sort_values(ascending=False).head(5).index
top_trends = genre_pivot[top_genres]

# Normalize to compare growth patterns
normalized = top_trends.div(top_trends.max())

plt.figure(figsize=(12,6))
normalized.plot(ax=plt.gca())
plt.title("Normalized Genre Growth Trends")
plt.ylabel("Relative Growth")
plt.tight_layout()
plt.show()
```
Observation: Racing games had a notable surge in the early 2000s, while Sports games show steady, consistent growth. This normalization lets us compare genres with very different sales volumes.

## Key Insights

Sports games are universally popular, but Japan has a unique appetite for RPGs.

PlayStation leads in total revenue; Nintendo excels in average sales per game.

North America is the biggest market, followed by PAL and Japan.

Critic scores have a weak correlation with sales—other factors like brand and marketing are crucial.

The industry peaked in the early 2010s, possibly tied to the last major console cycle.

Racing games spiked in the 2000s, while Sports games have remained consistently strong.



