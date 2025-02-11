# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ['薄翅锯天牛', '碧蛾蜡蝉', '扁刺蛾', '草履蚧', '大青叶蝉', '分月扇舟蛾', '柑橘凤蝶', '光肩星天牛', '黑蚱蝉', '红尾大蚕蛾', '黄刺蛾', '美国白蛾', '人纹污灯蛾', '桑天牛', '松墨天牛','桃红颈天牛','星天牛', '杨扇舟蛾', '杨小舟蛾', '云斑白条天牛']



def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    # try:
        in_file = open('VOCData/Annotations/%s.xml' % (image_id), encoding='utf-8')
        out_file = open('VOCData/labels/%s.txt' % (image_id), 'w', encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " +
                           " ".join([str(a) for a in bb]) + '\n')
    # except Exception as e:
    #     print(e, image_id)


wd = getcwd()
for image_set in sets:
    if not os.path.exists('VOCData/labels/'):
        os.makedirs('VOCData/labels/')
    image_ids = open('VOCData/labels/%s.txt' %
                     (image_set)).read().strip().split()
    list_file = open('VOCData/%s.txt' % (image_set), 'w')
    for image_id in tqdm(image_ids):
        list_file.write('VOCData/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
