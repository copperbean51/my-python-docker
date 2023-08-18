# -*- coding:utf-8 -*-
import requests
import json
from pathlib import Path


def get_weather_info(code: str) -> None:
    # 気象庁データの取得
    jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/" + str(area_code) + ".json"
    jma_json = requests.get(jma_url).json()

    # 取得したいデータを選ぶ
    jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    jma_wind = jma_json[0]["timeSeries"][0]["areas"][0]["winds"][0]

    # 全角スペースの削除
    jma_weather = jma_weather.replace('　', '')
    jma_wind = jma_wind.replace('　', '')

    print("Date :    ", jma_date)
    print("Weather : ", jma_weather)
    print("Wind :    ", jma_wind)

if __name__=="__main__":
    area_code = 130000
    get_weather_info(area_code)
