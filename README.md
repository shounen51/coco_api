# coco_api

資料設置
* 用 coco \ images \ train2017 這樣的目錄形式放置所有 coco 原圖
* coco \ annotations 放置 json label

config.yaml 設置
* 將 data / base_dir 指向 images 那層 dir
* data / annotations 指向 json label
* output / base_dir 是輸出整理過後的 yolo 圖片資料夾
* labels_dir 會自動指向對應的 yolo label 資料夾
* names 是要下載的 label，工具只會下載包含這些 label 的圖片以及這些 label，將他和 yolo 訓練資料 yaml 的 names 同步