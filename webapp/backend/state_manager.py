import datetime
import time

from webapp.backend.data_api import DataApi


class StateManager:
    def __init__(self):
        self.__data_api = DataApi()
        self.__current_user = None
        self.__current_search = None
        self.__current_search_data = None

    def set_search(self, search):
        self.__current_search = search

    def reset_search(self):
        self.__current_search = None

    def get_search(self):
        return self.__current_search

    def authenticate_user(self, user):
        self.__current_user = user

    def deauthenticate_user(self):
        self.__current_user = None

    def is_authenticated(self):
        return self.__current_user is not None

    def get_user(self):
        return self.__current_user

    def execute_search(self, term, geo, loc):
        end = datetime.date.today() - datetime.timedelta(weeks=2)
        start = end - datetime.timedelta(weeks=52 * 5)

        five_years = self.__data_api.get_weather_trend_data(term, geo, loc, start, end)
        one_year = {
            'weather': five_years['weather'][-52:],
            'trends': five_years['trends'][-52:]
        }

        self.__current_search_data = {
            "1y": one_year,
            "5y": five_years
        }

    def get_current_search_data(self):
        return self.__current_search_data

    def time(self):
        return time.time()

