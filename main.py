import streamlit as st
import pandas as pd
from matplotlib import dates
from matplotlib.patches import Patch
import matplotlib.pyplot as plt

st.title('Teamhood tech')
tech_numbers_file = st.file_uploader('Upload tech numbers file', type=['xlsx'])
if tech_numbers_file is not None:
  df = pd.read_excel(tech_numbers_file, sheet_name='Sheet1')
  df = df.iloc[:, [0, 1, 2, 3, 4]]
  df.columns = ['Date', 'TotalErrors', 'FailedCommands', 'FailedPercent', 'TotalCommands']
  df['Date'] = pd.to_datetime(df['Date'])
  df['Date'] = pd.date_range(end=df.iloc[-1]['Date'], periods=len(df), freq="W-WED", inclusive='both')
  df = df.set_index('Date').sort_index()

  df['FailedPercent'] = (df['FailedCommands'] * 100) / df['TotalCommands']
  df['MovingAverage'] = df['FailedPercent'].rolling(4*3, center=False).mean()
  df = df[-28:]
  bg_color = '#333333'
  text_color = '#e2e2e2'

  fig = plt.figure(figsize=(14, 7.5))

  ax = fig.add_subplot(111)

  ax.grid(axis='y', color=text_color, alpha=0.2, zorder=-1.0)

  ax.plot(df['FailedPercent'], color="w", linewidth=0, zorder=1)
  ax.plot(df['MovingAverage'], color="orange")

  ax.set_facecolor(bg_color)
  fig.patch.set_facecolor(bg_color)
  ax.spines['left'].set_color(bg_color)
  ax.spines['bottom'].set_color(bg_color)
  ax.spines['top'].set_color(bg_color)
  ax.spines['right'].set_color(bg_color)
  ax.tick_params(axis='x', colors=text_color)
  ax.tick_params(axis='y', colors=text_color)
  ax.yaxis.tick_right()
  ax.fill_between(df.index, df['FailedPercent'], 0.1, where=(df['FailedPercent'] > 0.1), facecolor="crimson", interpolate=True, zorder=1)
  ax.fill_between(df.index, df['FailedPercent'], 0.1, where=(df['FailedPercent'] <= 0.1), facecolor="limegreen", interpolate=True, zorder=1)
  ax.xaxis.set_major_locator(dates.MonthLocator(bymonthday=1))
  ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%b'))
  ax.text(0.82, 0.96, 'Total commands: ' + f'{df["TotalCommands"].tail(1).values[0]:,}'.replace(',', ' '), transform=ax.transAxes, color=text_color)
  pa1 = Patch(facecolor='limegreen')
  pa2 = Patch(facecolor='crimson')
  pb1 = Patch(facecolor='orange')
  ax.legend(handles=[pa1, pb1, pa2, pb1], labels=['', '','Failed commands (%)', 'Rolling average (3 months)'], loc='lower left', ncol=2, handletextpad=0.5, handlelength=1.0, columnspacing=-0.5)

  plt.title('Failed commands', color=text_color)
  plt.savefig('./tech_output.png',  bbox_inches='tight')
  st.pyplot(fig)

  with open('./tech_output.png', 'rb') as f:
    st.download_button(
      label='Download chart',
      data=f,
      file_name='tech_output.png',
      mime='image/png'
    )