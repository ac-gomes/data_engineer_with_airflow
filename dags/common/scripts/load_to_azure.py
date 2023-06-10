from airflow.providers.microsoft.azure.hooks.wasb import WasbHook


def upload_to_azure_bob(file_name, container_name, blob_name, wasb_conn_id) -> None:

    Wasb_Hook = WasbHook(wasb_conn_id=wasb_conn_id)

    Wasb_Hook.load_file(
        file_path=file_name,
        container_name=container_name,
        blob_name=blob_name,
        overwrite=True,
    )
