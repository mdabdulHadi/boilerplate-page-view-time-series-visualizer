import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",
                 parse_dates=["date"],
                 index_col="date")


# Clean data
def clean_data():
  # Calculate the limits for top and bottom 2.5% of the data
  lower_lim = df["value"].quantile(0.025)
  upper_lim = df["value"].quantile(0.975)

  # Filter the data to remove values outside the limits
  df_cleaned = df[(df["value"] >= lower_lim) & (df["value"] <= upper_lim)]

  # Print the number of rows in the cleaned DataFrame
  print("Number of rows in the cleaned DataFrame:", df_cleaned.shape[0])

  return df_cleaned


def draw_line_plot():
  # Clean data
  df_cleaned = clean_data()

  # Draw line plot
  fig, ax = plt.subplots(figsize=(15, 5))
  ax.plot(df_cleaned.index, df_cleaned["value"], color="r")
  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  ax.set_xlabel("Date")
  ax.set_ylabel("Page Views")

  # Save image and return fig
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Clean data
  df_cleaned = clean_data()

  # Copy and modify data for monthly bar plot
  df_bar = df_cleaned.copy()
  df_bar["year"] = df_bar.index.year
  df_bar["month"] = df_bar.index.month_name()

  # Group data by year and month, calculate the mean of page views
  df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

  # Reorder the months to display Jan to Dec
  months = [
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"
  ]
  df_bar = df_bar.reindex(columns=months)

  # Draw bar plot
  fig, ax = plt.subplots(figsize=(12, 6))
  df_bar.plot(kind="bar", ax=ax)
  ax.set_xlabel("Years")
  ax.set_ylabel("Average Page Views")
  ax.legend(title="Months", labels=months, loc="upper left")

  # Save image and return fig
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Clean data
  df_cleaned = clean_data()

  # Prepare data for box plots
  df_box = df_cleaned.copy()
  df_box.reset_index(inplace=True)
  df_box["year"] = [d.year for d in df_box.date]
  df_box["month"] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  fig, axes = plt.subplots(1, 2, figsize=(20, 8))

  sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
  axes[0].set_xlabel("Year")
  axes[0].set_ylabel("Page Views")
  axes[0].set_title("Year-wise Box Plot (Trend)")

  sns.boxplot(x="month",
              y="value",
              data=df_box,
              ax=axes[1],
              order=[
                "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                "Oct", "Nov", "Dec"
              ])
  axes[1].set_xlabel("Month")
  axes[1].set_ylabel("Page Views")
  axes[1].set_title("Month-wise Box Plot (Seasonality)")

  # Save image and return fig
  fig.savefig('box_plot.png')
  return fig
