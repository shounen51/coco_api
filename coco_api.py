import os, shutil
from pycocotools.coco import COCO
import skimage.io as io
from pathlib import Path
import yaml

def make_pic_txt(pic_name, obj_list):
    with open(pic_name, "w") as txt:
        _str = ""
        for obj in obj_list:
            _str += " ".join([str(cxy) for cxy in obj]) + "\n"
        txt.write(_str)


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

data_dir = Path(config['data']['base_dir'])
data_type = config['data']['type']
ann_file = data_dir.parent / config['data']['annotations'].format(type=data_type)
img_dir = Path(config['data']['images'].format(base_dir=data_dir, type=data_type))

output_dir = Path(config['output']['base_dir']).joinpath(data_type)
if not output_dir.exists():
    output_dir.mkdir(parents=True)

txt_dir = Path(config['output']['labels_dir'].format(base_dir=str(output_dir)).replace('images', 'labels'))
if not txt_dir.exists():
    txt_dir.mkdir(parents=True)

my_class = config['classes']

# 输出检查
print("Annotation File:", ann_file)
print("Image Directory:", img_dir)
print("Output Image Directory:", output_dir)
print("Labels Directory:", txt_dir)
print("Classes:", my_class)

coco=COCO(ann_file)
cats = coco.loadCats(coco.getCatIds())
categories = coco.cats
nms=[cat['name'] for cat in cats]
if len(my_class) == 0: my_class = nms
print('Download categories: \n{}\n'.format(' '.join(my_class)))
# nms = set([cat['supercategory'] for cat in cats])
# print('COCO supercategories: \n{}'.format(' '.join(nms)))

imgIds = []
catIds = coco.getCatIds(catNms=my_class)
for c in catIds:
    imgIds += coco.getImgIds(catIds=c)
imgIds = list(set(imgIds))
total = len(imgIds)

for i, imgId in enumerate(imgIds):
    objs = []
    img = coco.loadImgs(imgId)[0]
    try:
        shutil.copyfile(os.path.join(img_dir,img['file_name']), os.path.join(output_dir,img['file_name']))
    except:
        I = io.imread(img['coco_url'])
        io.imsave(os.path.join(str(output_dir), img['file_name']), I)
    txt_path = os.path.join(txt_dir, img['file_name'].replace(".jpg", ".txt"))

    annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
    anns = coco.loadAnns(annIds)
    height = img['height']
    width = img['width']
    for ann in anns:
        obj = []
        xywh = [
            round((ann['bbox'][0]+ann['bbox'][2]/2)/width, 6),
            round((ann['bbox'][1]+ann['bbox'][3]/2)/height, 6),
            round(ann['bbox'][2]/width,6),
            round(ann['bbox'][3]/height,6)
        ]
        cat_id = ann['category_id']
        class_id = my_class.index(categories[cat_id]['name'])
        obj.append(class_id)
        obj += xywh
        objs.append(obj)
    make_pic_txt(txt_path, objs)
    print(f"\r [{round((i/total)*100,2)} %] ({i} / {total}) \U0001F680   ", end = "")
