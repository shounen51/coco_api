import os, shutil
from pycocotools.coco import COCO
import skimage.io as io

def make_pic_txt(pic_name, obj_list):
    with open(pic_name, "w") as txt:
        _str = ""
        for obj in obj_list:
            _str += " ".join([str(cxy) for cxy in obj]) + "\n"
        txt.write(_str)

dataDir='/home/ubuntu/datasets/'
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
imgDir = os.path.join(dataDir, dataType)
detDir = '/home/ubuntu/datasets/yolov5/images/train/'
txtDir = '/home/ubuntu/datasets/yolov5/labels/train/'
my_class = ['person']
coco=COCO(annFile)

cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

catIds = coco.getCatIds(catNms=my_class);
imgIds = coco.getImgIds(catIds=catIds );
total = len(imgIds)
for i, imgId in enumerate(imgIds):
    objs = []
    img = coco.loadImgs(imgId)[0]
    try:
        shutil.copyfile(os.path.join(imgDir,img['file_name']), os.path.join(detDir,img['file_name']))
    except:
        I = io.imread(img['coco_url'])
        io.imsave(os.path.join(detDir,img['file_name']), I)
    txt_path = os.path.join(txtDir, img['file_name'].replace(".jpg", ".txt"))

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
        cat = ann['category_id']
        obj.append(cat)
        obj += xywh
        objs.append(obj)
    make_pic_txt(txt_path, objs)
    print(f"\r [{round((i/total)*100,2)} %] ({i} / {total})    ", end = "")
