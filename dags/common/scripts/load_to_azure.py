from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.microsoft.azure.hooks.data_lake import AzureDataLakeHook


class AzureUploader():

    def upload_to_bob(blob_name, file_name, container_name, azure_conn_id) -> None:

        Wasb_Hook = WasbHook(wasb_conn_id=azure_conn_id)
        try:

            Wasb_Hook.load_file(
                file_path=file_name,
                container_name=container_name,
                blob_name=f'{blob_name}/sports.json',
                overwrite=True,

            )

        except Exception as Error:
            print(f'Something went worng! Error: {Error}')

    def upload_to_azure_datalake(azure_data_lake_conn_id, local_path, remote_path):

        hook = AzureDataLakeHook(
            azure_data_lake_conn_id=azure_data_lake_conn_id)

        hook.upload_file(
            local_path=local_path,
            remote_path=remote_path,
            overwrite=True
        )
