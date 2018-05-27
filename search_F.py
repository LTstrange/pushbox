import copy
import time
"""
用穷举和剪枝的方法，找到推箱子的最佳走法，广度优先
对每一步的field都与先前的步骤的field比对，重复则剪枝
先前的field储存在T_field里面
0，1，2，3 分别为上右下左
"""
step =0
T_field=[]


def in_field():
    code =1
    T_line=[]
    while True:
        line_str = input('line%d:'%(code))
        if line_str == 'end':
            return T_line
        line = [int(x) for x in line_str]
        T_line.append(line)
        code += 1

def in_target():
    code = 1
    T_target=[]
    while True:
        tar_str = input('tar%d:'%(code))
        if tar_str == 'end':
            return T_target
        tar = [int(x) for x in tar_str]
        T_target.append(tar)
        code += 1

def cut_branch(field,T_field):
    if T_field.count(field)==0:
        return True
    else:
        return False

def Fpoint(field):
    point =[]
    for Ly in field:
        for each in Ly:
            if each == 3:
                x = Ly.index(3)
                y = field.index(Ly)
                point.append(y)
                point.append(x)
    return point

def move(nfield,way,point):
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

def check_goal(field,target):
    for each in target:
        if field[each[0]][each[1]] == 2:
            continue
        else:
            return False
    return True

def C_tree(field,point,tree,target):
    global T_field
    global step
#    if step > 3:
#        print('超出设定')
#        exit(0)
    nfield = copy.deepcopy(field)
    new_tree=[]
    step +=1
    print("searching step%d..." %(step))
    print('此时tree内元素数量',len(tree))
    if len(tree) !=0:
        for way in tree:
            for i in range(4):
                nway=copy.deepcopy(way)
                nway.append(i)
                result = move(nfield,nway,point)
                if result[0]:
                    if cut_branch(result[1],T_field):
                        if check_goal(result[1],target):
                            return nway
                        T_field.append(copy.deepcopy(result[1]))
                        new_tree.append(copy.deepcopy(nway))
                    else:
                        continue
                else:
                    continue

    else:
        for i in range(4):
            way =[]
            way.append(i)
            result = move(nfield,way,point)
            if result[0]:
                if cut_branch(result[1],T_field):
                    if check_goal(result[1],target):
                        return way
                    T_field.append(copy.deepcopy(result[1]))
                    new_tree.append(copy.deepcopy(way))
                else:
                    continue
            else:
                continue
    return C_tree(field,point,new_tree,target)

def answer(get):
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

def main():
    global T_field
    field= in_field()
#    field=[[0,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,1,1,0,0],[0,0,0,1,0,1,0,0],[0,1,0,2,0,1,3,0],[0,1,2,1,1,0,1,0],[0,1,1,1,1,2,1,0],[0,0,0,0,0,0,0,0]]
    target=in_target()
#    target=[[4,1],[5,1],[6,1]]
    T_field.append(copy.deepcopy(field))
    num=0
    for Ly in field:
        num += Ly.count(2)
    if len(target) == num:
        point = Fpoint(field)
        tree=[]
        starttime = time.time()
        get = C_tree(field,point,tree,target)
        FINALtime = time.time()
        alltime = FINALtime - starttime
        print("耗时：",alltime)
        answer(get)

    else:
        print("啦啦啦,箱子和目标的数目不一致哦")
if __name__ == '__main__':
    main()
