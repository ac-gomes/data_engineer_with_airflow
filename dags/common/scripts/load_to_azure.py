from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.microsoft.azure.hooks.data_lake import AzureDataLakeHook


class AzureUploader():
    """ class has two methods to write files into azure storage """

    def upload_to_azure_bob(file_name, container_name, blob_name) -> None:

        Wasb_Hook = WasbHook(wasb_conn_id='az-blob-conn')

        Wasb_Hook.load_file(
            file_path=file_name,
            container_name=container_name,
            blob_name=blob_name,
            overwrite=True,

        )

    def upload_to_azure_datalake(azure_data_lake_conn_id, local_path, remote_path) -> None:

        hook = AzureDataLakeHook(
            azure_data_lake_conn_id=azure_data_lake_conn_id)

        hook.upload_file(
            local_path=local_path,
            remote_path=remote_path,
            overwrite=True
        )
