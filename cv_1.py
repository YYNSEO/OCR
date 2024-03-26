import cv2
# capture = cv2.VideoCapture('v.mp4')
# while cv2.waitKey(30) < 0:
#     if capture.get(cv2.CAP_PROP_POS_FRAMES)==capture.get(cv2.CAP_PROP_FRAME_COUNT):
#         capture.set(cv2.CAP_PROP_POS_FRAMES,0)
#         #조건문 : 전체 프레임 카운트와 현재 프레임 카운트가 같다면 : 영상끝이다. :
#         #capture.set(cv2.CAP_PROP_POS_FRAMES를 0으로 설정)
#     ret,frame=capture.read()
#     cv2.imshow("frame", frame)
# capture.release()
# cv2.destroyAllWindows()
# src = cv2.imread("image1.png", cv2.IMREAD_ANYCOLOR)
# height, width, channel =src.shape
# matrix = cv2.getRotationMatrix2D((width/2,height/2),45,2)
# dst = cv2.warpAffine(src,matrix,(width,height)) # 회전된 이미지를 출력
# cv2.imshow('src',src) #원본 이미지
# cv2.imshow('dst', dst) #회전된 이미지
# cv2.waitKey()
# cv2.destroyAllWindows()
# getRotationmatrix2D함수는 이미지 회전 확대 기능
# 중심점 w/2 , h/2
# warpAffine함수에 매개변수로 회전 마스크 matrix를 넣어줌
# 아핀변환(warpAffine)변환 함수 :
# 원본이미지 (src)에 matrix를 적용하고
# 출력이미지 사이즈를 dsize로 width, height 원본사이즈 동일하게 변형하는 작업
# 아핀 맵 행렬에 따라 회전된 이미지를 반환한다.


# #영상/이미지 처리에서 확대 축소를 업샘플링 or 다운샘플링으로 표현
# # 업샘플링 -> 원본 이미지 크기 확대
# # 다운샘플링 -> 원본 이미지 크기 축소
#
# src = cv2.imread('image1.png', cv2.IMREAD_COLOR)
# height,width,channel = src.shape
# dst = cv2.pyrUp(src,dstsize=(width*2,height*2),borderType=cv2.BORDER_DEFAULT)
# #pyrUp : 업샘플링 함수 : 이미지 확대, 확대에는 dstsize로 확대 배율 설정(튜플형태)
# #borderType 매개변수 :
# #cv2.BORDER_DEFAULT : 기본값
# #cv2.BORDER_CONSTANT : 픽셀 채우기
# #cv2.BORDER_REFLECT : 경계 기준 이미지 반사 채우기
# #CV2.BORDER_REFLECT_101 : 경계 기준 이미지 반사 채우기, 경계 픽셀 제외
# #이미지 연산 중 이미지 경계 처리 방법 지정하는 속성
# reflected_src = cv2.copyMakeBorder(src, 100, 100, 100, 100, cv2.BORDER_REFLECT)
# #copyMakeBorder 함수 : 테두리 두께 설정 및 테두리 속성 설정
# dst2 = cv2.pyrDown(src)
# #pyrDown : 다운 샘플링 함수 : 이미지 축소이고 고정적으로 절반으로 축소함
#
# cv2.imshow('ref',reflected_src)
# cv2.imshow("src",src)
# cv2.imshow("up",dst)
# cv2.imshow("down",dst2)
# cv2.waitKey()
# cv2.destroyAllWindows()
#
#
# #ROI 관심 구역 : Region Of Interest
# #R-CNN의 특징
# #기존 CNN 신경망에 비해 속도가 매우 빠름.
# #특정 구역을 지정해서 해당 구역에 대해서 신경망 처리
# #seg
# #영상 처리시 객체 탐지detect, 추적tracking, 검출하는 영역을 관심 영역이라 함
# #특정 ROI만 추철하여 해당 부분에만 영상처리를 적용해 빠르게 구동
# #불필요한 부분 연산이 줄어 정확도, 속도 향상

# src = cv2.imread("image1.png", cv2.IMREAD_COLOR)
# roi1 = src[100:400,200:500].copy()
# #복사
# cv2.imshow("src", src)
# cv2.imshow("dst", roi1)
# cv2.waitKey()


#복사의 종류
lista = []
listb = [1,2,3,4]
listc = [1]

listc.append(listb)
print(listc)

listc = listc+listb
print(listc)
listc = [1,2,3]
print(listc)

def changeList(list_x):
    temp = list_x
    list_x.append(10)
    print("temp",temp)
    print("list_x",list_x)
changeList(listc)


#깊은 복사 vs 얕은 복사
#파이썬 객체는 immutable 객체와 mutable 객체로 나뉜다.
#immutable 객체는 값을 바꿀 수 없는 객체
#mutable 객체는 값을 바꿀 수 있는 객체

#immutable 객체는 값이 바뀌면 다른 메모리 공간을 할당하여 주소값도 바뀜
#mutable 객체는 주소값이 동일해도 그 안의 값 바꿀 수 있음

#immutable : tuple, str, int, float , boolean
#mutable : list, dict


#ex) teml_List_x
#ex) def changeList(list_x)
#이 때 실제 값이 복사되는 것이 아니라
#참조 주소값만 복사된다.
#따라서 temp = list_x를 해놔도
#후에 list_x의 구성을 변경하면, temp구성도 같이 바뀌게 됨

#위 동일한 작업을 immutable 객체를 대상으로 수행하면
#ex) temp=src
#후에 src의 값 할당이 바뀌면 재할당이 이루어지며 메모리 주소가 변경된다.
#따라서 temp와 src는 다른 값을 가지게 됨.
#
# a = [1,2,3]
# b = a[:]
# print(id(a))
# print(id(b))
# print(a==b)
# print( a is b )
# # list 슬라이싱을 통한 새로운 값 할당
# # 슬라이싱을 통한 할당을 하면 새로운 id가 부여된다.
# # 서로 영향 없음.
# # 슬라이싱은 얕은 복사 (shallow copy)라고 함.
# a = [[1,2],[3,4]]
# b = a[:]
# print(id(a))
# print(id(b))
# print(id(a[0]))
# print(id(b[0]))
# a[0] = [5,6]
# print(a)
# print(b)
# print(id(a[0]))
# print(id(b[0]))
# a[1].append(5)
# print(a)
# print(b)
#
# import copy
# a = [[1,2],[3,4]]
# b = copy.copy(a)
# a[1].append(5)
# print(a)
# print(b)
#
#
# ##################################
# a = [[1,2],[3,4]]
# b=copy.deepcopy(a)
# a[1].append(5)
# print(a)
# print(b)

#결론 : 대입 = 형태로 복사함녀 원본도 영향 받는다.
#싫으면 deepcopy를 쓴다.



#영상 binary : 이진화 작업
#이진화란 : 어느 밸류를 기준으로 값이 높거나 or 낮은 픽셀의 값을 특정 기준 값으로 변환
#일반적으로 검정 혹은 흰색의 값으로 변경함.
#기준 밸류에 따라 이분법적으로 구분하여, 픽셀을 T or F로 나누는 연산이고, 이미지 행렬(matrix)
#의 모든 픽셀에 대해 연산을 수행한다.

#cv2.cvtColor(대상이미지객체, cv2.COLOR_BRG2GRAY) #그레이 컬러 사진이 됨
#cv2.threshold(그레이스케일이미지객체, threshV, maxV, cv2.THRESH_BINARY)

# src=cv2.imread('tesla.jpg',cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(src,cv2.COLOR_BGRA2GRAY)
# ret,dst = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
# cv2.imshow('dst',dst)
# cv2.imshow('src',src)
# cv2.waitKey()
# cv2.destroyAllWindows()
#170수치를 기준으로 초과 : 255처리
#이하는 0처리하여 이진화를 했다.
#threshold : 임계값


#cv2.THRESH_BINARY : 임계값 초과시 maxValue 아닐 경우 0
#CV2.THRESH_BINARY_INY : 임계값 초과시 0 아닐 경우 maxval
#cv2.THRESH_TRUNC : 임계값 초과시 thresh 값으로 아닐 경우 변형 없음
#cv2.THRESH_TOZERO : 임계값 초과시 변형 X, 미만은 0처리

#RGB -> GRAYSCALE 공식
#3채널 -> 1채널 변환
#G =(0.299*R) + (0.587*G) + (0.114*B)
#0.299 + 0.587 + 0.114 = 1
# 1채널 gray값도 0 ~ 255



#blur 흐리게 처리
#흐림 효과 , 블러링, 스무딩
#블러는 영상의 샤프니스를 줄여 노이즈를 줄이는 작업
#원하는 객체 외 외부 영향 최소화 목적
#블러는 영상이나 이미지를 번지게 처리함.
#해당 픽셀과 주변 값들을 비교해서 계산한다.
#노이즈 제거가 주 목적이고, 후 작업에 연산 속도 향상

# src = cv2.imread('apple.jpg', cv2.IMREAD_COLOR)
# dst = cv2.blur(src,(3,3), anchor=(-1,-1), borderType = cv2.BORDER_DEFAULT)
# #blur함수로 블러처리가 가능하고
# #ksize는 커널의 크기를 의미한다. 주변의 픽셀 고려하는 범위
# #anchor = (-1, -1) 커널의 중심 , -1,-1로 두면 자동설정
# #커널 홀수 단위
# cv2.imshow('dst', dst)
# cv2.imshow('src',src)
# cv2.waitKey()
# cv2.destroyAllWindows()

src=cv2.imread('dog.jpg',cv2.IMREAD_COLOR)
dst = cv2.blur(src,(5,5), anchor=(-1,-1), borderType = cv2.BORDER_DEFAULT)
gray = cv2.cvtColor(dst,cv2.COLOR_BGRA2GRAY)
ret,dst2 = cv2.threshold(gray,167,255,cv2.THRESH_BINARY)
cv2.imshow('dst',dst2)
cv2.imshow('src',src)
cv2.waitKey()
cv2.destroyAllWindows()

#커널은 이미지에서 특정 픽셀 spot(x,y)의 주변 일정 범위 박스 공간
#신호처리 분야에서 커널은 필터라고 부름

#anchor 포인트 (고정점)
#고정점은 커널을 통해 컨벌루션된 값을 할당한 지점
#컨벌루션 : 새로운 픽셀을 만들어 낼 때 커널 크기의 화소 값을 이용해서 어떤 시스템(함수)를 통과시켜
#계산하는 행위를 의미
#커널 내 고정점은 하나의 포인트이다.
