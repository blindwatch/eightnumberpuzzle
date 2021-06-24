import tkinter
import time
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

direction = [[1, 3], [1, 2, 3], [1, 2], [0, 1, 3], [0, 1, 2, 3], [0, 1, 2], [0, 3], [0, 2, 3], [0, 2]] #九个位置的移动方向
round = np.array([0, 1, 2, 5, 8, 7, 6, 3])  #顺时针一圈
target = np.array([1,2,3,8,0,4,7,6,5])
control = 'type 1'      #启发函数
it_limit = 1000     #最大迭代次数
color=['white', 'brown', 'burlywood', 'cadetblue', 'coral', 'beige', 'cornflowerblue', 'crimson', 'aquamarine'] #每个数字对应颜色
reset = ['1', '2', '3', '8', '', '4', '7', '6', '5']    #重置默认状态
root_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]        #初始状态
resolve = []        #解答路径
st = 0      #搜索次数

'''
节点结构体
'''
class node:
    def __init__(self, num, data, father, score=0):
        self.pattern = data
        self.space = list(np.where(data==0)[0])[0]
        self.num = num
        self.father = father
        self.score = score

'''
移动方块
'''
def switch(pattern, direct):
    index = list(np.where(pattern == 0))[0]
    x = np.copy(pattern)
    if direct == 0: #上
        x[index] = x[index - 3]
        x[index - 3] = 0
    elif direct == 1:  #下
        x[index] = x[index + 3]
        x[index + 3] = 0
    elif direct == 2:  #左
        x[index] = x[index - 1]
        x[index - 1] = 0
    else:   #右
        x[index] = x[index + 1]
        x[index + 1] = 0
    return x

'''
检查问题有没有解
'''
def check_state(start):
    count = 0
    for i in range(1, len(start)):
        if not start[i] == 0:
            for j in range(i):
                if start[j] > start[i]:
                    count = count + 1
    if count % 2 != 0:
        return 0
    else:
        return 1

'''
检测pattern是否存在，避免死循环
'''
def isexist(x, list_e):
    for i in range(len(list_e)):
        c = (x == list_e[i].pattern)
        if c.all():
            return 1
    return 0

'''
启发函数
'''
def score_function(pattern, control):
    global target
    global direction
    global round
    if control == 'type 1':
        count = 0
        for i in range(len(pattern)):
            if pattern[i] != 0 and pattern[i] != target[i]:
                count = count + 1
        return count
    if control == 'type 2':
        count = 0
        for i in range(len(pattern)):
            if pattern[i] != 0:
                tari = np.where(target.reshape(3, -3) == pattern[i])[0]
                tarj = np.where(target.reshape(3, -3) == pattern[i])[1]
                count += abs(tari - int(i / 3)) + abs(tarj - i % 3)
        return count
    elif control == 'type 3':
        count = 0
        '''
        for i in range(len(pattern)):
            if pattern[i] != 0 and pattern[i] != target[i]:
                for direct in direction[i]:
                    if direct == 0:  # 上
                        test = pattern[i - 3]
                    elif direct == 1:  # 下
                        test = pattern[i + 3]
                    elif direct == 2:  # 左
                        test = pattern[i - 1]
                    else:  # 右
                        test = pattern[i + 1]
                    if test != 0 and test == target[i] and i == np.where(target == test)[0]:
                        count += 1
        '''
        for i in range(1, len(round)):
            if pattern[round[i]] < pattern[round[i-1]]:
                count += 2
        return count
    elif control == 'type 4':
        count = 0
        for i in range(len(pattern)):
            if pattern[i] != 0 and pattern[i] != target[i]:
                count = count + 1
        '''
                for direct in direction[i]:
                    if direct == 0:  # 上
                        test = pattern[i - 3]
                    elif direct == 1:  # 下
                        test = pattern[i + 3]
                    elif direct == 2:  # 左
                        test = pattern[i - 1]
                    else:  # 右
                        test = pattern[i + 1]
                    if test != 0 and test == target[i] and i == np.where(target == test)[0]:
                        count += 1
        '''
        for i in range(1, len(round)):
            if pattern[round[i]] < pattern[round[i-1]]:
                count += 3
        return count
    elif control == 'type 5':
        count = 0
        for i in range(len(pattern)):
            if pattern[i] != 0 and pattern[i] != target[i]:
                count = count + 1
            if pattern[i] != 0:
                tari = np.where(target.reshape(3, -3) == pattern[i])[0]
                tarj = np.where(target.reshape(3, -3) == pattern[i])[1]
                count += abs(tari - int(i / 3)) + abs(tarj - i % 3)
        return count


'''
插入排序重排open表
'''
def reorganize(openlist, nnode):
    if len(openlist) == 0:
        openlist.append(nnode)
    else:
        for i in range(len(openlist)):
            if nnode.score < openlist[i].score:
                openlist.insert(i, nnode)
                return
        openlist.append(nnode)
        return


'''
求解八数码问题
'''
def solver(start_state):
    global direction
    global it_limit
    global target
    nodetree = []
    open = []
    close = []
    resol = []
    state = 0
    if check_state(start_state) == 1:
        state = 1
        return resol, state
    root = node(0, start_state, -1)
    open.append(root)
    nodetree.append(root)
    print("root state is:\n {}".format(root.pattern.reshape(3,3)))
    flag = 0
    times =0
    while len(open) > 0 and flag == 0:
        temp = open.pop(0)
        close.append(temp)
        for i in direction[temp.space]:
            newpattern = switch(temp.pattern, i)
            if not isexist(newpattern, nodetree):
                newnode = node(len(nodetree), newpattern, temp.num, score_function(newpattern, control))
                nodetree.append(newnode)
                reorganize(open, newnode)
            if (newpattern == target).all():
                trace = newnode
                resol.insert(0, trace)
                while trace.father > -1:
                    trace = nodetree[trace.father]
                    resol.insert(0, trace)
                flag = 1
                break
        times += 1
        if times > it_limit:
            flag = 2
            break
    if flag == 0:
        state = -1
        return resol, state, times
    elif flag == 1:
        return resol, state, times
    else:
        state = 2
        return resol, state, times
    #for i in range(len(resol)):
     #   print('第{}次走动:\n{}'.format(i, resolve[i].pattern.reshape(3,3)))

'''
设置初始状态
'''
def set_root():
    global root_state
    root_state = [int(i) for i in s.get()]
    for i in range(len(root_state)):
        if root_state[i] == 0:
            mlist[i].set('')
            malist[i].config(bg=color[0])
        else:
            mlist[i].set(str(root_state[i]))
            malist[i].config(bg=color[root_state[i]])
    return

'''
重置初始状态
'''
def clr_root():
    global root_state
    global resolve
    resolve = []
    z.set('')
    s.set('请输入初始状态')
    for i in range(len(root_state)):
        root_state[i] = 0
        mlist[i].set(reset[i])
        if reset[i] != '':
            malist[i].config(bg=color[int(reset[i])])
        else:
            malist[i].config(bg=color[0])
    return

'''
设置随机初始状态
'''
def random_set():
    global root_state
    a = np.arange(9)
    np.random.shuffle(a)
    root_state = list(a)
    s.set(''.join(str(i) for i in root_state))
    for i in range(len(root_state)):
        if root_state[i] == 0:
            mlist[i].set('')
            malist[i].config(bg=color[0])
        else:
            mlist[i].set(str(root_state[i]))
            malist[i].config(bg=color[root_state[i]])
    return

'''
开始进行计算的回调
'''
def start_calculate():
    global root_state
    global resolve
    global st
    if (np.array(root_state) == 0).all():
        z.set('未设置初始状态')
        return
    z.set('正在计算中...')
    root.update()
    resolve, state, st = solver(np.array(root_state))
    if state == -1:
        clr_root()
        z.set('问题无解,请重新输入初始状态....error state:-1')
        return
    elif state == 0:
        steps = len(resolve)
        z.set('移动到目标状态，总共走了' + str(steps - 1) + '步,搜索' + str(st) + '次')
        return
    elif state == 1:
        clr_root()
        z.set('问题无解,请重新输入初始状态....error state:1')
        return
    else:
        z.set('计算超过'+str(it_limit) + '次,已终止计算')
    return


'''
推演走动过程的回调
'''
def start_deduction():
    if len(resolve) == 0:
        z.set('还未求出路径，请先计算路径')
        return
    for i in range(len(resolve)):
        cur_state = resolve[i].pattern
        for j in range(len(cur_state)):
            if cur_state[j] == 0:
                mlist[j].set('')
                malist[j].config(bg=color[0])
            else:
                mlist[j].set(str(cur_state[j]))
                malist[j].config(bg=color[cur_state[j]])
        root.update()
        time.sleep(1)
    return

'''
界面设置
'''
root =Tk()
root.geometry("800x600")

#标签
titile = Label(root,text='八数码问题')
titile.config(font='Helvetica -30 bold', fg='blue')
titile.place(x=400, y=40, anchor="center")

zhuangtai = Label(root,text='输出')
zhuangtai.place(x=350, y=150, anchor="center")

s_input = Label(root, text='初始状态设置')
s_input.config(font='Helvetica -15 bold', fg='blue')
s_input.place(x=40, y=70)
input_guide = Label(root, text='例(123405678)')
input_guide.place(x=40, y=90)
c_input = Label(root, text='启发函数类型')
c_input.config(font='Helvetica -15 bold', fg='blue')
c_input.place(x=40, y=280)
it_input = Label(root, text='最大搜索次数')
it_input.config(font='Helvetica -15 bold', fg='blue')
it_input.place(x=40, y=200)


def settype1():
    global control
    control = 'type 1'
    q.set('type 1')
    return


def settype2():
    global control
    control = 'type 2'
    q.set('type 2')
    return


def settype3():
    global control
    control = 'type 3'
    q.set('type 3')
    return


def settype4():
    global control
    control = 'type 4'
    q.set('type 4')
    return


def settype5():
    global control
    control = 'type 5'
    q.set('type 5')
    return

def itset():
    global it_limit
    it_limit = int(it.get())
    return
#按钮
B_set = Button(root, text="设置", height=1, width=6,command=set_root)
B_set.place(x=40, y=160)
B_reset = Button(root, text="重置",height=1, width=6, command=clr_root)
B_reset.place(x=100,y=160)
B_reset = Button(root, text="随机设置",height=1, width=6, command=random_set)
B_reset.place(x=160,y=160)
B_itset = Button(root, text="设置", height=1, width=6,command=itset)
B_itset.place(x=40, y=245)
B_t1 = Button(root, text="错位数码的个数", command=settype1)
B_t1.place(x=40, y=320)
B_t2 = Button(root, text="移动到正确位置的距离", command=settype2)
B_t2.place(x=40, y=360)
B_t3 = Button(root, text="逆转棋子的个数乘2", command=settype3)
B_t3.place(x=40, y=400)
B_t4 = Button(root, text="错位个数加逆转乘三", command=settype4)
B_t4.place(x=40, y=440)
B_t5 = Button(root, text="错位个数加移动距离", command=settype5)
B_t5.place(x=40, y=480)
B_startc = Button(root, text="开始计算", height=3, width=12, command=start_calculate)
B_startc.place(x=320, y=500)
B_startd = Button(root, text="开始推演", height=3, width=12, command=start_deduction)
B_startd.place(x=600, y=500)


q = tkinter.Variable()
s = tkinter.Variable()
z = tkinter.Variable()
it = tkinter.Variable()

m0 = tkinter.Variable()
m0.set('1')
m1 = tkinter.Variable()
m1.set('2')
m2 = tkinter.Variable()
m2.set('3')
m3 = tkinter.Variable()
m3.set('8')
m4 = tkinter.Variable()
m4.set('')
m5 = tkinter.Variable()
m5.set('4')
m6 = tkinter.Variable()
m6.set('7')
m7 = tkinter.Variable()
m7.set('6')
m8 = tkinter.Variable()
m8.set('5')

mlist = [m0, m1, m2, m3, m4, m5, m6, m7, m8]

source = tk.Entry(root, textvariable=s)
source.place(x=40, y=120)
s.set('请输入初始状态')

state_show = tk.Entry(root,textvariable=z, width=40)
state_show.place(x=380, y=140)

itmax = tk.Entry(root, textvariable=it)
itmax.place(x=40, y=220)
it.set('1000')

qifa = tk.Entry(root, textvariable=q, width=10)
qifa.place(x=160, y=280)
q.set('type 1')

ma0 = tk.Button(root, textvariable=m0, bg=color[1], width=6, height=2)
ma0.place(x=430, y=250)
ma1 = tk.Button(root, textvariable=m1, bg=color[2], width=6, height=2)
ma1.place(x=490, y=250)
ma2 = tk.Button(root, textvariable=m2, bg=color[3], width=6, height=2)
ma2.place(x=550, y=250)
ma3 = tk.Button(root, textvariable=m3, bg=color[8], width=6, height=2)
ma3.place(x=430, y=310)
ma4 = tk.Button(root, textvariable=m4, bg=color[0], width=6, height=2)
ma4.place(x=490, y=310)
ma5 = tk.Button(root, textvariable=m5, bg=color[4], width=6, height=2)
ma5.place(x=550, y=310)
ma6 = tk.Button(root, textvariable=m6, bg=color[7], width=6,height=2)
ma6.place(x=430, y=370)
ma7 = tk.Button(root, textvariable=m7, bg=color[6], width=6,height=2)
ma7.place(x=490, y=370)
ma8 = tk.Button(root, textvariable=m8, bg=color[5], width=6, height=2)
ma8.place(x=550, y=370)

malist = [ma0, ma1, ma2, ma3, ma4, ma5, ma6, ma7, ma8]
root.mainloop()




