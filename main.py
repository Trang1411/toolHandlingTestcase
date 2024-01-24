import json
import os
import shutil


def copy_file():
    # Lấy đường dẫn của file cần copy
    file_path = os.path.join("bo_auto", "0.0,0.37 - Copy (5)", "body.json")
    # Lấy đường dẫn của folder đích
    destination_folder_path = os.path.join("bo_auto")
    # Lấy danh sách các file trong folder
    folder_list = os.listdir(destination_folder_path)
    print(folder_list)

    for folder in folder_list:
        # Copy file vào folder đích
        folder_path_copy = os.path.join("bo_auto", folder)
        if not os.path.isfile(os.path.join(folder_path_copy, file_path)):
            shutil.copy(file_path, folder_path_copy)


def insertFile():
    folders = os.listdir("bo_auto")
    file_expected_result = os.path.join("bo_auto\\0.0,0.37 - Copy (5)", "body.json")
    print(f"file_expected_result ====== {os.path.exists(file_expected_result)}")
    for folder in folders:
        if folder == "0.0,0.37 - Copy (5)":
            continue
        path = os.path.join("bo_auto\\", folder)
        # Sao chép file vào thư mục
        shutil.copy(file_expected_result, path)


def editContentFile():
    # đọc file và lấy ra key-value cần sửa
    path_file_edit = os.path.join("bo_auto\\0.0,0.37 - Copy (5)", "body.json")
    with open(path_file_edit, "r") as rf:
        data = json.load(rf)

    # print(f"data ========== {data}")
    crop_param = data["crop_param"]
    print(f"crop_param ======= {crop_param}")

    folders = os.listdir("bo_auto")
    for folder in folders:
        if folder == "0.0,0.37 - Copy (5)":
            continue
        path_file_edit = os.path.join("bo_auto\\", folder, "body.json")
        # đọc file và lấy ra key-value cần sửa
        with open(path_file_edit, "r") as rf:
            data = json.load(rf)

        name = folder.split(" ")[0]

        data["crop_param"] = name
        #         ghi lại vào file body.json
        print(f" ============ data =========== {data['crop_param']}")
        with open(path_file_edit, "w") as wf:
            json.dump(data, wf, indent=4)


def insertExpectedResultAndBody():
    folders = os.listdir("bo_auto")
    file_expected_result = os.path.join("bo_auto\\0.0,0.37 - Copy (5)", "expected_result.json")
    print(f"file_expected_result ====== {os.path.exists(file_expected_result)}")
    for folder in folders:
        if folder == "0.0,0.37 - Copy (5)":
            continue
        path = os.path.join("bo_auto\\", folder)
        # Sao chép file vào thư mục
        shutil.copy(file_expected_result, path)


def removeFile():
    folders = os.listdir("bo_auto")
    for folder in folders:
        if folder == "0.0,0.37 - Copy (5)":
            continue
        path = os.path.join("bo_auto\\", folder, "body.json")
        os.remove(path)


if __name__ == '__main__':
    # removeFile()
    # insertFile()
    editContentFile()
