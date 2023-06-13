
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class AWSUploader():
    """ class has two methods to write files into azure storage """

    def upload_to_s3_bucket(filename, key, bucket_name) -> None:
        hook = S3Hook(aws_conn_id='s3_conn')

        hook.load_file(
            filename=filename,
            key=key,
            bucket_name=bucket_name,
            replace=True
        )
