import os
import glob
import codecs

def start(dataroot):

    label_path= os.path.join(dataroot , "label_gen")
    detection_label_path = os.path.join(dataroot , "detection_label")
    if not os.path.exists(detection_label_path):
        os.mkdir(detection_label_path)
    files=[]
    for ext in ['txt']:
        files.extend(glob.glob(
                os.path.join(label_path, '*.{}'.format(ext))))

    for fn in files:
        basename = os.path.basename(fn)
        fw = open(os.path.join(detection_label_path,basename),'w', encoding='utf-8')
        with open(fn, 'r',encoding="utf-8") as f:
            for idx, line in enumerate(f.readlines()):
                line = line.rstrip()
                if line.startswith("[[") or line.startswith(" ["):
                    continue
                lx, ly, rx, ry = line.split(" ")[:4]
                ch = line[line.find("\""):][1:-1]
                if idx != 0:
                    fw.write("\n")
                fw.write((",").join([lx, ly, rx, ly, rx, ry, lx, ry]))
                fw.write("," + ch)
        fw.close()

if __name__=='__main__':
    data_root = "data/dataset/wot/"
    start(data_root)