from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import StoreModel

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    def delete(self, store_id):
        print("store id: " + store_id)
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        
        return {
            "message": "store has deleted"
        }


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists"
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating a store"
            )

        return store