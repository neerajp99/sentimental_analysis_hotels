import plotly.graph_objects as go
import pandas as pd

# Read csv data
dataFrame = pd.read_csv("kuala_lumpur.csv")
# Create initial arrays for hotels score
actual_hotel_score = list()
polarity_hotel_score = list()
base_content = list()

# Append the data to the lists
dataFrame1 = dataFrame['V1']
for i in dataFrame1:
    actual_hotel_score.append(i)

dataFrame2 = dataFrame['V2']
for i in dataFrame2:
    polarity_hotel_score.append(i)

for i in range(1, len(dataFrame1) + 1):
    base_content.append("H" + str(i))


fig = go.Figure()
fig.add_trace(go.Bar(x=base_content,
                y = actual_hotel_score,
                name = 'Actual Score',
                marker_color='rgb(55, 83, 109)'
                ))
fig.add_trace(go.Bar(x=base_content,
                y = polarity_hotel_score,
                name = 'Score Calculated',
                marker_color='rgb(26, 118, 255)'
                ))

fig.update_layout(
    title='Analysis of Kuala Lumpur Hotels Ratings',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Ratings',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    autosize = False,
    width = 800,
    height = 800,
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()