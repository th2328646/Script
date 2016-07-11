#!/usr/bin/env python
# coding=utf-8

from ConfigParser import ConfigParser
from xlutils.copy import copy
from xlrd import open_workbook
import os
import xlrd
import xlwt
import MySQLdb
import time
import subprocess

CONFIGFILE = "report_service_2_0.ini"
config = ConfigParser()
config.read(CONFIGFILE)

nowTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

dbHost = config.get("DB", "_host")
dbUser = config.get("DB", "_user")
dbPassword = config.get("DB", "_password")
dbDatabase = config.get("DB", "_database")
dbPort = config.getint("DB", "_port")
SQL_childrenDept = config.get("SQL", "_childrenDept")

db = MySQLdb.connect(dbHost, dbUser, dbPassword, dbDatabase, dbPort, charset="utf8")
cs = db.cursor()

def execute_SQL(sql):
    cs.execute(sql)
    result = cs.fetchall()
    return result

def getChildren(id):
    cs.execute(SQL_childrenDept % id)
    result = cs.fetchall()
    return result
    
def subThisDept(id):
    tup = getChildren(id)
    arr = []
    for i in range(len(tup)):
        arr.append(tup[i][0])
    return arr
    
arrSubCCWY = subThisDept(1)
tupSubCCWY = getChildren(1)
for i in range(len(tupSubCCWY)):
    if (tupSubCCWY[i][1] == u'\u5fae\u8d37\u7f51'):
        arrSubWD = subThisDept(tupSubCCWY[i][0])
    elif (tupSubCCWY[i][1] == u'\u7fa4\u7855'):
        arrSubQS = subThisDept(tupSubCCWY[i][0])
    
online = config.get("SQL", "_online")
offline = config.get("SQL", "_offline")
closed = config.get("SQL", "_closed")
intotal = config.get("SQL", "_intotal")
countOne = [online, offline, closed, intotal]
def count(departmentId):
    data = []
    deptId = ""
    if (isinstance(departmentId, list)):
        deptId = ",".join(map(str, departmentId))
    elif (isinstance(departmentId, long) or isinstance(departmentId, int)):
        deptId = str(departmentId)
    for i in countOne:
        cs.execute(i % deptId)
        result = cs.fetchone()
        row = int(result[0])
        data.append(row)
    return data    

oldExcelName = config.get("FILE", "_oldExcelName")
newExcelName = config.get("FILE", "_newExcelName")
subprocess.call(["cp", oldExcelName, newExcelName])

excelPath = config.get("FILE", "_newExcelName")
openworkbook = xlrd.open_workbook(excelPath, formatting_info=True)
wb = copy(openworkbook) 
SHEET = wb.get_sheet(0)

#定义样式
font1 = xlwt.Font()
font1.colour_index = 2
#excel单元格边框
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1
borders.bottom_colour = 0x3A
#居中(horz:水平，vert垂直)
alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER 
alignment.vert = xlwt.Alignment.VERT_CENTER
#默认字体
STYLE_BLACK = xlwt.XFStyle()
STYLE_BLACK.borders = borders
#红色字体
STYLE_RED = xlwt.XFStyle()
STYLE_RED.borders = borders 
STYLE_RED.alignment = alignment
STYLE_RED.font = font1

COUNTER = 0
ALLChildrenDict = {}
ALLChildrenDictName = ""
ALLChildrenArr = []
SHEET.write(0 , 11 , nowTime)

def wtExcelForCount(tup, name):
    global COUNTER, SHEET, STYLE_BLACK, STYLE_RED, arrSubCCWY, arrSubWD, arrSubQS
    SHEET.write(COUNTER + 3 , 0 , COUNTER , STYLE_BLACK)
    SHEET.write(COUNTER + 3 , 1 , "" , STYLE_BLACK)
    SHEET.write(COUNTER + 3 , 2 , "" , STYLE_BLACK)
    SHEET.write_merge(COUNTER + 3, COUNTER + 3, 3, 4, "", STYLE_BLACK)
    data = []
    if (isinstance(tup, list)):
        data = count(tup)
        cellValue = name + u'\uff08\u603b\uff09'
        SHEET.write_merge(COUNTER + 3, COUNTER + 3, 1, 4, cellValue, STYLE_RED)
    elif (isinstance(tup, tuple)):
        data = count(tup[0])
        if (tup[0] in arrSubCCWY):
            SHEET.write(COUNTER + 3 , 1 , tup[1] , STYLE_RED)
        elif (tup[0] in arrSubWD or tup[0] in arrSubQS):
            SHEET.write(COUNTER + 3 , 2 , tup[1] , STYLE_BLACK)
        else :
            SHEET.write_merge(COUNTER + 3, COUNTER + 3, 3, 4, tup[1], STYLE_BLACK)
    SHEET.write(COUNTER + 3, 5, data[0], STYLE_BLACK)
    SHEET.write(COUNTER + 3, 6, data[1], STYLE_BLACK)
    SHEET.write(COUNTER + 3, 7, data[2], STYLE_BLACK)
    SHEET.write(COUNTER + 3, 8, data[3], STYLE_BLACK)
    SHEET.write(COUNTER + 3, 9, "", STYLE_BLACK)
    SHEET.write(COUNTER + 3, 10, "", STYLE_BLACK)
    SHEET.write_merge(COUNTER + 3, COUNTER + 3, 11, 12, "", STYLE_BLACK)

def editExcel(allChildren):
    global COUNTER, arrSubCCWY, ALLChildrenDict, ALLChildrenArr, ALLChildrenDictName
    COUNTER += 1
    print COUNTER
    for i in range(len(allChildren)):
        if (allChildren[i][0] in arrSubCCWY):
            if (ALLChildrenArr != "[]"):
                ALLChildrenDict[ALLChildrenDictName] = ALLChildrenArr
                ALLChildrenDictName = allChildren[i][1]
            else:
                ALLChildrenDictName = allChildren[i][1]
            ALLChildrenArr = []
            
        thisChild = getChildren(allChildren[i][0])
        if(thisChild == "()"):
            wtExcelForCount(allChildren[i], "")
            ALLChildrenArr.append(allChildren[i][0])
        else:
            wtExcelForCount(allChildren[i], "")
            ALLChildrenArr.append(allChildren[i][0])
            editExcel(getChildren(allChildren[i][0]))
    ALLChildrenDict[ALLChildrenDictName] = ALLChildrenArr
            
editExcel(getChildren(1));

wtExcelForCount(ALLChildrenDict[u'\u5fae\u8d37\u7f51'], u'\u5fae\u8d37\u7f51')
COUNTER += 1
wtExcelForCount(ALLChildrenDict[u'\u7fa4\u7855'], u'\u7fa4\u7855')

os.remove(newExcelName)
wb.save(newExcelName)

cs.close()
db.close()
