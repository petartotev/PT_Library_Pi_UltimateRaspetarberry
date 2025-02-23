import pandas as pd  # Import the pandas library for data manipulation and analysis
import matplotlib.pyplot as plt  # Import the matplotlib library for plotting graphs

point_values_visualized = False;

# Define a function to analyze air quality
def analyze_air_quality(date_from=None, date_to=None):
    # Step 1: Load the air quality data from a CSV file using pandas
    # 'Date (EEST)' is the column containing the date of the data, which will be parsed as datetime
    df = pd.read_csv('../input/air_quality_data.csv', parse_dates=['Date (EEST)'])
    
    # Convert the 'Date (EEST)' column into a pandas datetime object and set it as the index of the DataFrame
    df['Date'] = pd.to_datetime(df['Date (EEST)'])
    df.set_index('Date', inplace=True)  # This makes the 'Date' column the index of the dataframe

    # Step 2: Check if date_from and date_to were provided by the user
    # If not, use the first and last dates from the data as the default date range
    if not date_from or not date_to:
        # Get the minimum (earliest) and maximum (latest) dates from the dataframe
        date_from = df.index.min().strftime('%Y-%m-%d')
        date_to = df.index.max().strftime('%Y-%m-%d')

    # Step 3: Filter the dataframe to include only the rows within the given date range
    df = df.loc[date_from:date_to]

    # Step 4: Define PM2.5 ranges and their associated colors for visualization
    # These ranges correspond to different levels of air quality based on PM2.5 concentration
    pm25_ranges = [
        (0, 9, 'green'),               # Good (0.0 to 9.0)
        (9, 35.4, 'yellow'),           # Moderate (9.0 to 35.4)
        (35.4, 55.4, 'orange'),        # Unhealthy for sensitive groups (35.4 to 55.4)
        (55.4, 125.4, 'red'),          # Unhealthy (55.4 to 125.4)
        (125.4, 225.4, 'darkred'),     # Very unhealthy (125.4 to 225.4)
        (225.4, 500, 'purple')         # Hazardous (225.4 to 500)
    ]

    # Step 5: Define the corresponding labels for each PM2.5 range (for the legend)
    pm25_range_labels = [
        'Good: 0.0 – 9.0',
        'Moderate: 9.0 – 35.4',
        'Unhealthy for sensitive groups: 35.4 – 55.4',
        'Unhealthy: 55.4 – 125.4',
        'Very unhealthy: 125.4 – 225.4',
        'Hazardous: 225.4 – 500'  # Renamed "Purple (Hazardous)" to just "Hazardous"
    ]

    # Step 6: Define a function to determine the color based on the PM2.5 value
    def get_pm25_color(value):
        for low, high, color in pm25_ranges:
            if low <= value < high:
                return color
        return 'gray'  # If the value doesn't fit any range, return 'gray'

    # Apply the color function to the 'PM2.5 [µg/m³]' column to create a new 'PM2.5 Color' column
    df['PM2.5 Color'] = df['PM2.5 [µg/m³]'].apply(get_pm25_color)

    # Step 7: Plot the Temperature data (red line for temperature values)
    plt.figure(figsize=(10, 6))  # Set the figure size (10 inches by 6 inches)
    plt.plot(df.index, df['Temperature [°C]'], color='red', zorder=1)  # Plot the temperature data (line)
    plt.scatter(df.index, df['Temperature [°C]'], color='red', s=8, zorder=2)  # Add scatter points on top of the line

    # Background coloring for temperature ranges
    plt.axhspan(-100, 18, facecolor='red', alpha=0.10, zorder=0)      # Below 18°C: Red
    plt.axhspan(18, 24, facecolor='green', alpha=0.10, zorder=0)      # 18°C to 24°C: Green
    plt.axhspan(24, 100, facecolor='orange', alpha=0.10, zorder=0)    # Above 24°C: Orange

    # Find the maximum and minimum temperature values and their corresponding dates
    max_temp = df['Temperature [°C]'].max()
    min_temp = df['Temperature [°C]'].min()
    max_temp_idx = df['Temperature [°C]'].idxmax()
    min_temp_idx = df['Temperature [°C]'].idxmin()

    # Add annotations for the maximum and minimum temperature values
    plt.scatter(max_temp_idx, max_temp, color='black', s=16, zorder=3)
    plt.scatter(min_temp_idx, min_temp, color='black', s=16, zorder=3)

    # Step 8: Annotate each point in the temperature plot with its value (above the point)
    if point_values_visualized:
        for i, v in enumerate(df['Temperature [°C]']):
            plt.text(df.index[i], v + 0.3, f'{v:.2f}', ha='center', fontsize=8, rotation=90, verticalalignment='bottom')

    # Step 9: Set plot title, labels, and formatting
    plt.title(f'Temperature Over Time')  # Title of the plot
    plt.xlabel('Date')  # Label for the x-axis
    plt.ylabel('Temperature [°C]')  # Label for the y-axis
    plt.xticks(rotation=90)  # Rotate x-axis labels to make them readable
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M'))  # Format the date labels
    plt.ylim(df['Temperature [°C]'].min() - 5, df['Temperature [°C]'].max() + 5)  # Set y-axis limits with a little padding

    # Make the layout tight (avoid clipping of labels and titles)
    plt.tight_layout()

    # Save the plot as an image with the filename based on the date range
    plt.savefig(f'{date_from}_{date_to}_temperature_diagram.png')
    plt.clf()  # Clear the current plot to avoid overlap with the next one

    # Step 10: Plot the Humidity data (cyan line for humidity values)
    plt.figure(figsize=(10, 6))  # Set the figure size (10 inches by 6 inches)
    plt.plot(df.index, df['Humidity [%]'], color='cyan', zorder=1)  # Plot the humidity data (line)
    plt.scatter(df.index, df['Humidity [%]'], color='cyan', s=8, zorder=2)  # Add scatter points on top of the line

    # Background coloring for humidity ranges
    plt.axhspan(0, 40, facecolor='orange', alpha=0.10, zorder=0)   # 0 - 40: Orange
    plt.axhspan(40, 60, facecolor='green', alpha=0.10, zorder=0)   # 40 - 60: Green
    plt.axhspan(60, 100, facecolor='red', alpha=0.10, zorder=0)    # 60 - 100: Red

    # Find the maximum and minimum humidity values and their corresponding dates
    max_humidity = df['Humidity [%]'].max()
    min_humidity = df['Humidity [%]'].min()
    max_humidity_idx = df['Humidity [%]'].idxmax()
    min_humidity_idx = df['Humidity [%]'].idxmin()

    # Add annotations for the maximum and minimum humidity values
    plt.scatter(max_humidity_idx, max_humidity, color='black', s=16, zorder=3)
    plt.scatter(min_humidity_idx, min_humidity, color='black', s=16, zorder=3)

    # Step 11: Annotate each point in the humidity plot with its value (above the point)
    if point_values_visualized:
        for i, v in enumerate(df['Humidity [%]']):
            plt.text(df.index[i], v + 0.3, f'{v:.2f}', ha='center', fontsize=8, rotation=90, verticalalignment='bottom')

    # Step 12: Set plot title, labels, and formatting for humidity
    plt.title(f'Humidity Over Time')
    plt.xlabel('Date')
    plt.ylabel('Humidity [%]')
    plt.xticks(rotation=90)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.ylim(df['Humidity [%]'].min() - 10, df['Humidity [%]'].max() + 10)  # Set y-axis limits

    # Make the layout tight (avoid clipping of labels and titles)
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(f'{date_from}_{date_to}_humidity_diagram.png')
    plt.clf()

    # Step 13: Plot the PM2.5 data with background colors representing air quality ranges
    plt.figure(figsize=(10, 6))  # Set the figure size (10 inches by 6 inches)
    plt.plot(df.index, df['PM2.5 [µg/m³]'], color='lime', zorder=1)  # Plot the PM2.5 data (line)
    plt.scatter(df.index, df['PM2.5 [µg/m³]'], color='lime', s=8, zorder=2)  # Add scatter points on top of the line

    # Find the maximum and minimum PM2.5 values and their corresponding dates
    max_pm25 = df['PM2.5 [µg/m³]'].max()
    min_pm25 = df['PM2.5 [µg/m³]'].min()
    max_pm25_idx = df['PM2.5 [µg/m³]'].idxmax()
    min_pm25_idx = df['PM2.5 [µg/m³]'].idxmin()

    # Add annotations for the maximum and minimum PM2.5 values
    plt.scatter(max_pm25_idx, max_pm25, color='black', s=16, zorder=3)
    plt.scatter(min_pm25_idx, min_pm25, color='black', s=16, zorder=3)

    # Add colored background bands for the PM2.5 ranges
    for low, high, color in pm25_ranges:
        plt.axhspan(low, high, facecolor=color, alpha=0.1, zorder=0)

    # Step 14: Annotate each point in the PM2.5 plot with its value (above the point)
    if point_values_visualized:
        for i, v in enumerate(df['PM2.5 [µg/m³]']):
            plt.text(df.index[i], v + 0.3, f'{v:.2f}', ha='center', fontsize=8, rotation=90, verticalalignment='bottom')

    # Step 15: Set plot title, labels, and formatting for PM2.5
    plt.title(f'PM2.5 Over Time')
    plt.xlabel('Date')
    plt.ylabel('PM2.5 [µg/m³]')
    plt.xticks(rotation=90)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.ylim(df['PM2.5 [µg/m³]'].min() - 10, df['PM2.5 [µg/m³]'].max() + 10)

    # Make the layout tight (avoid clipping of labels and titles)
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(f'{date_from}_{date_to}_dust_pm25_diagram.png')
    plt.clf()

    # Step 16: Create a pie chart to visualize the distribution of PM2.5 levels across the defined ranges
    range_counts = [((df['PM2.5 [µg/m³]'] >= low) & (df['PM2.5 [µg/m³]'] < high)).sum() for low, high, _ in pm25_ranges]
    range_colors = [color for _, _, color in pm25_ranges]  # Get the colors for each PM2.5 range

    plt.figure(figsize=(8, 8))  # Square figure
    wedges, texts, autotexts = plt.pie(range_counts, labels=pm25_range_labels, autopct='%1.1f%%', startangle=90, colors=range_colors)

    # Step 17: Add a title to the pie chart and adjust its layout to make it look clean
    plt.title(f'PM2.5 Distribution by Range')

    # Adjust the pie chart positioning to avoid overlapping
    plt.subplots_adjust(top=0.8, bottom=0.2)  # Adjusted for better spacing

    # Add a centered legend below the pie chart
    plt.legend(wedges, pm25_range_labels, title="PM2.5 Ranges", loc="center", bbox_to_anchor=(0.5, -0.45), ncol=2)

    # Adjust the text properties for better readability
    for text in texts:
        text.set_fontsize(10)
        text.set_horizontalalignment('center')

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_horizontalalignment('center')

    # Remove the unwanted overlapping text
    plt.setp(texts, visible=False)

    # Save the pie chart as an image
    plt.tight_layout()
    plt.savefig(f'{date_from}_{date_to}_dust_pm25_chart_pie.png')
    plt.clf()

    # Print the filenames of the saved images
    print("Images saved as:")
    print(f"{date_from}_{date_to}_dust_pm25_chart_pie.png")
    print(f"{date_from}_{date_to}_dust_pm25_diagram.png")
    print(f"{date_from}_{date_to}_humidity_diagram.png")
    print(f"{date_from}_{date_to}_temperature_diagram.png")

    # Step 18: Calculate summary statistics
    temperature_stats = df['Temperature [°C]'].agg(['average', 'min', 'max', 'median'])
    humidity_stats = df['Humidity [%]'].agg(['average', 'min', 'max', 'median'])
    pm25_stats = df['PM2.5 [µg/m³]'].agg(['average', 'min', 'max', 'median'])

    # Print the summary in the console
    print(f"\nSummary Statistics ({date_from} to {date_to}):")
    print(f"Temperature [°C]:\n{temperature_stats}")
    print(f"Humidity [%]:\n{humidity_stats}")
    print(f"PM2.5 [µg/m³]:\n{pm25_stats}")

    # Save the summary to a text file
    summary_filename = f'{date_from}_{date_to}_summary_statistics.txt'
    with open(summary_filename, 'w') as f:
        f.write(f"Summary Statistics ({date_from} to {date_to}):\n\n")
        f.write(f"Temperature [°C]:\n{temperature_stats.to_string()}\n\n")
        f.write(f"Humidity [%]:\n{humidity_stats.to_string()}\n\n")
        f.write(f"PM2.5 [µg/m³]:\n{pm25_stats.to_string()}\n")

    print(f"Summary statistics saved as: {summary_filename}")

    # Optional: Display summary as a table using matplotlib
    fig, ax = plt.subplots(figsize=(7, 4))  # Slightly wider figure
    ax.axis('tight')
    ax.axis('off')

    table_data = [
        ["Metric", "Average", "Min", "Max", "Median"],
        ["Temperature [°C]", f"{temperature_stats['average']:.2f}", f"{temperature_stats['min']:.2f}", f"{temperature_stats['max']:.2f}", f"{temperature_stats['median']:.2f}"],
        ["Humidity [%]", f"{humidity_stats['average']:.2f}", f"{humidity_stats['min']:.2f}", f"{humidity_stats['max']:.2f}", f"{humidity_stats['median']:.2f}"],
        ["PM2.5 [µg/m³]", f"{pm25_stats['average']:.2f}", f"{pm25_stats['min']:.2f}", f"{pm25_stats['max']:.2f}", f"{pm25_stats['median']:.2f}"],
    ]

    table = ax.table(cellText=table_data, loc='center', cellLoc='center', colLabels=None, bbox=[0, -0.2, 1, 1.2])  # Stretch the height a bit
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Adjust column widths to prevent tight first column
    for i in range(5):
        table.auto_set_column_width(i)

    # Add a title above the table
    plt.title(f'Summary Statistics ({date_from} to {date_to})', fontsize=12, pad=10)

    # Save the table as an image
    summary_table_filename = f'{date_from}_{date_to}_summary_table.png'
    plt.savefig(summary_table_filename, bbox_inches='tight', pad_inches=0.5)
    plt.clf()

    print(f"Summary table saved as: {summary_table_filename}")


# Step 19: Example usage of the function to analyze air quality
# Call the function without specifying dates to use the dataset's full date range
#analyze_air_quality(date_from='2025-02-16', date_to='2025-02-22')
analyze_air_quality()
