import json
import typing
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

class StepFunctionTrigger:
    def __init__(self, 
                 region_name: str = 'us-east-1', 
                 state_machine_arn: str = "arn:aws:states:us-east-1:314146336986:stateMachine:M5-G1-sfjobswaterfall"):
        """
        Initialize Step Functions client and configuration.
        
        :param region_name: AWS region for the Step Function
        :param state_machine_arn: ARN of the Step Function state machine
        """
        self._stepfunctions_client = boto3.client('stepfunctions', region_name=region_name)
        self._state_machine_arn = state_machine_arn

    def trigger(self) -> Dict[str, Any]:
        """
        Trigger Step Function execution.
        
        :return: Dictionary with execution details
        """
        try:
            # Start Step Function execution with empty input
            response = self._stepfunctions_client.start_execution(
                stateMachineArn=self._state_machine_arn
            )
            
            return {
                'statusCode': 200,
                'body': {
                    'executionArn': response['executionArn'],
                    'startDate': str(response['startDate'])
                }
            }
        
        except ClientError as e:
            print(f"AWS Client Error: {e}")
            return {
                'statusCode': 500,
                'body': {'error': str(e)}
            }
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {
                'statusCode': 500,
                'body': {'error': str(e)}
            }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for triggering Step Function.
    
    :param event: Lambda event object (not used)
    :param context: Lambda context object (not used)
    :return: Execution result
    """
    trigger = StepFunctionTrigger()
    return trigger.trigger()

# Local testing block
if __name__ == '__main__':
    print("Running local test...")
    result = lambda_handler({}, None)
    print("\nFunction Result:")
    print(json.dumps(result, indent=2))