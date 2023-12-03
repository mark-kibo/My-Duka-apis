from flask_restx import Namespace, Resource , marshal, fields
from flask import request
from http import HTTPStatus
from ..models.stores import  Store

store_namespace= Namespace("stores", "stores endpoints")







store_model = store_namespace.model('store', {
    'store_id': fields.Integer(description='The unique identifier of a store'),
    'store_name': fields.String(description='The name of the store'),
    'location': fields.String(description='The location address of the store'),
    'user_id': fields.Integer(description='The owner of the store'),
})



@store_namespace.route("/")
class StoreList(Resource):

    # @store_namespace.marshal_list_with(store_model)
    def get(self):
        "get all stores available"
        try:
            stores = Store.query.all()
            print(stores)  # Check what is retrieved from the database

            if stores:
                return marshal(stores, store_model), HTTPStatus.OK
            else:
                return {"message": "No stores found"}, HTTPStatus.OK
      
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
        

    @store_namespace.expect(store_model)
    def post(self):
        """Create new store"""
        
        try:
            data = request.get_json()

            new_store = Store(
                store_name=data.get('store_name'),
                location=data.get('location'),
                user_id=data.get('user_id'),
                # supplier_id=data.get('supplier_id')
            )
            print(new_store.location)

            new_store.save()

            # Optionally, you can return the newly created store
            return marshal(new_store, store_model), HTTPStatus.CREATED

        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
        

    


@store_namespace.route("/<int:id>")
class MutateStore(Resource):
    def get(self, id):
        """Get a single store by its ID"""
        try:
            store = Store.query.filter_by(id=id).first()
            if not store:
                return {"message": f"Store with id '{id}' doesn't exist."}, HTTPStatus.NOT_FOUND
            return marshal(store, store_model), HTTPStatus.OK
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
        

    @store_namespace.expect(store_model)
    def patch(self, id):
        """Update an existing store"""
        try:
            store = Store.query.filter_by(id=id).first()
            if not store:
                return {"message": f"Store with id '{id}' doesn't exist."}, HTTPStatus.NOT_FOUND
            data = request.get_json()
            for attr in data:
                setattr(store, attr, data.get(f'{attr}'))
            store.save()
            return marshal(store, store_model, skip_none=True), HTTPStatus.OK
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
        

# this is only allowed by a mercharnt to delete a store


@store_namespace.route("/<store_id>/<role_naem>/")
class DeletStore(Resource):
    def delete(self, role_name, store_id):
        """Delete a store and all of its associated products"""
        try:
            # check if the user has permission to do that
            if int(role_name) != "merchant":
                return {"message": "You don't have permissions to perform this action!"}, HTTPStatus.UNAUTHORIZED
            


            store = Store.query.filter_by(store_id=store_id).first()
            if not store:
                return {"message": f"Store with id '{store_id}' doesn't exist."}, HTTPStatus.NOT_FOUND
            
            
            # this delete is modified to delete also p[roducts associated with the store
            store.delete()
            return {"message": f"Successfully deleted store with id '{store_id}'"}, HTTPStatus.NO_CONTENT
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
