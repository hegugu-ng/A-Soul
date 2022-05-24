# 这是进行选取已经打标的文件并且重命名为数字序列
import os
import shutil
import xml.etree.ElementTree as ET
from os import getcwd, listdir
from os.path import join

classes = ['Diana','Eileen','Bella','Carol','Ava']
 
def convert(size, box):
 
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

r = 0
def convert_annotation(image_name):
    global r
    in_file = open(f'./Asoul/labels/{image_name}.xml')
    out_file = open(f'./Asoul/txtlabels/{r}.txt',mode='a')
    try:
        shutil.copy(f'./Asoul/images/{image_name}.jpg', f'./Asoul/useimg/{r}.jpg')
    except:
        try:
            shutil.copy(f'./Asoul/images/{image_name}.jpeg', f'./Asoul/useimg/{r}.jpeg')
        except:
            shutil.copy(f'./Asoul/images/{image_name}.png', f'./Asoul/useimg/{r}.png')


    with open(f'./Asoul/labels/{image_name}.xml') as f:
        xml_text = f.read()
        root = ET.fromstring(xml_text)
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)




    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(f"{str(cls_id)} " + " ".join([str(a) for a in bb]) + '\n')
    r += 1
 
wd = getcwd()
 
if __name__ == '__main__':
    list_ = ['.'.join(x.split('.')[:-1]) for x in os.listdir("./Asoul/labels") if os.path.isfile(os.path.join('./Asoul/labels', x))]
    for id in list_:
        try:
            convert_annotation(id)
        except:
            continue


