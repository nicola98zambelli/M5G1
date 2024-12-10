import json
import boto3

def lambda_handler(event, context):
    try:
        # Initialize Step Functions client with explicit region
        stepfunctions_client = boto3.client('stepfunctions', region_name='us-east-1')
        
        # Get Step Function ARN 
        state_machine_arn = "arn:aws:states:us-east-1:314146336986:stateMachine:M5G1-sftest"
        
        # Prepare input for Step Function
        input_payload = {
            'data': event.get('data', {})
        }
        
        # Trigger Step Function execution
        response = stepfunctions_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_payload)
        )
        
        print("Successfully triggered Step Function!")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'executionArn': response['executionArn'],
                'startDate': str(response['startDate'])
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

# Add a local testing block
if __name__ == '__main__':
    # Simulate an event for local testing
    test_event = {
        'data': {
            'some_key': 'some_value'
        }
    }
    
    print("Running local test...")
    result = lambda_handler(test_event, None)
    print("\nFunction Result:")
    print(json.dumps(result, indent=2))