from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Episode,Guest,Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stella:Stellanjambi8652#@localhost/appearances'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Episodes(Resource):

    def get(self):
        response_dict_list=[n.to_dict(only=("id","date","number")) for n in Episode.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

api.add_resource(Episodes, '/episodes')

class EpisodeByID(Resource):

    def get(self, id):
        
        response_dict = Episode.query.filter_by(id=id).first().to_dict(only=( "id","date","number","appearances"))
        if response_dict==None:
         response=make_response(
            {
            "error":'Episode not found'
           },404)
        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(EpisodeByID, '/episodes/<int:id>')

class Guests(Resource):

    def get(self):
        response_dict_list=[n.to_dict(only=("id","name","occupation")) for n in Guest.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

api.add_resource(Guests, '/guests')


class Appearances(Resource):
    def post(self):
        data = request.get_json()
        rating = data.get("rating")
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Validate input data
        if rating is None or episode_id is None or guest_id is None:
            return make_response({"errors": ["Validation errors: 'rating', 'episode_id', and 'guest_id' are required."]}, 400)

       
        episode = Episode.query.filter(Episode.id == episode_id).first()
        guest = Guest.query.filter(Guest.id == guest_id).first()

        if not episode or not guest:
            return make_response({"errors": ["Validation errors: 'episode' or 'guest' not found."]}, 404)

        try:
            
            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )

            db.session.add(new_appearance)
            db.session.commit()

           
            appearance_data = {
                "id": new_appearance.id,
                "rating": new_appearance.rating,  
                "guest_id": new_appearance.guest_id,
                "episode_id": new_appearance.episode_id,
                "episode": episode.to_dict(only=("date", "id", "number")),
                "guest": guest.to_dict(only=("id", "name", "occupation"))
            }

            response = make_response(appearance_data, 201)
            return response

        except Exception as e:
           
            db.session.rollback()
            return make_response({"errors": [str(e)]}, 500)


api.add_resource(Appearances, '/appearances')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
