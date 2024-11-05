from pymongo.errors import PyMongoError

class UserAndPaymentsRepository:
    def __init__(
            self, 
            db,
            client,
            ) -> None:
        self.db = db
        self.client = client

    def update_user_and_create_card(
            self,
            query_user,
            update_user,
            create_card
            ):
         with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    result_insert = self.db.cardsPayments.insert_one(
                        create_card,
                        session=session
                    )

                    update_user["$push"]["token_card"] = result_insert.inserted_id

                    result_update = self.db.users.update_one(
                        query_user,
                        update_user,
                        session=session
                    )

                return {
                    "user_update": result_update.modified_count,  
                    "card_inserted_id": result_insert.inserted_id  
                }

            except PyMongoError as e:
                raise