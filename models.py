from flask_pymongo import PyMongo

mongo = PyMongo()

class Preference:
    def __init__(self, user_id, category, preference):
        self.user_id = user_id
        self.category = category
        self.preference = preference

class Recommendation:
    def __init__(self, user_id, recommendation):
        self.user_id = user_id
        self.recommendation = recommendation


