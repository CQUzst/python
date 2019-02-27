a_list = [1,2,3,4,5,6,7,8]

d1 = {'apple':1, 'pear':2, 'orange':3}
d2 = {1:'a', 2:'b', 3:'c'}
d3 = {1:'a', 'b':2, 'c':3}

print(d1['apple'])  # 1
print(a_list[0])    # 1

del d1['pear']
print(d1)   # {'orange': 3, 'apple': 1}

d1['b'] = 20
print(d1)   # {'orange': 3, 'b': 20, 'pear': 2, 'apple': 1}

def func():
    return 0

d4 = {'apple':[1,2,3], 'pear':{1:3, 7:'a'}, 'orange':func}
print(d4['pear'][7])    # a 字典里的字典
