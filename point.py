# point.py
# 2022-08-18
# Tian Zhenshiyi

class Point():
    def __init__(self, longitude, latitude, tc_id = None):
        self.x = longitude
        self.y = latitude
        self.name = tc_id