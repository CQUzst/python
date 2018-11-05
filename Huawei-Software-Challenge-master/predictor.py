#-*- coding: UTF-8 -*-
import random

def predict_vm(ecs_lines, input_lines):
    # Do your work from here
    #创建全年日期列表
    createDateList()
    #获得训练集数据
    dataSet, train_start, train_end = getDataSet(ecs_lines)
    #获得输入文件信息，物理服务器的CPU,RAM，虚拟机的总数，型号，要求优化的内容，预测开始和结束时间
    cpu, arm, flavor_num, flavor_set, CPUorRAM, prediction_start, \
    prediction_end,predict_days = getInputSet(input_lines)
    # 创建训练集中所对应的日期
    date1 = createDateSet1(dataSet)
    #将训练集所缺失的日期补全
    date2 = createDateSet2(train_start, train_end)
    #print "date2"+str(date2)
    #创建列表，列表内容为每天所对应的第i个虚拟机的个数
    fla_num_days,not_zero_average,no_clear_fla_num_days = countFlaNumDays(dataSet, date1, date2, flavor_set)
    print "fla_num_days="
    print len(fla_num_days)

    print "not zero average"
    print not_zero_average
    no_clear_near_result=getNearResult(no_clear_fla_num_days, prediction_start, prediction_end)
    near_result=getNearResult(fla_num_days, prediction_start, prediction_end)
    print "near_result"
    print near_result

    print "no_clear_near_result"
    print no_clear_near_result

    train_s=train_count(fla_num_days, prediction_start, prediction_end)
    # print "train_s="
    # print train_s
    train_days = len(train_s[0])
    print "train_days"
    print train_days

    predict_answer=AR(train_s, predict_days,not_zero_average,near_result,no_clear_near_result)
    result = outputTxt(cpu, arm, flavor_set,predict_answer)
    print "result"
    print result
    output = result
    f = open('output.txt', 'w')
    f.write(str(output))
    f.close()
    #print "output="+str(output)
    return output

#创建全年日期列表
def createDateList():
    f = open('dateList.txt','w')
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    month1 = ['01','03','05','07','08','10','12']
    month2 = ['04','06','09','11']
    strs = ''
    for a in month:
        if a in month1:
            b = 31
        elif a in month2:
            b = 30
        else:
            b = 28
        for i in range(b):
            if i < 9:
                strs += a + '-0' + str(i+1) + '\n'
            else:
                strs += a + '-' + str(i+1) + '\n'
    f.write(strs)
    f.close()
#获得训练集数据
def getDataSet(ecs_lines):
    f = ecs_lines
    dataSet = []
    for line in f:
        line = line.strip('\n')
        lineArr = line.strip().split()

        dataSet.append([int(lineArr[1].lstrip('flavor')),lineArr[2]])
    # print "dataSet"
    # print dataSet
    train_start = dataSet[0][1]
    train_end = dataSet[-1][1]
    # print train_start
    # print train_end
    return dataSet,train_start,train_end
#获得输入文件信息，物理服务器的CPU,RAM，虚拟机的总数，型号，要求优化的内容，预测开始和结束时间
def getInputSet(input_lines):
    fileSet = input_lines
    #fileSet = input_lines.readlines()
    cpu = int(fileSet[0].strip().split()[0])
    ram = int(fileSet[0].strip().split()[1])
    flavor_num = int(fileSet[2].strip().split()[0])
    flavor_set = []
    for i in range(3,flavor_num +3):
        flavor_set.append(int(fileSet[i].strip().split()[0].lstrip('flavor')))
    CPUorRAM = fileSet[flavor_num +4].strip().split()[0]
    prediction_start = fileSet[flavor_num +6].strip().split()[0]
    prediction_end = fileSet[flavor_num +7].strip().split()[0]
    predict_days = len(createDateSet2(prediction_start, prediction_end)) - 1
    print "prediction_end"
    print prediction_end
    return cpu,ram,flavor_num,flavor_set,CPUorRAM,prediction_start,prediction_end,predict_days
#创建训练集中所对应的日期
def createDateSet1(dataSet):
    date = set([])
    for d in dataSet:
        date.add(d[1])
    return sorted(list(date))
#将训练集所缺失的日期补全
def createDateSet2(startDate,endDate):
    date = []
    a = startDate[0:5]
    f = open('dateList.txt')
    flag = False
    for line in f.readlines():
        i = line.strip()
        if i == startDate[5:]:
            flag = True
        if i == endDate[5:]:
            flag = False
            date.append(a+i)
        if flag:
            date.append(a+i)
    return date
#创建列表，列表内容为每天所对应的第i个虚拟机的个数
def countFlaNumDays(dataSet, date1, date2, fla_set):
    fla_num_days = []

    #fla_set需要预测的虚拟机的型号集合
    a = len(fla_set)
    for date in date2:
        labelSet = [0]*a
        if date in date1:
            for data in dataSet:
                #data[0]表示天对应的虚拟机型号
                if data[0] in fla_set :
                    if data[1] == date:
                        labelSet[fla_set.index(data[0])] += 1
        fla_num_days.append(labelSet)
    no_clear_fla_num_days=[]
    a = len(fla_set)
    for date in date2:
        labelSet = [0] * a
        if date in date1:
            for data in dataSet:
                # data[0]表示天对应的虚拟机型号
                if data[0] in fla_set:
                    if data[1] == date:
                        labelSet[fla_set.index(data[0])] += 1
        no_clear_fla_num_days.append(labelSet)

    # 去噪
    # print "fla_num_days[0]"
    # print fla_num_days
    # print "len(fla_num_days"
    # print len(fla_num_days[0])
    not_zero_average=[]
    for i in range(len(fla_num_days[0])):
        sums = 0
        cou = 0
        for x in fla_num_days:
            if x[i] != 0:
                sums += x[i]
                cou += 1
        average = sums / cou
        not_zero_average.append(average)
        for j in range(len(fla_num_days)):
            if fla_num_days[j][i] >= average * 4:
                fla_num_days[j][i] = average
            if fla_num_days[j][i] == 0:
                fla_num_days[j][i] +=random.choice(range(100))/1010.0
    # print "not zero average"
    # print not_zero_average

    return fla_num_days,not_zero_average,no_clear_fla_num_days

#训练统计
def train_count(fla_num_days, prediction_start, prediction_end):
    #统计需要预测的时间长度
    predict_days = len(createDateSet2(prediction_start,prediction_end))-1

    # 统计训练集的时间长度
    trainData_days = len(fla_num_days)
    # print fla_num_days
    # print trainData_days


    #训练集的虚拟机直接累加
    train_sum=[]
    for k in range (len(fla_num_days)-predict_days+1):
        count=[]
        for j in range(len(fla_num_days[0])):
            count1 = 0
            for i in range(k,predict_days+k):
                count1 += fla_num_days[i][j]
            count.append(count1)
        train_sum.append(count)
    # print "train_sum"
    # print train_sum

    flavor_i=[]
    for i in range (len(train_sum[0])):
        aa=[]
        for j in range (len(train_sum)):
            aa.append(train_sum[j][i])
        flavor_i.append(aa)
    #print flavor_i
    return flavor_i

def getNearResult(fla_num_days, prediction_start, prediction_end):

    # 统计需要预测的时间长度
    predict_days = len(createDateSet2(prediction_start, prediction_end)) - 1
    # 统计训练集的时间长度
    trainData_days = len(fla_num_days)
    # 训练集的虚拟机直接累加
    train_sum = []
    for k in range(len(fla_num_days[0])):
        count = 0
        for i in range(trainData_days):
            if (i >= int(trainData_days - predict_days)):
                count += fla_num_days[i][k]
        train_sum.append(count)

    predic_flavors = [0] * len(train_sum)
    for i in range(len(train_sum)):
        predic_flavors[i] = train_sum[i] / ((predict_days) * 1.0) * predict_days
        if (int(predic_flavors[i] + 0.5) == int(predic_flavors[i])):
            predic_flavors[i] = int(predic_flavors[i])
        else:
            predic_flavors[i] = int(predic_flavors[i]) + 1
    # print "predic_flavors"+str(predic_flavors)
    return predic_flavors

#矩阵求逆
def matrix_ni(matrix):
    add_matrix = matrix
    l = len(matrix)
    for i in range(0, l):
        add_matrix[i].extend([0] * i)
        add_matrix[i].extend([1])
        add_matrix[i].extend([0] * (l - i - 1))
    for i in range(0, len(add_matrix)):
        if add_matrix[i][i] == 0:
            for j in range(i, len(add_matrix)):
                if add_matrix[j][i] != 0:
                    add_matrix[i], add_matrix[j] = add_matrix[j], add_matrix[i]
                    break
            if j >= len(add_matrix):
                return 0
            break
    for i in range(0, len(add_matrix)):
        f = add_matrix[i][i]
        for j in range(0, len(add_matrix[i])):
            add_matrix[i][j] /= f
        for m in range(0, len(add_matrix)):
            if m == i:
                continue
            ccc = add_matrix[m][i]
            for n in range(0, len(add_matrix[i])):
                add_matrix[m][n] -= add_matrix[i][n] * ccc
    for i in range(0, len(add_matrix)):
        add_matrix[i] = add_matrix[i][l:]
    return add_matrix


def AR (train_s,predict_days,not_zero_average,near_result,no_clear_near_result):
    predict_answer=[]
    for i in range (len(train_s)):
        #print train_s[i]
        w=AR_test(train_s[i],len(train_s[0]))
        answer=predict(train_s[i],w,predict_days)
        predict_answer.append(answer)
    for i in range(len(predict_answer)):
        if (int(predict_answer[i] + 0.5) == int(predict_answer[i])):
            predict_answer[i] = int(predict_answer[i])
        else:
            predict_answer[i] = int(predict_answer[i]) + 1
    print "AR predict answer:"
    print predict_answer

    for i in range(len(predict_answer)):
        #突增判定
        if(no_clear_near_result[i]>not_zero_average[i]*3):
            predict_answer[i]=no_clear_near_result[i]
            continue
        if(predict_answer[i]>(no_clear_near_result[i]-3)
                              and predict_answer[i]<(no_clear_near_result[i]+3)):
            if (predict_answer[i] <no_clear_near_result[i]):
                predict_answer[i]+=1
                continue
            if (predict_answer[i] > no_clear_near_result[i]):
                predict_answer[i] -= 1
                continue
        if(predict_answer[i]>no_clear_near_result*2):
            predict_answer[i]+=int((predict_answer[i]-near_result[i])/2.0)
            continue
    for i in range(len(predict_answer)):
        if(predict_answer[i]==0):
            predict_answer[i] = near_result[i]
    for i in range(len(predict_answer)):
        if(not_zero_average[i]==1 and no_clear_near_result[i]==0):
            predict_answer[i] = 0

    print "fix answer:"
    print predict_answer
    return predict_answer

def AR_test(x,N,p=9):
    gamma = [[0 for i in range(p+1)] for i in range(p+1)]
    for i in range(p+1):
        for j in range(i,p+1):
            # 点乘并求均值
            sum = 0
            #print x[p-i]
            for k in range(N-p):
                sum += x[p-i+k]*x[p-j+k]
            gamma[i][j] = float(sum)/(N-p)
            gamma[j][i] = gamma[i][j]
    #print ["gamma", gamma]
    v = [0]*p
    mat = [[0 for i in range(p)] for i in range(p)]
    for i in range(p):
        v[i] = gamma[i+1][0]
    for i in range(p):
        for j in range(p):
            mat[i][j] = gamma[i+1][j+1]
    retv = [mat,v]
    #print(retv[0])
    # 求逆、矩阵相乘
    imat = matrix_ni(retv[0])
    w = []
    for i in range(p):
        a = 0
        for j in range(p):
            a += v[j]*imat[j][i]
        w.append(a)
    return w

def predict(x,w,predict_days,p=9):
    result = x[-p:]
    # print "result"
    # print result
    for i in range(predict_days):
        a = 0
        for j in range(p):
            a += w[j]*result[i+p-1-j]
        result.append(a)
    # print "result[-1]"
    # print result[-1]
    if (result[-1]>50):
        result[-1]=0
    if (result[-1] <0):
        result[-1] =0
    return result[-1]


# return result
def outputTxt(cpu, arm, fla_set, predict_answer):
    lay_data = [[1, 1, 1], [2, 1, 2], [3, 1, 4], [4, 2, 2], [5, 2, 4], [6, 2, 8], [7, 4, 4], [8, 4, 8],
                [9, 4, 16], [10, 8, 8], [11, 8, 16], [12, 8, 32], [13, 16, 16], [14, 16, 32], [15, 16, 64]]
    count = predict_answer
    # 放置
    count_copy = count[:]
    fla_cpu = [lay_data[x - 1][1] for x in fla_set]
    fla_arm = [lay_data[x - 1][2] for x in fla_set]
    p_cpu = sum([count_copy[x] * fla_cpu[x] for x in range(len(count_copy))])
    p_arm = sum([count_copy[x] * fla_arm[x] for x in range(len(count_copy))])
    k2 = max(p_cpu / cpu, p_arm / arm) + 1
    #print p_cpu, p_arm, k2
    a = [[0 for i in range(len(fla_set))] for j in range(k2)]
    n = len(fla_set) - 1
    flag = True
    while flag:
        flag1 = 0
        for i in range(k2):
            b = 0
            b1 = 0
            c = 0
            c1 = 0
            for j in range(len(a[i])):
                b += a[i][j] * lay_data[fla_set[j] - 1][1]
                c += a[i][j] * lay_data[fla_set[j] - 1][2]
            a[i][n] += 1
            for j in range(len(a[i])):
                b1 += a[i][j] * lay_data[fla_set[j] - 1][1]
                c1 += a[i][j] * lay_data[fla_set[j] - 1][2]
            a[i][n] -= 1
            if (b <= cpu and b1 > cpu) or (c <= arm and c1 > arm):
                flag1 += 1
                if flag1 == k2:
                    flag = False
                    break
                continue
            if count_copy[-1] != 0:
                a[i][n] += 1
                count_copy[-1] -= 1
            else:
                count_copy = count_copy[:-1]
                n -= 1
            if count_copy == []:
                flag = False
                break
    count_put = []
    for i in range(len(a[0])):
        C = 0
        for j in range(len(a)):
            C += a[j][i]
        count_put.append(C)
    #print count_put
    k3 = sum(count_put)
    fla_set_set = []
    for i in range(len(count_put)):
        fla_set_set.append('flavor' + str(fla_set[i]) + ' ' + str(count_put[i]))
    layout_set = []
    for i in range(k2):
        layout_strs = str(i + 1)
        d1 = 0
        d2 = 0
        for j in range(len(fla_set)):
            if a[i][j] != 0:
                d1 += a[i][j] * lay_data[fla_set[j] - 1][1]
                d2 += a[i][j] * lay_data[fla_set[j] - 1][2]
                layout_strs += ' flavor' + str(fla_set[j]) + ' ' + str(a[i][j])
        #print str(i + 1) + '  ' + str(cpu) + ':' + str(d1) + '  ' + str(arm) + ':' + str(d2)
        layout_set.append(layout_strs)

    result = [k3] + fla_set_set + [''] + [k2] + layout_set
    cpu_rate = float(p_cpu) / (cpu * k2)
    arm_rate = float(p_arm) / (arm * k2)
    #print('cpu_rate:%f ,arm_rate:%f' % (cpu_rate, arm_rate))
    return result