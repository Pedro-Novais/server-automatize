import requests

from flask import Request, jsonify, g
from bson import ObjectId

from Core._StructurePlans import StructurePlans
from Repository import PlansRepository
from Models import Plans

from .utils.validators import validate_headers

from config import ENDPOINTS, HEADER_PREVIEW

from CustomExceptions import (
    HeaderInvalid,
    DatasNotSend,
    OperationsDatabaseException
)

class PaymentService:
    def get_plan(user: ObjectId) -> dict:
        try:
            plan_repo = PlansRepository(db=g.db)

            projection = {
                "planId": 0
            }

            plans = list(plan_repo.get_many(
                query_filter={}, 
                projection=projection
                ))
            
            for plan in plans:
                plan["_id"] = str(plan["_id"])

            if len(plans) == 0:
                raise DatasNotSend("Não há planos cadastrados na base de dados!")

            return jsonify({"msg": 'Operação realizada com sucesso!', "plans": plans}), 200
        
        except (
            DatasNotSend,
            ) as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:  
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def create_plan(user: ObjectId, request: Request):
        try:
            
            plan_repo = PlansRepository(g.db)
            custom_header = request.headers.get('X-Private-Header')

            if custom_header is None:
                raise HeaderInvalid()
            
            validate_headers(key_from_request=custom_header)

            data = request.get_json()

            name = data.get("name")
            price = float(data.get("price"))
            details = data.get("details")

            if not name or not price:
                raise DatasNotSend()

            plan_data = StructurePlans(namePlan=name, pricePlan=price)

            response = requests.post(
                ENDPOINTS.CREATE_PLAN,
                json=plan_data.to_dict(), 
                headers=HEADER_PREVIEW
            )

            response_data = response.json()

            if not response_data["status"] == 201 and not response_data["status"] == "active":
                return jsonify({"msg": response_data.get["message"]}), response_data.get["status"]

            plan_final = Plans(
                planId= response_data["id"],
                namePlan=response_data["reason"],
                auto_recurring=response_data["auto_recurring"],
                status=response_data["status"],
                date_created=response_data["date_created"],
                details=details
            )
            
            result = plan_repo.post(data=plan_final.to_dict())

            if not result:
                raise OperationsDatabaseException("Erro ao criar o plano")

            return jsonify({"msg": 'Plano criado com sucesso!'}), 200
        
        except (
            HeaderInvalid, 
            DatasNotSend,
            OperationsDatabaseException
            ) as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:  
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        

    def create_subscription(user: ObjectId, request: Request) -> dict:
        pass

    def cancel_subscription(user: ObjectId, ) -> dict:
        pass