import copy
import logging


# 输入方块下落后的游戏画板
# 0表示没有方块，1表示有方块，2表示当前方块
def cal_score(s: list) -> float:
    # 经验权重
    # return (
    #         - 4.500158825082766 * _cal_landingHeight(s)
    #         + 3.4181268101392694 * _cal_erodedPieceCellsMetric(s)
    #         - 3.2178882868487753 * _cal_boardRowTransitions(s)
    #         - 9.348695305445199 * _cal_boardColTransitions(s)
    #         - 7.899265427351652 * _cal_boardBuriedHoles(s)
    #         - 3.3855972247263626 * _cal_boardWells(s)
    # )
    return (100.500158825082766 * _cal_landingHeight(s)
            + 100.4181268101392694 * _cal_erodedPieceCellsMetric(s))


# 计算高度
def _cal_landingHeight(s: list) -> int:
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == 2:
                return len(s) - i
    # 正常不会执行到这
    logging.error("高度计算错误")
    return 0


# 计算消除贡献值
def _cal_erodedPieceCellsMetric(s: list) -> int:
    contribute = 0
    delete_line = 0
    for i in range(len(s)):
        if 0 not in s[i]:
            delete_line += 1
            for j in range(len(s[i])):
                if s[i][j] == 2:
                    contribute += 1
    return contribute * delete_line


# 计算行变换数
def _cal_boardRowTransitions(s: list) -> int:
    s2 = copy.deepcopy(s)
    # 添加左右两列
    _fill_left_right(s2)
    _to_one(s2)
    # 计算行变换数
    count = 0
    for i in range(len(s2)):
        for j in range(len(s2[i]) - 1):
            if s2[i][j] != s2[i][j + 1]:
                count += 1
    return count


# 计算列变换数
def _cal_boardColTransitions(s: list) -> int:
    s2 = copy.deepcopy(s)
    _fill_up_down(s2)
    _to_one(s2)
    # 计算列变换数
    count = 0
    for i in range(len(s2[0])):
        for j in range(len(s2) - 1):
            if s2[j][i] != s2[j + 1][i]:
                count += 1

    return count


# 计算空洞数
def _cal_boardBuriedHoles(s: list) -> int:
    _to_one(s)
    count = 0
    for i in range(len(s[0])):
        for j in range(len(s) - 1):
            if s[j][i] == 1 and s[j + 1][i] == 0:
                count += 1
    return count


# 计算井数
def _cal_boardWells(s: list) -> int:
    _to_one(s)
    count = 0
    _fill_left_right(s)

    # 按列遍历，遇到0判断两边是否为1，是则计算井数，同时计算井深，深度为1count为1，深度2count为3，深度3count为6，以此类推
    for i in range(1, len(s[0]) - 1):
        deep = 0
        for j in range(len(s)):
            if s[j][i] == 0 and s[j][i - 1] == 1 and s[j][i + 1] == 1:
                deep += 1
            else:
                count += deep * (deep + 1) / 2
                deep = 0
        count += deep * (deep + 1) / 2
    return int(count)


# 把非0数字变为1
def _to_one(s: list):
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] != 0:
                s[i][j] = 1


# 填充左右两列
def _fill_left_right(s: list):
    for i in range(len(s)):
        if s[i].count(0) == len(s[i]):
            s[i].insert(0, 0)
            s[i].append(0)
        else:
            s[i].insert(0, 1)
            s[i].append(1)


# 填充上下两行
def _fill_up_down(s: list):
    new_s = [row for row in s if any(row)]
    s.clear()
    s.extend(new_s)
    s.insert(0, [1 for _ in range(len(s[0]))])
    s.append([1 for _ in range(len(s[0]))])


if __name__ == "__main__":
    square = [
        [0, 0, 0, 0, 0],
        [0, 1, 2, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0],
    ]
    s1 = copy.deepcopy(square)
    print(cal_score(s1))
    s1 = copy.deepcopy(square)
    print(_cal_landingHeight(s1))
    s1 = copy.deepcopy(square)
    print(_cal_erodedPieceCellsMetric(s1))
    s1 = copy.deepcopy(square)
    print(_cal_boardRowTransitions(s1))
    s1 = copy.deepcopy(square)
    print(_cal_boardColTransitions(s1))
    s1 = copy.deepcopy(square)
    print(_cal_boardBuriedHoles(s1))
    s1 = copy.deepcopy(square)
    print(_cal_boardWells(s1))
