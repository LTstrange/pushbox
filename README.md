## pushbox
# 输入推箱子地图，返回操作步骤


search_F.py 是单线程的搜索代码，输入的时候，需要是矩阵形式，或者在函数里建立地图对应的矩阵列表。代码的可读性和鲁棒性还需改进，敬请期待。。

代码讲解：在代码中，field是地图变量，图中的0代表墙壁（不可移动的物块）， 3代表玩家所在位置，2代表箱子所在位置，1代表没有东西（空位）
而target则是箱子（2）最终应该在的位置，所有箱子在其应该在的位置时，游戏胜利。
Corner参数则是由于加速查找速度的，当箱子在Corner位置时，且此Corner不是target，那么直接可以判断游戏结束，因为箱子在角落里的时候，是无法推出来的。

find_corner函数是用来自动寻找Corner的，但是似乎不是很好使。所以需要in_corner函数来手动输入Corner。

程序依然有很多bug，比如，过大的地图必须手动在程序中输入，因为in_field函数无法输入两位数的行数或列数。
同理，in_target函数也是如此。

# 若要体验程序，将search_F.py下载运行即可，
其中有部分作者用来测试的地图，以及配套的target与Corner。

也可以将in_field 和in_target 函数的注释取消掉，就可以将自己的推箱子难题来进行自动求解了。

谢谢支持，希望大佬可以来fork改进程序，如有帮助，希望可以给star支持～
