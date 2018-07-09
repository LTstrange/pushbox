#!/user/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LTstrange'

import copy
import time
import multiprocessing as mp

step = 0
T_field = []

def in_field():#finished
    code =1
    T_line=[]
    while True:
        line_str = input('line%d:'%(code))
        if line_str == 'end':
            return T_line
        line = [int(x) for x in line_str]
        T_line.append(line)
        code += 1

def in_target():#finished
    code = 1
    T_target=[]
    while True:
        tar_str = input('tar%d:'%(code))
        if tar_str == 'end':
            return T_target
        tar=[]
        a = 0
        for x in tar_str:
            try:
                a = a*10 + int(x)
            except:
                tar.append(a)
                a=0
            continue
        tar.append(a)
        T_target.append(tar)
        code += 1

def find_coners(field,targets):#finished
    corners = []
    ind_y = -1
    for y in field:
        ind_y += 1
        ind_x = -1
        for x in y:
            ind_x += 1
            if x !=0:
                try:
                    if field[ind_y-1][ind_x] == 0 and field[ind_y][ind_x-1] == 0:
                        coners.append([ind_y,ind_x])
                    if field[ind_y-1][ind_x] == 0 and field[ind_y][ind_x+1] == 0:
                        coners.append([ind_y,ind_x])
                    if field[ind_y+1][ind_x] == 0 and field[ind_y][ind_x-1] == 0:
                        coners.append([ind_y,ind_x])
                    if field[ind_y+1][ind_x] == 0 and field[ind_y][ind_x+1] == 0:
                        corners.append([ind_y,ind_x])
                except:
                    continue
    for each in corners:
        if each in targets:
            corners.extend(each)
    return corners

def move(nfield,way,point):#finished
    field = copy.deepcopy(nfield)
    for each in way:
        if each == 0:
            if field[point[0]-1][point[1]] ==1:
                field[point[0]-1][point[1]] = 3
                field[point[0]][point[1]] =1
            elif field[point[0]-1][point[1]] ==2:
                if field[point[0]-2][point[1]] ==1:
                    field[point[0]-2][point[1]] =2
                    field[point[0]-1][point[1]] =3
                    field[point[0]][point[1]] =1
                else:
                    return False,0
            else:
                return False,0
        elif each == 1:
            if field[point[0]][point[1]+1] ==1:
                field[point[0]][point[1]+1] = 3
                field[point[0]][point[1]] = 1
            elif field[point[0]][point[1]+1] ==2:
                if field[point[0]][point[1]+2] ==1:
                    field[point[0]][point[1]+2] =2
                    field[point[0]][point[1]+1] =3
                    field[point[0]][point[1]] =1
                else:
                    return False,0
            else:
                return False,0
        elif each == 2:
            if field[point[0]+1][point[1]] ==1:
                field[point[0]+1][point[1]] = 3
                field[point[0]][point[1]] = 1
            elif field[point[0]+1][point[1]] ==2:
                if field[point[0]+2][point[1]] ==1:
                    field[point[0]+2][point[1]] =2
                    field[point[0]+1][point[1]] =3
                    field[point[0]][point[1]] =1
                else:
                    return False,0
            else:
                return False,0
        elif each == 3:
            if field[point[0]][point[1]-1] ==1:
                field[point[0]][point[1]-1] = 3
                field[point[0]][point[1]] = 1
            elif field[point[0]][point[1]-1] ==2:
                if field[point[0]][point[1]-2] ==1:
                    field[point[0]][point[1]-2] =2
                    field[point[0]][point[1]-1] =3
                    field[point[0]][point[1]] =1
                else:
                    return False,0
            else:
                return False,0
        point = Fpoint(field)
    return True,field

def Fpoint(field):#finished
    point =[]
    for Ly in field:
        for each in Ly:
            if each == 3:
                x = Ly.index(3)
                y = field.index(Ly)
                point.append(y)
                point.append(x)
    return point

def check_goal(field,target):#finished
    for each in target:
        if field[each[0]][each[1]] == 2:
            continue
        else:
            return False
    return True

def answer(get):#finished
    t_answer = []
    for each in get:
        if each == 0:
            t_answer.append('U')
        elif each == 1:
            t_answer.append('R')
        elif each == 2:
            t_answer.append('D')
        elif each == 3:
            t_answer.append('L')
    print("解决方案：",t_answer)

def deleteFalseway(field,corners):#finished
    ind_y=-1
    for y in field:
        ind_y += 1
        ind_x = -1
        for x in y:
            ind_x += 1
            if x == 2:
                if field[ind_y + 1][ind_x]==2 and field[ind_y][ind_x + 1]==2 and field[ind_y + 1][ind_x + 1]==2:
                    return False
    for corner in corners:
        if corner == 2:
            return False
    return True

def cut_branch(field,T_field,corners):#finished
    if T_field.count(field)==0 and deleteFalseway(field,corners):
        return True
    else:
        return False

def processjob(q,ntree,field,point,corners,target,T_field,name):#待调校
    print("第%d进程执行中" %(name))
    for way in ntree:
        for i in range(4):
            nway=copy.deepcopy(way)
            nway.append(i)
            result = move(field,nway,point)
            if result[0]:
                if cut_branch(result[1],T_field,corners):
                    if check_goal(result[1],target):
                        answer(nway)
                    q.put([result[1],nway])
                    print(nway)
                else:
                    continue
            else:
                continue

def C_tree(field,point,tree,target,corners):#待调校
    global T_field
    global step
    step += 1
    #if step >3:
    #    return [0]
    print("searching step%d..." %(step))
    num = len(tree)
    print('此时tree内元素数量',num)
    ft_time = time.time()
    if num < 121:
        print("树形庞大，使用多核处理模式")
        print("正在分配任务给多核处理器。。")
        n = ((num - (num%12)) /12) +1
        q = mp.Queue()
        processes = []
        for k in range(12):
            try:
                ntree = copy.deepcopy(tree[int(k*n):int((k+1)*n)])
            except:
                ntree = copy.deepcopy(tree[int(k*n):])
            p = mp.Process(target=processjob,args=(q,ntree,field,point,corners,target,T_field,k))
            p.start()
            print(p)
            processes.append(p)
        print("分配完毕，正在计算中。。")
        for process in processes:
            process.join()
            print(process)
        print("计算完毕，正在提取数据。。")
        L1 = []
        while True:
            try:
                L1.append(q.get(False))
            except:
                break
        new_tree = []
        for i,s in L1:
            T_field.append(i)
            new_tree.append(s)
        print(new_tree)
    else:
        print("单核处理中。。")
        nfield = copy.deepcopy(field)
        new_tree=[]
        for way in tree:
            for i in range(4):
                nway = copy.deepcopy(way)
                nway.append(i)
                result = move(nfield,nway,point)
                if result[0]:
                    if cut_branch(result[1],T_field,corners):
                        if check_goal(result[1],target):
                            return nway
                        T_field.append(copy.deepcopy(result[1]))
                        new_tree.append(copy.deepcopy(nway))
                    else:
                        continue
                else:
                    continue
    end_time = time.time()
    print("this step use %f s" %(end_time - ft_time))
    return C_tree(field,point,new_tree,target,corners)

def main():
    global T_field
    #field = in_field()
    field=[[0,0,0,0,0,0,0,0],
           [0,0,1,1,0,0,0,0],
           [0,0,1,1,1,1,0,0],
           [0,0,0,1,0,1,0,0],
           [0,1,0,2,0,1,3,0],
           [0,1,2,1,1,0,1,0],
           [0,1,1,1,1,2,1,0],
           [0,0,0,0,0,0,0,0]]
#    target = in_target()
    target=[[4,1],[5,1],[6,1]]
    corners = find_coners(field,target)
    T_field.append(copy.deepcopy(field))
    num = 0
    for Ly in field:
        num += Ly.count(2)
    if len(target) == num:
        point = Fpoint(field)
        tree=[[]]
        starttime = time.time()
        get = C_tree(field,point,tree,target,corners)
        FINALtime = time.time()
        alltime = FINALtime - starttime
        print("耗时：",alltime)
        answer(get)
    else:
        print("啦啦啦,箱子和目标的数目不一致哦")
    

if __name__ == '__main__':
    main()