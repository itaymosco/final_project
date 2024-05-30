from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import os
 
def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://root:root@mongo:27017/recommendations_db?authSource=admin")
    mongo = PyMongo(app)
 
    @app.route('/')
    def index():
        preferences = mongo.db.preferences.find()
        recommendations = mongo.db.recommendations.find()
        return render_template('index.html', preferences=list(preferences), recommendations=list(recommendations))
 
    @app.route('/add', methods=['POST'])
    def add_preference():
        user_id = request.form.get('user_id')
        category = request.form.get('category')
        preference = request.form.get('preference')
 
        new_preference = {"user_id": user_id, "category": category, "preference": preference}
        mongo.db.preferences.insert_one(new_preference)
 
        generate_recommendations(user_id, category, preference)
 
        return redirect(url_for('index'))
 
    def generate_recommendations(user_id, category, preference):
        similar_items = [preference + " 1", preference + " 2", preference + " 3"]
        for item in similar_items:
            new_recommendation = {"user_id": user_id, "recommendation": item}
            mongo.db.recommendations.insert_one(new_recommendation)
 
    return app
 
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 


