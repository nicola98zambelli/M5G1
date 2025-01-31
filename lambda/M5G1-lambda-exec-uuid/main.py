import uuid

def lambda_handler(event, context):
    
    exec_uuid = str(uuid.uuid4())

    return {
        'exec_uuid': exec_uuid
    }