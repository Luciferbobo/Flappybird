# Flappybird
和DQN一起玩Flappybird(Flappybird的强化学习实现)
在pygame的Flappybird的游戏上实添加DQN模块，实现AI与玩家共同进行游戏。

## 1.效果展示
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/Flappybird.gif" width="356" height="288"> 
  
左AI,右玩家
  
</div>

·Epoch 1000     Score：1-2 

·Epoch 10k       Score：20+

·Epoch 100w    Score：200+ 



## 2.算法

Q-Learning工作过程
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s1.png" width="840" height="395">  
</div>


Q-Learning迭代函数
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s3.png" width="690" height="109">  
</div>

利用神经网络拟合Q(s, a)
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s2.png" width="493" height="270">  
</div>

## 3.操作说明

Main requirements:
~~~shell
torch
cv2
pygame
~~~

空格键进行跳跃

