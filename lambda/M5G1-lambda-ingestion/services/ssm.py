import boto3


class ssm:
    @staticmethod
    def get_parameter(name, with_decryption):
        ssm = boto3.client('ssm')
        res = ssm.get_parameter(
            Name=name,
            WithDecryption=with_decryption
        )
        return res["Parameter"]["Value"]