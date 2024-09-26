def create_pipeline(rules: dict) -> list:

    pipeline = [
        {
            "$match": {"_id": rules.get('id')} 
        },
        {
            "$lookup": {
                "from": rules.get('from'), 
                "localField": rules.get('local'), 
                "foreignField": rules.get('foreign'),  
                "as": rules.get('as') 
            }
        },
        {
            "$project": rules.get('project')
        }
    ]
          
    return pipeline