# 保留指定class的圖片以及指定class的標籤，並刪除所有不在指定class列表中的圖片和標籤
from pathlib import Path
import os
import shutil
from tqdm import tqdm

ori_classes = ["person", "bicycle", "car", "motorcycle", "bus", "train", "backpack", "handbag", "suitcase", "wheelchair", "person_on_wheelchair"]
keep_classes = ["person", "bicycle", "wheelchair", "person_on_wheelchair"]  # 指定要保留的class名稱

dataset_label_dir=Path(r"E:\wheelchair_11\wheelchair\labels\train")
dataset_image_dir=Path(str(dataset_label_dir).replace("labels", "images"))
target_label_dir=Path(r"E:\wheelchair_4\wheelchair\labels\train")
target_image_dir=Path(str(target_label_dir).replace("labels", "images"))
target_label_dir.mkdir(parents=True, exist_ok=True)
target_image_dir.mkdir(parents=True, exist_ok=True)
for label_file in tqdm(dataset_label_dir.glob("*.txt")):
    with open(label_file, 'r') as f:
        lines = f.readlines()

    # 只保留指定class的標籤
    temp_lines = []
    for line in lines:
        l = line.split(" ")
        if ori_classes[int(l[0])] in keep_classes:
            l[0] = str(keep_classes.index(ori_classes[int(l[0])]))
            temp_lines.append(" ".join(l))
    if len(temp_lines) == 0:
        continue
    try:
        shutil.copyfile(str(label_file).replace("labels", "images").replace(".txt",".jpg"), target_image_dir / label_file.name.replace(".txt",".jpg"))
    except:
        continue
    with open(target_label_dir / label_file.name, 'w') as f:
        f.writelines(temp_lines)
