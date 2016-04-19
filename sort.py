
import os
import random
import heapq
from collections import deque
# str1, str2 : 15:58:00.364521
# 返回值
def compare_time(str1='', str2=''):
    if str1 == '':
        return 1
    if str2 == '':
        return -1
    idx1_1 = str1.find(':')
    idx2_1 = str2.find(':')
    tmp1 = int(str1[0:idx1_1]) # 比较小时
    tmp2 = int(str2[0:idx2_1]) #
    if tmp1 != tmp2:
        return tmp1 - tmp2
    idx1_2 = str1.find(':', idx1_1+1)
    idx2_2 = str2.find(':', idx2_1+1)
    tmp1 = int(str1[idx1_1+1 : idx1_2]) # 比较分钟
    tmp2 = int(str2[idx2_1+1 : idx2_2])
    if tmp1 != tmp2:
        return tmp1 - tmp2
    idx1_3 = str1.find('.', idx1_2+1)
    idx2_3 = str2.find('.', idx2_2+1)
    tmp1 = int(str1[idx1_2+1 : idx1_3]) # 比较剩下的时间值
    tmp2 = int(str2[idx2_2+1 : idx2_3])
    if tmp1 != tmp2:
        return tmp1 - tmp2
    tmp1 = int(str1[idx1_3+1 : idx1_3+7])
    tmp2 = int(str2[idx2_3+1 : idx2_3+7])
    if tmp1 != tmp2:
        return tmp1 - tmp2
    return 0

class path_node(object):
    def __init__(self, rindex=-1, fd=None, str_path=''):
        self.index = rindex # k th road
        self.filehandle = fd  # file handler
        self.path = str_path  # full path which is used to create filehandle
    def clear(self):
        self.road_idx = -1
        self.fd = None
        self.path = ''
    def __lt__(self, other):
        return compare_time(self.path, other.path) < 0
    def __eq__(self, other):
        return compare_time(self.path, other.path) == 0

# 返回特定/当前路径下的所有文件的完整路径
def getAllFiles(path=None):
    retlist = []
    curDir = os.getcwd()
    if path != None:
        curDir = os.path.join(curDir, path)
    #print(curDir)
    curFiles = os.listdir(curDir)
    for x in curFiles:
        x = os.path.join(curDir, x)
        if os.path.isfile(x) and x != '..' and x != '.':
            retlist.append(x)
            #print(x)
    #print(retlist)
    return retlist

# 得到完整路径的文件名
# fullpath 是一个 未处理过的完整路径的str
def getfilename(fullpath):
    return os.path.split(fullpath)[1]

# 得到文件名中的日期信息
# filename 是一个处理过的只剩文件名的str
def getfiledate(filename):
    return filename[:filename.find('-', # 第三个 -
                               filename.find('-', # 第二个 -
                                         filename.find('-')+1)+1)] # 第一个 -

# 得到 日期-路径 的映射集合
def daytoFiles(fileSet):
    dayset = {}
    print(fileSet)
    for x in fileSet:
        filename = getfilename(x)
        filedate = getfiledate(filename)
        if dayset.get(filedate) == None:
            dayset[filedate] = []
        dayset[filedate].append(x)
    return dayset

def add_head_date(date, filename):
    pass

# 合并的具体实现， k(=10)路归并
def kmerge(lists, date=''):
    if date != '':
        date += ' '
    files=[]        # 构建k路的文件名
    i = 0
    for i in range(0,10):
        try:
            files.append(lists.pop())
        except:
            break  # 不足10个就退出循环

    # 创建k路空链表，序号为 0 ~ 9
    kroad_list = []  #
    for j in range(0, i):
        kroad_list.append(deque())
    # 打开文件
    fd_list =[]
    for j in range(0, i):
        fd_list.append(open(files[j], 'r'))

    number_etimes = 10 # 当某路为空，读取10条记录进内存，放于指定位
    # 初始化每路10个记录
    for j in range(0, i):
        for k in range(0, 10):
            try: # 防止不够
                record = fd_list[j].readline().strip('\n')
                if record == '':
                    break
                print(record)
                kroad_list[j].append(path_node(j, files[j], record))
            except:
                break

    #创建合并的文件
    x = 'merge'
    merge_path = os.path.join(os.getcwd(), x)
    while os.path.exists(merge_path):
        x += str(1)
        merge_path = os.path.join(os.getcwd(), x)
    merge_fd = open(merge_path, 'a')

    priority = []
    empty_file = i+1 # 一共i+1 个文件
    # 插入i个到堆中
    for j in range(0, i):
        if len(kroad_list[j]) > 0:
            single = kroad_list[j].popleft()  # O(1)
            heapq.heappush(priority, single)
        else:
            try:
                line = fd_list[j].readline().strip('\n')
                if line == '':
                    continue
                kroad_list[j].append(path_node(j, files[j] , line))
            except:
                empty_file -= 1
                continue

    while len(priority) > 0:
        pop = heapq.heappop(priority)
        pop_index = pop.index
        if len(kroad_list[pop_index]) > 0:      # 如果内存中第 k 路还有数据，取出来压入堆中
            heapq.heappush(priority, kroad_list[pop_index].popleft())
        else: # 如果没有数据了，就在读十条
            for j in range(0, 10):
                try:
                    line = fd_list[pop_index].readline().strip('\n')
                    if line == '':
                        break
                    kroad_list[pop_index].append(path_node(pop_index, files[pop_index], ))
                    heapq.heappush(priority, kroad_list[pop_index].popleft())
                except:
                    break
        print('pop index: %d ' %pop_index, ' for %s' %pop.path)
        merge_fd.write(date + pop.path + '\n')
    # 关闭文件
    for j in range(0, i):
        fd_list[j].close()
    merge_fd.close()
    return lists

# 合并文件
def merge(date, pathlist=list()):
    # 已经带日期的文件
    merge_list = []
    #合并所有同日期的文件
    while len(pathlist) > 0:
        merge_list.append(kmerge(pathlist, date))
    # 假设有21个同日期的文件，就会有3个已经带日期的文件生成
    while len(merge_list) > 1:
        merge_list.append(kmerge(merge_list))

filelist = getAllFiles() # filelist 是一个包含完整路径的 list
datedict = daytoFiles(filelist) #datedict 是一个包含 日期-列表 的键值对
for eachday in datedict.items():
    merge(eachday[0], eachday[1])