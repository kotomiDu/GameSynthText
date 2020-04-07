from collections import Counter
import pickle

filename =u"C:\\Users\\yarudu\\Documents\\project\\synth_tool\\SynthText\\data\\textsource_temp.txt"
def start(filename):
    cnt=0
    with open(filename, encoding="utf-8") as f:
        c = Counter()
        for x in f:
            #x=x.decode('utf-8')
            c += Counter(x.strip())
            cnt+=len(x.strip())
            #print c


    for key in c:
        c[key]=float(c[key])/cnt  
        #print key,c[key]
        
    d = dict(c)
    #print d
    with open("data/models/char_freq.cp",'wb') as f:
        pickle.dump(d,f)

if __name__ == '__main__':
    start(filename)

