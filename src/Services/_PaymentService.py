from flask import Request, jsonify
from bson import ObjectId

from Core._StructurePlans import StructurePlans
from Repository import PlansRepository

from CustomExceptions import (
    HeaderInvalid
)

from .utils.validators import validate_headers

class PaymentService:
    def create_plan(user: ObjectId, request: Request):
        try:
            
            validate_headers(key_from_request=request.headers['X-Private-Header'])

            data = request.get_json()

            name = data.get("name")
            price = float(data.get("price"))

            if not name or len(name) < 5 or not price:
                raise

            plan = StructurePlans(namePlan=name, pricePlan=price)


            return jsonify({"msg": 'Plano cirado com sucesso!'}), 200
        
        except HeaderInvalid as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:  
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500