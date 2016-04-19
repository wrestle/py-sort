
import os
import random
import heapq
from collections import deque
# str1, str2 : 15:58:00.364521
# ����ֵ
def compare_time(str1='', str2=''):
    if str1 == '':
        return 1
    if str2 == '':
        return -1
    idx1_1 = str1.find(':')
    idx2_1 = str2.find(':')
    tmp1 = int(str1[0:idx1_1]) # �Ƚ�Сʱ
    tmp2 = int(str2[0:idx2_1]) #
    if tmp1 != tmp2:
        return tmp1 - tmp2
    idx1_2 = str1.find(':', idx1_1+1)
    idx2_2 = str2.find(':', idx2_1+1)
    tmp1 = int(str1[idx1_1+1 : idx1_2]) # �ȽϷ���
    tmp2 = int(str2[idx2_1+1 : idx2_2])
    if tmp1 != tmp2:
        return tmp1 - tmp2
    idx1_3 = str1.find('.', idx1_2+1)
    idx2_3 = str2.find('.', idx2_2+1)
    tmp1 = int(str1[idx1_2+1 : idx1_3]) # �Ƚ�ʣ�µ�ʱ��ֵ
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

# �����ض�/��ǰ·���µ������ļ�������·��
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

# �õ�����·�����ļ���
# fullpath ��һ�� δ�����������·����str
def getfilename(fullpath):
    return os.path.split(fullpath)[1]

# �õ��ļ����е�������Ϣ
# filename ��һ���������ֻʣ�ļ�����str
def getfiledate(filename):
    return filename[:filename.find('-', # ������ -
                               filename.find('-', # �ڶ��� -
                                         filename.find('-')+1)+1)] # ��һ�� -

# �õ� ����-·�� ��ӳ�伯��
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

# �ϲ��ľ���ʵ�֣� k(=10)·�鲢
def kmerge(lists, date=''):
    if date != '':
        date += ' '
    files=[]        # ����k·���ļ���
    i = 0
    for i in range(0,10):
        try:
            files.append(lists.pop())
        except:
            break  # ����10�����˳�ѭ��

    # ����k·���������Ϊ 0 ~ 9
    kroad_list = []  #
    for j in range(0, i):
        kroad_list.append(deque())
    # ���ļ�
    fd_list =[]
    for j in range(0, i):
        fd_list.append(open(files[j], 'r'))

    number_etimes = 10 # ��ĳ·Ϊ�գ���ȡ10����¼���ڴ棬����ָ��λ
    # ��ʼ��ÿ·10����¼
    for j in range(0, i):
        for k in range(0, 10):
            try: # ��ֹ����
                record = fd_list[j].readline().strip('\n')
                if record == '':
                    break
                print(record)
                kroad_list[j].append(path_node(j, files[j], record))
            except:
                break

    #�����ϲ����ļ�
    x = 'merge'
    merge_path = os.path.join(os.getcwd(), x)
    while os.path.exists(merge_path):
        x += str(1)
        merge_path = os.path.join(os.getcwd(), x)
    merge_fd = open(merge_path, 'a')

    priority = []
    empty_file = i+1 # һ��i+1 ���ļ�
    # ����i��������
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
        if len(kroad_list[pop_index]) > 0:      # ����ڴ��е� k ·�������ݣ�ȡ����ѹ�����
            heapq.heappush(priority, kroad_list[pop_index].popleft())
        else: # ���û�������ˣ����ڶ�ʮ��
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
    # �ر��ļ�
    for j in range(0, i):
        fd_list[j].close()
    merge_fd.close()
    return lists

# �ϲ��ļ�
def merge(date, pathlist=list()):
    # �Ѿ������ڵ��ļ�
    merge_list = []
    #�ϲ�����ͬ���ڵ��ļ�
    while len(pathlist) > 0:
        merge_list.append(kmerge(pathlist, date))
    # ������21��ͬ���ڵ��ļ����ͻ���3���Ѿ������ڵ��ļ�����
    while len(merge_list) > 1:
        merge_list.append(kmerge(merge_list))

filelist = getAllFiles() # filelist ��һ����������·���� list
datedict = daytoFiles(filelist) #datedict ��һ������ ����-�б� �ļ�ֵ��
for eachday in datedict.items():
    merge(eachday[0], eachday[1])