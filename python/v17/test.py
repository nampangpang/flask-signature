import numpy as np
import random


bts = ["V","RM", "Junkook", 'Suga', 'Jin']
bts.append("Jimin")

print(max(bts))
#print(bts)
ints = [10, 20, 30]
ints += [40, 50]
#print(ints)

list(range(5)) #0~4까지 생성
list(range(0, 5))#0~4까지 생성
list(range(0, 5, 1))#0~4까지 1칸씩 증가시킴
list(range(0, 5, 2))#0~4까지 2칸씩 증가시킴
list(range(2, 5))#2에서 5-1까지의 연속된 수 즉 2, 3, 4생성

intss = [1, 3, 5] * 3# 135135135

#print(1 in intss)#1이 intss안에 있는가 not in 쓰면 안에 없는가

#하나의 리스트에 여라가지 타입의 데이터를 섞어서 저장하는 것도 가능

# @@@@@@@@@리스트에서 사용 가능한 함수들
# len, max, min, sum, @@@평균을 구하고 싶으면 sum(list) / len(list)
# any = 리스트에 0이 아닌 원소가 하나라도 있는가


bts[:3] # v, rm, junkook 출력
bts[3:] # junkook, suga, jin 출력
bts[:]  # 싹다
bts[::2]#처음부터 읽어오느데 2씩 건너 뛰어서

bts[2] = "남광훈"

bts[2:3] = ["남광훈", "손흥민"]

#index( x ) 원소 x를 이용하여 위치를 찾는 기능을 한다.
#append( x ) 원소 x를 리스트의 끝에 추가한다.
#count( x ) 리스트 내에서 x 원소의 개수를 반환한다.
#extend([x1, x2]) [x1, x2] 리스트를 기존 리스트에 삽입한다.
#insert(index, x) 원하는 index 위치에 x를 추가한다.
#remove( x ) x 원소를 리스트에서 삭제한다.
#pop(index) index 위치의 원소를 삭제한 후 반환한다. 이때 index는 생략될 수 있으며
# 이 경우 리스트의 마지막 원소를 삭제하고 이를 반환한다.
#sort() 값을 오름차순 순서대로 정렬한다. 키워드 인자 reverse=True이면 내림차순으로
#정렬한다.
#reverse() 리스트를 원래 원소들의 역순으로 만들어 준다.
