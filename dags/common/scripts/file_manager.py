import pathlib
import json
import os


def write_json_file(file_content, local_path, file_name) -> None:
    TEMP_FILE_PATH: pathlib.Path = local_path+'/'+file_name

    with open(TEMP_FILE_PATH, "w+") as f:
        response_data = json.loads(file_content.json())
        f.write(json.dumps(response_data, ensure_ascii=False))


def remove_temp_file() -> None:
    TEMP_FILE_PATH = 'data/'
    files = os.listdir(TEMP_FILE_PATH)

    for file in files:
        if file.endswith('.json'):
            os.remove(os.path.join(TEMP_FILE_PATH, file))
