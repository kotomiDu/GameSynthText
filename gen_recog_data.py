import re
import cv2
import os
import glob
'''
1.crop image to all_train
2.label box to all_label
3.generate character dictionary
'''

def start(data_root):
    chardic = set()
    recog_img_path = os.path.join(data_root, 'recognition_data')
    recog_label_path = os.path.join(data_root,"recognition_label.txt")
    img_path = os.path.join(data_root,'img_gen')
    if(os.path.exists(recog_img_path) is False):
        os.makedirs(recog_img_path)

    recog_label_f = open(recog_label_path, 'w', encoding="utf-8")
    imlist = []
    imlist.extend(glob.glob(os.path.join(img_path,"*png")))
    if len(imlist) != 0:
        for fn in imlist:
            image_prefix,_ = os.path.splitext(os.path.basename(fn))
            label_file = os.path.join(data_root , "label_gen", image_prefix + ".txt") 
            im = cv2.imread(fn.rstrip())
            with open(label_file, 'r', encoding="utf-8") as f:
                for idx, line in enumerate(f.readlines()):
                    line = line.rstrip()
                    if line.startswith("[[") or line.startswith(" ["):
                        continue
                    lx, ly, rx, ry = line.split(" ")[:4]
                    word = line[line.find("\""):][1:-1]

                    crop_img = im[int(ly):int(ry),int(lx):int(rx)]
                    recog_img_file = os.path.join(recog_img_path,image_prefix+'_'+str(idx).zfill(3)+'.png')
                    cv2.imwrite(recog_img_file,crop_img)
                    recog_label_f.write("{} {}".format(recog_img_file, word))
                    for ch in word:
                        chardic.add(ch)
                  
    recog_label_f.close()
    chardic_f = open(os.path.join(data_root , "character_dic.txt"),"w", encoding="utf-8")
    for item in chardic:
        chardic_f.write(item)

    chardic_f.close()


if __name__=='__main__':
    data_root = "data/dataset/wot/"
    start(data_root)
