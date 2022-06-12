from pandas.core.indexes.base import Index
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, url_for, redirect, render_template

app=Flask(__name__)

@app.route('/')
def hompage():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def runProg():
    try:
        cntry1=request.form.get('urlName1')
        cntry2=request.form.get('urlName2')
        params = {
           'access_key': '362cc1a8c6813f1ed397dc8e8d1a65a5',
           'query': cntry1
        }
        country1 = requests.get('http://api.weatherstack.com/current', params)
        with open('static/data/c1.json', 'wb') as c1:
            for content1 in country1.iter_content():
                c1.write(content1)


        params = {
            'access_key': '362cc1a8c6813f1ed397dc8e8d1a65a5',
            'query': cntry2
        }

        country2 = requests.get('http://api.weatherstack.com/current', params)
        with open('static/data/c2.json', 'wb') as c2:
            for content2 in country2.iter_content():
                c2.write(content2)

        df1=pd.read_json('static/data/c1.json')
        df2=pd.read_json('static/data/c2.json')
    
        df1=df1.drop(columns=['request', 'location'])
        df1noT=df1.drop(['observation_time', 'weather_code', 'weather_icons', 'weather_descriptions', 'wind_dir', 'is_day', 'wind_degree', 'cloudcover', 'precip', 'feelslike', 'pressure'])
        df1noT=df1noT.dropna()
        df1Time=str(df1.loc['observation_time', 'current'])

        df2=df2.drop(columns=['request', 'location'])
        df2noT=df2.drop(['observation_time', 'weather_code', 'weather_icons', 'weather_descriptions', 'wind_dir', 'is_day', 'wind_degree', 'cloudcover', 'precip', 'feelslike', 'pressure'])
        df2noT=df2noT.dropna()
        df2Time=str(df2.loc['observation_time', 'current'])

        df=pd.merge(df1noT, df2noT, left_index=True, right_index=True, suffixes=['_1', '_2'])
        df=df.rename(columns={df.columns[0]: cntry1, df.columns[1]: cntry2})
        df=df.pivot_table(columns=['temperature', 'wind_speed', 'humidity', 'uv_index', 'visibility'], values=[cntry1, cntry2])
        df=df.melt(ignore_index=False)
        print(df)


        fig, ax=plt.subplots()
        sns.set_palette(sns.color_palette("Paired"))
        sns.barplot(x='variable', y='value', hue=df.index, data=df)
        plt.ylim(min(df['value']), max(df['value']))
        ax.bar_label(ax.containers[0])
        ax.bar_label(ax.containers[1])
        plt.title('Weather Comparison of two Countries')
        plt.ylabel('Measurements')
        plt.legend()
        plt.savefig('static/graph/count1.png')

        return render_template('index.html', df1Time=df1Time, df2Time=df2Time, cntry1=cntry1, cntry2=cntry2)

    except:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)