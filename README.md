# Project2-2_Garbled_circuit
## code、txt連結
https://drive.google.com/open?id=12KNqMt8HA6rP0rpxQUtpiHF2hAFOhq2T

## 想法
用電路計算 g ^ x mod p

方法:

```
f = g
for i in range x-1:
  f = f * g
  while (len(f) > len(p)):
    f = f[:len(f) - len(p)] * (p 2's complement) + f[:len(f) - len(p):]
if f > p:
  f = f + (p 2's complement)
```

乘法用乘法器完成，加法用加法器完成。

我的寫法是當使用者輸入g、x、p之後，把g、p轉換成二進制，開始依照上面code的概念把它用and、or、xor gate完成計算並產出電路。

連結中的`文件.txt`有每一個code的解釋。

但是這跟老師要求的不一樣，老師要的是先有電路、再輸入input，得出答案。

但我的是先輸入input，經過計算之後得出電路，再吃一次input亂數，得出答案，也就是說，我這個寫法產出的電路，基本上只有這一組input可以跑，其他會出錯。

## 工作分配
###  1051524莊子毅 25%
###  1051433葛東昇 20%
###  1051518李政憲 35%
###  1051434蔡適謙 20%
