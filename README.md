<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default">
# Flappybird
和DQN一起玩Flappybird(Flappybird的强化学习实现)

## 1.效果展示
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/Flappybird.gif" width="356" height="288"> 
  
左AI,右玩家
  
</div>

## 2.算法

Q-Learning迭代
$$Q(s, a) \leftarrow Q(s, a)+\alpha \cdot\left[r_{t+1}+\gamma \cdot \max _{a^{\prime}} Q\left(s^{\prime}, a^{\prime}\right)-Q(s, a)\right] $$

利用神经网络拟合$Q(s, a)$

## 3.操作说明

需要安装的库
空格键进行跳跃

</script>
