# coding:utf-8 os
import xlrd
import json
import re
import os
import datetime
import httpx
import time

# 读取.xls文件
def readExcel(filename):
    f = xlrd.open_workbook(filename=filename)
    data = f.sheet_by_index(0)
    return data


# 获取当前时间的时分秒 ==》》11:22:33    112233 

def getCurDate():
    return time.strftime('%H%M%S',time.localtime(time.time()))

# 填充数据
def fill(data):
    global tmp
    dataList = []
    tmp = ''
    tmp2 = ''
    sheet = data.name
    for line in data.get_rows():
        l = line[0].value
        try:
            if "编码" in l or "code" in l or "导入须知" in l:
                continue
        except Exception:
            print(line)
        tmpLine = [i.value for i in line]
        if tmpLine[0]:
            tmp = tmpLine[0]
            tmp2 = tmpLine[4]
        else:
            tmpLine[0] = tmp
            tmpLine[4] = tmp2
        tmpLine.append(sheet)
        dataList.append(tmpLine)
    return dataList


# 生成数据列表，[{},{}]  ---> 这是基础数据，所有的数据操作都在这个上面做
def generateDict(datalist, orgcode):
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
            dataDict[i[0]] = [i[0], i[1], orgcode, i[4],
                              i[4], i[5], i[5], i[-1], i[3], i[6], [tmpDict]]
        else:
            n = dataDict[i[0]][-1][-1]["workNo"]
            tmpDict2 = {
                "workNo": n + 1,
                "workDesc": '|'.join(str(i[7]).split('、')),
                "relaRiskCode": i[8],
                "relaRiskName": i[8],
                "relaSafeCode": i[9],
                "relaSafeDesc": i[9]
            }
            dataDict[i[0]][-1].append(tmpDict2)
    return dataDict


# 转换成 json
def dictToJson(datadict, code1, code2, code3, code4):
    tmpList = []
    for v in datadict.values():
        tmpDict = {}
        tmpDict["jsaCode"] = v[0]
        tmpDict["jsaName"] = ''.join(v[1].split())
        tmpDict["orgCode"] = v[2]
        tmpDict["relaMaterielCode"] = '|'.join(
            [code2[i] if i != "/" else "" for i in v[3].split('、') if i])
        tmpDict["relaMaterielName"] = v[3] if v[3] != "/" else ""
        tmpDict["relaToolCode"] = '|'.join([code1[i] for i in v[5].split('、') if i])
        tmpDict["relaToolName"] = '|'.join(v[6].split('、'))
        tmpDict["workplace"] = v[7]
        tmpDict["workAddress"] = v[8]
        tmpDict["workDesc"] = '|'.join(v[9].split('、'))

        # 替换 relaRiskCode，relaSafeCode  现在是个列表
        for i in v[-1]:
            i["relaRiskCode"] = '|'.join(
                [code3[j] for j in (re.sub(r'\d|\.', '', i) for i in i["relaRiskName"].split('\n')) if j])
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
def generateDictCode(datadict, index, orgcode):
    tmpList = []
    tmpDict = {}
    for v in datadict.values():
        tmpList += [i if i != "/" else "" for i in v[index].split("、")]
    for index, i in enumerate([i for i in set(tmpList) if i], 1):
        k = str(index).zfill(8)
        tmpDict[i] = orgcode + k
    return tmpDict


# 生成编码字典  --> 处理字典中的列表 relaRiskName
def generateDictCode2(datadict, fieldname, orgcode):
    tmpList = []
    tmpDict = {}
    for v in datadict.values():
        lastdata = v[-1]
        for i in lastdata:
            tmpList += [re.sub(r'\d|\.', '', i)
                        for i in str(i[fieldname]).split('\n')]
    for index, i in enumerate([i for i in set(tmpList) if i], 1):
        k = str(index).zfill(8)
        tmpDict[i] = orgcode + k
    return tmpDict


# 扫描目录下的文件
def scanDir(path):
    tmpList = []
    for i in os.listdir(path):
        _, ext = os.path.splitext(i)
        if ext == ".xls":
            tmpList.append(os.path.join(path, i))
    return tmpList


# [[]]
# 双列表数据处理

def twoList(tlist, dict):
    tmpList = []
    tmp1 = [i.split("|") for i in tlist]
    for i in tmp1:
        for j in i:
          if j:
            tmpList.append(dict[j])
    return "|".join(tmpList)

# 准备工具时被绊倒摔伤|准备工器具时手被挤伤，脚被砸伤|车辆伤害

def twoList2(tlist, dict):
    tmpList = []
    for i in tlist.split("|"):
        if i:
            tmpList.append(dict[i])
    return "|".join(tmpList)



# 处理风险数据关系
def extracData(orgcode, datadict, dict1, dict2):
    tmpList = []
    gList = []
    for v in datadict:
        tmpDict = {}
        relaRiskName = v[8]
        relaSafeDesc = v[9]
        len_relaRiskName = relaRiskName.split("\n")
        if  len(len_relaRiskName) < 2:
            k = re.sub(r'\d|\.', '', relaRiskName)
            if k:
                tmpDict[k] = [re.sub(r'\d|\.', '', i) for i in relaSafeDesc.split("\n") if i]
                tmpList.append(tmpDict)
        else:
            for index, data in enumerate([i for i in relaRiskName.split("\n") if i], 1):
                kk = re.sub(r'\d|\.', '', data)
                if kk:
                    tmpDict[kk] = [re.sub(r'\d|\.', '', i) for i in relaSafeDesc.split("\n") if "{}.".format(index) in i]
                    tmpList.append(tmpDict)
    for i in set(tmpList):
      print(i)
      for k, v in i.items():
          tDict = {}
          tmp = twoList2(k, dict1)
          tDict["RISK_CODE"] = tmp
          tDict["RISK_NAME"] = k
          tmp1 = twoList(v, dict2)
          tDict["RELA_SAFE_CODE"] = tmp1
          tmp2 = '|'.join([i for i in v])
          tDict["RELA_SAFE_DESC"] = tmp2
          tDict["ORG_CODE"] = orgcode
          tDict["DR"] = 0
          tDict["DATA_VERSION"] = 1
          tDict["DATA_NO"] = '{}{}'.format(getCurDate(), tmp)
          gList.append(tDict)
    

    return [dict(t) for t in set([tuple(d.items()) for d in gList])]


# 扫描文件 检查文件格式
def checkFileFormat(path):
    fileList = scanDir(path)
    for filename in fileList:
        data = readExcel(filename)
        gendata = fill(data)
        if not gendata:
            print('大哥呀文件格式好像有问题啊，检查下吧！！！ --->>{}'.format(filename))


# 请求数据
def post(url, data):
    headers = {
                "Content-Type":  "application/json"
            }
    http = httpx.post(url=url, data=data, headers=headers)
    print(http.text)
    return http.status_code


# 获取路径中最后一层文件名
def fastdir(path):
    _, tDir = os.path.split(path)
    return tDir


# 生成工器具请求报文数据
def genFormat(orgcode, codedict):

    tmpList = []
    for k, v in codedict.items():
        tmpDict = {
            "TOOL_CODE": k,
            "TOOL_NAME": v,
            "ORG_CODE": orgcode,
            "DR": 0,
            "DATA_VERSION": 1,
            "DATA_NO": '{}{}'.format(getCurDate(), k),
        }
        tmpList.append(tmpDict)
    return tmpList


def main():
    path = r"C:\Users\shil002\Desktop\ticket_env\1508"
    orgcode = fastdir(path)
    gendata = []
    fileList = scanDir(path)
    for filename in fileList:
        print('扫描文件---->>> {}'.format(filename))
        data = readExcel(filename)
        gendata += fill(data)
    gddata = generateDict(gendata, orgcode)

    # 工器具数据格式
    toolData = generateDictCode(gddata, 6, orgcode)
    # 物料数据格式  ---->>>>数据源有问题需要重新处理
    materielData = generateDictCode(gddata, 4, orgcode)

    # 安全措施数据格式
    riskData = generateDictCode2(gddata, "relaRiskName", orgcode)
    safeData = generateDictCode2(gddata, "relaSafeDesc", orgcode)

    gdd = dictToJson(gddata, toolData, materielData, riskData, safeData)

    #   ===========================================最大的那个json===============================================

    
    # l = len(gdd)
    # for i in range(int(l/10)+1):
    #     dataList = json.dumps(gdd[i*10:(i*10)+10])
    #     print(dataList)

        
    #     data = {
    #         "boName": "BO_EU_DEF_TOOL",
    #         "uid:": "admin",
    #         "recordDatas": dataList
    #     }
    #     print(data)
    #     print(post(r'http://127.0.0.1:8080/bd/jsa/batch/save', json.dumps(data)))
    #     time.sleep(0.5)
    #     break

    '''
    #  ------------------------------1-------------------------------
    for i in gdd:
        print(post(r'http://127.0.0.1:8080/bd/jsa/template/save', json.dumps(i)))

 #  ------------------------------2-------------------------------
    for k,v in toolData.items():
        toolJson = {
            "boName":"BO_EU_DEF_TOOL",
            "uid:":"admin",
            "recordDatas": [
              {"TOOL_CODE": v,
              "TOOL_NAME":k,
              "ORG_CODE":orgcode,
              "DATA_VERSION":1,
              "DR":0,
              "DATA_NO": getCurDate() + v}
            ]
        }
        print(post(r'http://127.0.0.1:8080/bd/jsa/batch/save', json.dumps(toolJson)))

     #  ------------------------------3-------------------------------
    for k,v in materielData.items():
        materielJson = {
            "boName":"BO_EU_DEF_MATERIEL",
            "uid:":"admin",
            "recordDatas": [
              {"MATERIEL_CODE": v,
              "MATERIEL_NAME":k,
              "ORG_CODE":orgcode,
              "DATA_VERSION":1,
              "DR":0,
              "DATA_NO": getCurDate() + v}
            ]
        }
        print(post(r'http://127.0.0.1:8080/bd/jsa/batch/save', json.dumps(materielJson)))
    '''
    #  ------------------------------4------------------------------- 
    print(len(extracData(orgcode, gendata, riskData, safeData)))
    for i in extracData(orgcode, gendata, riskData, safeData):
        riskJson = {
            "boName":"BO_EU_DEF_RISK",
            "uid:":"admin",
            "recordDatas": [i]
        }
        print(post(r'http://127.0.0.1:8080/bd/jsa/batch/save', json.dumps(riskJson)))
        break
    '''    
  
  #  ------------------------------5-------------------------------
    for k,v in safeData.items():
        safeJson = {
            "boName":"BO_EU_DEF_SAFETHING",
            "uid:":"admin",
            "recordDatas": [
              {"SAFE_CODE": v,
              "SAFE_DESC":k,
              "ORG_CODE":orgcode,
              "DATA_VERSION":1,
              "DR":0,
              "DATA_NO": getCurDate() + v,
            "BLN_IS_CONFIRM": 1,
            "BLN_IS_DELETE": 1,
            "BLN_IS_UPLOAD_FILE": 1,
            "BLN_IS_PHOTOGRAPH": 1,
            "BLN_IS_FILM_VIDEO": 1,
            "BLN_IS_SIGN": 1}
            ]
        }
        print(post(r'http://127.0.0.1:8080/bd/jsa/batch/save', json.dumps(safeJson)))
'''


if __name__ == "__main__":
    print(datetime.datetime.now())
    # profile.run("main()")
    # checkFileFormat(r"D:\learn\tmp\包化")
    main()
    print(datetime.datetime.now())
 