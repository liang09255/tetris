# Tetris 俄罗斯方块
# 简介

本项目基于[daishengdong/Games](https://github.com/daishengdong/Games)项目中的俄罗斯方块构建，优化了性能及内存使用情况，并新增部分功能，相关技术栈`pytohn3` `pygame`

# QuickStart

1. 将项目克隆到本地

   ```shell
   git clone https://github.com/liang09255/tetris.git
   ```

2. 安装依赖

   ```shell
   pip install - r requirements.txt
   ```

3. 运行

   ```shell
   python main.py
   ```

# 新功能列表

- [x] 优化UI
- [x] 优化CPU及内存使用
- [x] 最高历史得分记录
- [x] 速度变化
- [x] 游戏用时
- [x] 下落位点预测
- [x] 干扰块机制
- [ ] 创意双人

# 功能介绍

## 速度变化

速度根据得分情况变化，方块下落的间隔计算公式为：

`间隔=最小间隔+(最大间隔-最小间隔)/(1+当前得分/10)`  

可保证速度在合理范围内逐渐加快

## 下落位点预测

可在下方显示当前方块落点，按字母P键开启或关闭此功能

## 干扰块机制

随机掉落一块干扰方块在已有的方块上，按字母O键切换干扰等级

等级设定：

1. 等级0 不掉落干扰块

2. 等级1 每8个方块掉落一个干扰块

3. 等级2 每5个方块掉落一个干扰块

4. 等级3 每3个方块掉落一个干扰块

干扰块计算原理：

由Pierre Dellacherie算法改造而来，计算得到最小分数的位置为目标下落点，在保证高度较小(避免干扰块过度干扰导致游戏结束)的情况下避免消行达到干扰目的

## 创意双人
