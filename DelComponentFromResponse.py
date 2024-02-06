import json
import os


def readFileJson(path):
    with open(path, "r", encoding="utf-8") as rf:
        response_data = json.load(rf)
    return response_data


def writeFileJson(data, path):
    with open(path, "w", encoding="utf-8") as wf:
        json.dump(data, wf, indent=4)


def remove_element_by_key_path(data, key_path):
    keys = key_path.split('.')
    current = data

    for key in keys[:-1]:
        if key in current:
            current = current[key]
        else:
            # Key path không tồn tại, không cần xử lý
            return

    last_key = keys[-1]
    if last_key in current:
        del current[last_key]


def removeComponent():
    quality_front = ["resolution", "bright_spot_param", "average_intensity", "bright_spot_threshold",
                     "total_bright_spot_area", "final_result", "low_resolution_likelihood", "blurred_likelihood",
                     "bright_spot_likelihood", "bad_luminance_likelihood", "blur_score", "bright_spot_score",
                     "luminance_score"]

    checking_result_front = ["recaptured_result", "recaptured_prob", "edited_result", "edited_prob",
                             "corner_cut_result", "corner_cut_prob", "check_photocopied_result",
                             "check_photocopied_prob"]

    # lấy danh sách các folder
    folders = os.listdir("Ocr_Hanh_GPU")
    # Duyệt qua các folder trong Ocr_Sandbox
    for folder in folders:
        # Lấy đường dẫn của file expected_result.json
        file_path = os.path.join("Ocr_Hanh_GPU", folder, "expected_result.json")
        data = readFileJson(file_path)
        # print(f"00000000000 {folder} ::::  {data['object']} ")
        # print("=======================", file_path)
        if "object" not in data:
            continue
        else:
            if "quality_front" in data["object"]:
                dict_q = data["object"]["quality_front"]
                # print(f"000000000000 quality_front là :::::::: {dict_q}")
                if dict_q == {}:
                    del data["object"]["quality_front"]
                for qf in quality_front:
                    if qf in dict_q.keys():
                        print(f' key-value cần xóa là {qf} - {data["object"]["quality_front"][qf]}')
                        # del data["object"]["quality_front"][qf]
                        path = "object.quality_front." + qf
                        remove_element_by_key_path(data, path)
                        if qf not in data["object"]["quality_front"].keys():
                            print("Xóa thành công nhaaaaaaa")

            if "checking_result_front" in data["object"]:
                print(f' giá trị của mảng checking_result_front là:: {data["object"]["checking_result_front"]}')
                dict_cr = data["object"]["checking_result_front"]
                if dict_cr == {}:
                    del data["object"]["checking_result_front"]
                for qcr in checking_result_front:

                    if qcr in dict_cr.keys():
                        print(f' key-value cần xóa là {qcr} - {data["object"]["checking_result_front"][qcr]}')
                        # del data["object"]["quality_front"][qf]
                        path = "object.quality_front." + qcr
                        remove_element_by_key_path(data, path)
                        # if qcr in data["object"]["quality_front"].keys():
                        #     print("Xóa không thành công nhaaaaaaa")

            writeFileJson(data, file_path)


if __name__ == '__main__':
    removeComponent()
