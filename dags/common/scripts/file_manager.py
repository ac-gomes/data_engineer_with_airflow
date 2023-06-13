import pathlib
import json
import csv
import os


def write_json_file(file_content,  local_path, file_name) -> None:
    TEMP_FILE_PATH: pathlib.Path = local_path+'/'+file_name

    with open(TEMP_FILE_PATH, "w+") as f:
        response_data = json.loads(file_content.json())
        f.write(json.dumps(response_data, ensure_ascii=False))


def write_csv_file(file_content, cursor, local_path, file_name) -> None:
    TEMP_FILE_PATH = local_path+'/'+file_name

    with open(TEMP_FILE_PATH, "w+") as f:
        write_csv = csv.writer(f)
        write_csv.writerow(file_content)
        write_csv.writerows(cursor)


def remove_temp_file() -> None:
    TEMP_FILE_PATH = 'data/'
    files = os.listdir(TEMP_FILE_PATH)

    for file in files:
        if file.endswith(pathlib.Path(file).suffix):
            os.remove(os.path.join(TEMP_FILE_PATH, file))
