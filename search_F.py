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

def deleteFalseway(field,corners):
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

def cut_branch(field,T_field,corners):
    if T_field.count(field)==0 and deleteFalseway(field,corners):
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

def C_tree(field,point,tree,target,corners):
    global T_field
    global step
#    if step > 12:
#        print('超出设定')
#        FINALtime = time.time()
#        alltime = FINALtime - starttime
#        print("耗时：",alltime)

#        return [0]
    nfield = copy.deepcopy(field)
    new_tree=[]
    step +=1
    print("searching step%d..." %(step))
    print('此时tree内元素数量',len(tree))
    ft_time = time.time()
    if len(tree) !=0:
        for way in tree:
            for i in range(4):
                nway=copy.deepcopy(way)
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

    else:
        for i in range(4):
            way =[]
            way.append(i)
            result = move(nfield,way,point)
            if result[0]:
                if cut_branch(result[1],T_field,corners):
                    if check_goal(result[1],target):
                        return way
                    T_field.append(copy.deepcopy(result[1]))
                    new_tree.append(copy.deepcopy(way))
                else:
                    continue
            else:
                continue
    end_time = time.time()
    print("this step use %f s" %(end_time - ft_time))
    return C_tree(field,point,new_tree,target,corners)

def in_corners():
    code = 1
    T_corners=[]
    while True:
        cor_str = input('cor%d:'%(code))
        if cor_str == 'end':
            return T_corners
        cor = [int(x) for x in cor_str]
        T_corners.append(cor)
        code += 1

def find_corners(field,target):
    corners =[]
    ind_y=-1
    for y in field:
        ind_y += 1
        ind_x = -1
        for x in y:
            ind_x += 1
            if x == 0:
                try:
                    if field[ind_y + 1][ind_x]==0 and field[ind_y][ind_x + 1]==0:
                        corners.append((ind_y + 1,ind_x + 1))
                    if field[ind_y + 1][ind_x]==0 and field[ind_y][ind_x - 1]==0:
                        corners.append((ind_y + 1,ind_x - 1))
                    if field[ind_y - 1][ind_x]==0 and field[ind_y][ind_x + 1]==0:
                        corners.append((ind_y - 1,ind_x + 1))
                    if field[ind_y - 1][ind_x]==0 and field[ind_y][ind_x - 1]==0:
                        corners.append((ind_y - 1,ind_x - 1))
                except:
                    continue
    for each in corners:
        for any in each:
            if any <0:
                try:
                    
                    corners.remove(each)
                except:
                    continue
    return corners


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
#    field= in_field()
#    field=[[0,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,1,1,0,0],[0,0,0,1,0,1,0,0],[0,1,0,2,0,1,3,0],[0,1,2,1,1,0,1,0],[0,1,1,1,1,2,1,0],[0,0,0,0,0,0,0,0]]
    field = [[0,0,0,0,0,0,0,0,0],[0,3,1,1,1,1,1,1,0],[0,1,2,2,1,2,2,1,0],[0,2,1,1,1,1,2,1,0],[0,1,2,2,1,2,2,1,0],[0,1,2,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0]]#难度很高
#    target=in_target()
#    target=[[4,1],[5,1],[6,1]]
    target =[[1,3],[2,4],[4,4],[5,3],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7]]
#    target=[[4,8],[4,9],[4,10],[4,11],[5,8],[5,9],[5,10],[5,11],[6,8],[6,9],[6,10],[6,11],[7,8],[7,9],[7,10],[7,11]]
    T_field.append(copy.deepcopy(field))
    num=0
    for Ly in field:
        num += Ly.count(2)
    if len(target) == num:
        point = Fpoint(field)
#        corners = find_corners(field,target)
#        corners = in_corners()
        corners = [[1,1],[1,7],[5,1],[5,7]]
#        corners=[[1,1],[1,3],[1,5],[1,6],[1,13],[3,16],[4,1],[4,3],[4,5],[4,6],[4,18],[5,13],[5,18],[6,1],[6,6],[7,13],[7,18],[8,1],[8,7],[8,12],[9,5],[9,18],[10,7],[10,10],[10,12],[10,17]]
#        print(corners)
        tree=[]
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
