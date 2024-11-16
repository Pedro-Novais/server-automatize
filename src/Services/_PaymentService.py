import requests

from flask import Request, jsonify, g
from bson import ObjectId

from Core._StructurePlans import StructurePlans

from config import ENDPOINTS, HEADER_PREVIEW
from .utils.validators import validate_headers

from pymongo.errors import PyMongoError
from bson.errors import InvalidId

from Models import (
    Plans,
    Subscriptions
)

from Repository import (
    PlansRepository,
    UserRepository,
    UserAndPaymentsRepository,
    CardsClientsRepository,
    SubscriptionsRepository,
)

from CustomExceptions import (
    HeaderInvalid,
    DatasNotSend,
    OperationsDatabaseException,
    UserNotFound,
    PlanNotFound,
    CardsNotFound
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
        try:
            user_repo = UserRepository(db=g.db)
            plan_repo = PlansRepository(db=g.db)
            card_repo = CardsClientsRepository(db=g.db)
            user_subs_repo = UserAndPaymentsRepository(
                db=g.db,
                client=g.client
            )

            data = request.get_json()

            plan  = data.get("plan")

            if not plan:
                raise DatasNotSend("Parametros não foram enviados ao servidor!")

            filter_user = {
                "_id": user
            }

            projection_user = {
                "clientId": 1,
                "email": 1,
                "token_card": 1,
            }

            user_exist = user_repo.get(
                query_filter=filter_user,
                projection=projection_user
            )

            if not user_exist:
                raise UserNotFound()
            
            if not user_exist.get("clientId") or not user_exist.get("email"):
                raise UserNotFound("Usuário possui inconsistências em seu cadastro!")
            
            if not user_exist.get("token_card"):
                raise CardsNotFound("Usuário não possui métodos de pagamentos cadastrados!")
            
            filter_plan = {
                "_id": ObjectId(plan)
            }

            projection_plan = {
                "planId": 1
            }

            plan_exist = plan_repo.get(
                query_filter=filter_plan,
                projection=projection_plan
            )

            if not plan_exist:
                raise PlanNotFound()

            if not plan_exist.get("planId")[0]:
                raise PlanNotFound("Plano selecionado possui inconsistência em seu cadastro!")
            
            filter_card = {
                "owner": user,
                "default": True
            }

            projection_card = {
                "token": 1
            }

            card_exist = card_repo.get(
                query_filter=filter_card,
                projection=projection_card
            )

            if not card_exist:
                raise CardsNotFound()
            
            if not card_exist.get("token"):
                raise CardsNotFound("Inconsistência de cadastro do cartão selecionado!")
            
            subscription_data = {
                "preapproval_plan_id": plan_exist.get("planId")[0],
                "payer_email": user_exist.get("email"),
                "card_token_id": card_exist["token"],
            }

            response_create_subscription = requests.post(
                url=ENDPOINTS.SUBSCRIPTION,
                headers=HEADER_PREVIEW,
                json=subscription_data
            )

            response = response_create_subscription.json()

            if not response_create_subscription.status_code == 201 and not response_create_subscription.status_code == 200:
                return jsonify({"error": "Erro ao criar assinatura no gateway de pagamentos", "msg": response.get("message")}), response.get("status")
            
            subscription = Subscriptions(
                subscriptionId=response.get("id"),
                userId=user,
                planId=plan_exist.get("planId"),
                payer=response.get("payer_id"),
                auto_recurring=response.get("auto_recurring"),
                status=response.get("status"),
                created_at=response.get("date_created"),
                last_update=response.get("last_modified")
            )

            update_user = {
                "subscriptions": None
            }

            result_operation = user_subs_repo.update_user_and_create_subscription(
                query_user=filter_user,
                update_user=update_user,
                create_subscription=subscription.to_dict()
            )
            
            if not result_operation["user_update"] or not result_operation["subscription_insert"]:
                raise OperationsDatabaseException()

            return jsonify({"msg": 'Assinatura criada com sucesso!'}), 200
        
        except (
            DatasNotSend,
            UserNotFound,
            PlanNotFound,
            OperationsDatabaseException
            ) as e:
            return jsonify({"error": e.message}), e.status_code
        
        except InvalidId as e:
            return jsonify({"error": "Parametros incorretos enviados ao servidor: {}".format(str(e))}), 400
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao atualizar os docuemntos: {}".format(str(e))}), 500
        
        except Exception as e:  
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def cancel_subscription(user: ObjectId, ) -> dict:
        pass