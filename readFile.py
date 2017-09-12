__author__ = 'YANGDY'
import chardet

def readfiles(dataPath, firstRow, charset,separator):
    listdata =[]
    header=[]
    try:
        fsock = open(dataPath, "r")
    except IOError:
        print "The file {" + dataPath + "}don't exist, Please double check!"
        return
    s = fsock.readlines()
    fsock.close()
    i=0
    for line in s:
        datas = line.split(separator)
        if len(datas)<=1:
            print 'datas: '+datas
            continue;
        row =[]
        if i==0 and firstRow:
            for d in datas:
                d = d.decode(charset).encode("utf-8")
                header.append(d.strip('\n').strip())
            # print 'header: '+str(header)
            i = i + 1
            continue

        for d in datas:
            d = d.decode(charset).encode("utf-8")
            row.append(d.strip('\n').strip())
        listdata.append(row)
        i = i + 1

        if i>5840000:
            return listdata
    if not firstRow:
        return listdata

    return header, listdata

