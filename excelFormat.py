# coding:utf-8 os
import xlrd
import json
import re
import os
import datetime
import profile


'''
[text:'BHCPBZJSA0001', text:'1#搅拌更换搅拌减速机作业', text:'成品工区', text:'一线混料槽上方', text:'/', text:'扳手、撬棍、吊车', text:'使用工具拆卸固定连接螺栓，拆掉旧减速机，回装新减速机', text:'设备停运、断
电、挂牌', text:'触电伤害', text:'1.1正确佩戴好绝缘手套和绝缘鞋。\n1.2相关流程有效隔离。\n1.3使用正确有效的工器具。', empty:'']
'''

# 读取.xls文件


def readExcel(filename):
    f = xlrd.open_workbook(filename=filename)
    data = f.sheet_by_index(0)
    return data

# 填充数据


def fill(data):
    global tmp
    dataList = []
    tmp = ''
    tmp2 = ''
    for line in data.get_rows():
        l = line[0].value
        try:
            if "编码" in l or "code" in l or "导入须知" in l:
                continue
        except Exception:
            print(line)
            # return False
        tmpLine = [i.value for i in line]
        if tmpLine[0]:
            tmp = tmpLine[0]
            tmp2 = tmpLine[4]
        else:
            tmpLine[0] = tmp
            tmpLine[4] = tmp2
        dataList.append(tmpLine)
    return dataList


# 生成数据列表，[{},{}]  ---> 这是基础数据，左右的数据操作都在这个上面做

def generateDict(datalist):
    dataDict = {}
    for i in datalist:
        if i[0] not in dataDict.keys():
            tmpDict = {
                "workNo": 1,
                "workDesc": '|'.join(i[7].split('、')),
                "relaRiskCode": i[8],
                "relaRiskName": i[8],
                "relaSafeCode": i[9],
                "relaSafeDesc": i[9]
            }
            dataDict[i[0]] = [i[0], i[1], "orgCode", i[4],
                              i[4], i[5], i[5], i[2], i[3], i[6], [tmpDict]]
        else:
            n = dataDict[i[0]][-1][-1]["workNo"]
            tmpDict2 = {
                "workNo": n+1,
                "workDesc": '|'.join(str(i[7]).split('、')),
                "relaRiskCode": i[8],
                "relaRiskName": i[8],
                "relaSafeCode": i[9],
                "relaSafeDesc": i[9]
            }
            dataDict[i[0]][-1].append(tmpDict2)
    # for k,v in dataDict.items():
    #     print(k)
    #     print(v)
    return dataDict


# 转换成 json

def dictToJson(datadict, code1, code2, code3, code4):
    tmpList = []
    for v in datadict.values():
        try:
            tmpDict = {}
            tmpDict["jsaCode"] = v[0]
            tmpDict["jsaName"] = ''.join(v[1].split())
            tmpDict["orgCode"] = v[2]
            tmpDict["relaMaterielCode"] = '|'.join(
                [code1[i] if i != "/" else "" for i in v[3].split('、')])
            tmpDict["relaMaterielName"] = v[3] if v[3]!= "/" else ""
            tmpDict["relaToolCode"] = '|'.join(
                [code2[i] for i in v[5].split('、')])
            tmpDict["relaToolName"] = '|'.join(v[6].split('、'))
            tmpDict["workplace"] = v[7]
            tmpDict["workAddress"] = v[8]
            tmpDict["workDesc"] = '|'.join(v[9].split('、'))
        except Exception:
            pass

        # 替换 relaRiskCode，relaSafeCode  现在是个列表
        for i in v[-1]:
            # print(i["relaRiskName"])
            i["relaRiskCode"] = '|'.join([code3[j] for j in (re.sub(r'\d|\.', '', i) for i in i["relaRiskName"].split('\n')) if j])
            i["relaRiskName"] = '|'.join(
                [re.sub(r'\d|\.', '', i) for i in i["relaRiskName"].split('\n')])
            i["relaSafeCode"] = '|'.join([code4[j] for j in (
                re.sub(r'\d|\.', '', i) for i in i["relaSafeDesc"].split('\n')) if j])
            i["relaSafeDesc"] = '|'.join(
                [re.sub(r'\d|\.', '', i) for i in i["relaSafeDesc"].split('\n')])

        tmpDict["workStepDtoList"] = v[-1]
        tmpList.append(tmpDict)
    # for i in tmpList:
    #     print(i)
    return tmpList


# 生成编码字典  -->处理字典
def generateDictCode(datadict, index):
    tmpList = []
    tmpDict = {}
    for v in datadict.values():
        tmpList += [i if i != "/" else ""for i in v[index].split("、")]
        # try:
        #     tmpList += [i if i != "/" else ""for i in v[index].split("、")]
        # except Exception:
        #     pass

    for index, i in enumerate([i for i in set(tmpList) if i], 1):
        k = str(index).zfill(8)
        tmpDict[i] = k
    return tmpDict

# 生成编码字典  --> 处理字典中的列表 relaRiskName


def generateDictCode2(datadict, fieldname):
    tmpList = []
    tmpDict = {}
    for v in datadict.values():
        # print(v[-1])
        lastdata = v[-1]
        for i in lastdata:
            tmpList += [re.sub(r'\d|\.', '', i)
                        for i in str(i[fieldname]).split('\n')]
    for index, i in enumerate([i for i in set(tmpList) if i], 1):
        k = str(index).zfill(8)
        tmpDict[i] = k
    # for k,v in tmpDict.items():
    #     print(k)
    #     print(v)

    return tmpDict


# 扫描目录下的文件
def scanDir(path):
    tmpList = []
    for i in os.listdir(path):
        _, ext = os.path.splitext(i)
        if ext == ".xls":
            tmpList.append(os.path.join(path, i))
    return tmpList


# 处理风险数据关系


def extracData(datadict, dict1, dict2):
    print(dict1)
    tmpList = []
    gList = []
    for v in datadict.values():
        for i in v[-1]:
            tmpDict = {}
            relaRiskName = i["relaRiskName"].split("\n")
            relaSafeDesc = i["relaSafeDesc"].split("\n")
            if len(relaRiskName) < 2:
                k = re.sub(r'\d|\.', '', relaRiskName[0])
                if k:
                    tmpDict[k] = [re.sub(r'\d|\.', '', i) for i in relaSafeDesc if i]
                    tmpList.append(tmpDict)
            else:
                for index, data in enumerate(relaRiskName, 1):
                    kk = re.sub(r'\d|\.', '', data)
                    if kk:
                        tmpDict[kk] = [re.sub(r'\d|\.', '', i) for i in relaSafeDesc if "{}.".format(index) in i]
                        tmpList.append(tmpDict)
    for i in tmpList:
        for k, v in i.items():
            tDict = {}
            tDict["riskCode"] = dict1[k]
            tDict["riskName"] = k
            tDict["relaSafeCode"] = '|'.join([dict2[i] for i in v])
            tDict["relaSafeDesc"] = '|'.join([i for i in v])
            gList.append(tDict)
    return gList


# 扫描文件 检查文件格式
def checkFileFormat(path):
    fileList = scanDir(path)
    for filename in fileList:
        data = readExcel(filename)
        gendata = fill(data)
        if not gendata:
            print('大哥呀文件格式好像有问题啊，检查下吧！！！ --->>{}'.format(filename))


def main():
    path = r"D:\learn\tmp\包化"
    gendata = []
    fileList = scanDir(path)
    for filename in fileList:
        print('扫描文件---->>> {}'.format(filename))
        data = readExcel(filename)
        gendata += fill(data)
    gddata = generateDict(gendata)

    # 工器具数据格式
    code1 = generateDictCode(gddata, 6)
    # 物料数据格式  ---->>>>数据源有问题需要重新处理
    code2 = generateDictCode(gddata, 4)

    # 安全措施数据格式
    code3 = generateDictCode2(gddata, "relaRiskName")
    code4 = generateDictCode2(gddata, "relaSafeDesc")

    gdd = dictToJson(gddata, code1, code2, code3, code4)
    # for i in gdd:
    #     print("写入数据········")
    #     print(json.dumps(i))
    with open('1.txt', 'w') as f:
        for i in gdd:
            f.write(json.dumps(i))
            f.write("\n")

    #  风险格式数据
    # with open('1.txt', 'w') as f:
    #     for i in extracData(gddata, code3, code4 ):
    #         print(i)
    #         f.write(json.dumps(i))
    #         f.write("\n")

    # with open('1.txt', 'w') as f:
    #     for i in code3:
    #         print(i)
    #         f.write(json.dumps(i))


if __name__ == "__main__":
    print(datetime.datetime.now())
    # profile.run("main()")
    # checkFileFormat(r"D:\learn\tmp\包化")
    main()
    print(datetime.datetime.now())
