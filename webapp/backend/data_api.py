import datetime

from webapp.backend.data_storage import DataStorage, DataCollection


class DataApi:
    def __init__(self):
        self.data_storage = DataStorage()
        self.data_collection = DataCollection()

    def get_weather_trend_data(self, keyword, geo_code, weather_location, start_date, end_date):
        start_date = start_date if isinstance(start_date, datetime.datetime) else datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_date = end_date if isinstance(end_date, datetime.datetime) else datetime.datetime.combine(end_date, datetime.datetime.min.time())

        missing_weather_ranges = self.data_storage.get_missing_weather_ranges(start_date, end_date, weather_location)
        missing_trend_ranges = self.data_storage.get_missing_trend_ranges(start_date, end_date, geo_code, keyword)
        print(f"Missing trends: {missing_trend_ranges}")
        print(f"Missing weather: {missing_weather_ranges}")

        for s, e in missing_weather_ranges:
            missing_weather = self.data_collection.collect_weekly_weather_data(s, e, weather_location)
            self.data_storage.insert_weather_data(missing_weather, weather_location)
        for s, e in missing_trend_ranges:
            missing_trends = self.data_collection.collect_weekly_trend_data(keyword, s, e, geo_code)
            self.data_storage.insert_trend_data(missing_trends, geo_code, keyword)

        return {
            "weather": self.data_storage.get_weather_data(weather_location, start_date, end_date),
            "trends": self.data_storage.get_trend_data(keyword, geo_code, start_date, end_date)
        }


if __name__ == "__main__":
    LOCATIONS = [
        {
            'name': 'Washington State',
            'geo_code': 'US-WA',
            'w_search': 'washing+dc,wa'
        },
        {
            'name': 'Netherlands',
            'geo_code': 'NL',
            'w_search': 'amsterdam'
        },
        {
            'name': 'UK',
            'geo_code': 'GB',
            'w_search': 'london,united+kingdom'
        },
        {
            'name': 'Spain',
            'geo_code': 'ES',
            'w_search': 'madrid,spain'
        },
        {
            'name': 'Japan',
            'geo_code': 'JP',
            'w_search': 'tokyo,japan'
        },
    ]
    ITEMS = ['raincoat',
             'sandals',
             'umbrella',
             'sun'+'hat',
             'winter'+'coat',
             'skirt', 't-shirt',
             'tights',
             'prom'+'dress']

    search = 'lol'
    geo = 'GB'
    loc = 'London'
    dapi = DataApi()

    end = datetime.date.today() - datetime.timedelta(days=60)
    start = end - datetime.timedelta(weeks=52)

    print(dapi.get_weather_trend_data(search, geo, loc, start, end))


    # TODO: Need mappings between geo code for trend --> name for weather
    # for location in LOCATIONS:
    #     search.append(location['w_search'])
    #     geo.append(location['geo_code'])
