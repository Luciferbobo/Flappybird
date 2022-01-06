# Flappybird
Play Flappybird with DQN (Reinforcement Learning for Flappybird)
Player can play Flappybird with AI together by DQN module.

## 1.Intro
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/Flappybird.gif" width="356" height="288"> 
  
(Left AI, Right Player)
  
</div>

·Epoch 1000     Score：1-2 

·Epoch 10k       Score：20+

·Epoch 100w    Score：200+ 



## 2.Algorithm

Q-Learning
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s1.png" width="840" height="395">  
</div>


Q-Learning iteration function
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s3.png" width="690" height="109">  
</div>

Using neural network to fit Q(s, a)
<div align=center>
<img src="https://github.com/Luciferbobo/Flappybird/blob/main/Fig/s2.png" width="493" height="270">  
</div>

## 3.How to play

Main requirements:
~~~shell
torch
cv2
pygame
~~~

Space→Jump

