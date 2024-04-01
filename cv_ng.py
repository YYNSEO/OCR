import cv2
import numpy as np

image_path = 'dog.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
r, thresh = cv2.threshold(gray, 166,255, cv2.THRESH_BINARY)
cv2.imshow('threshold', thresh)
#cv2.waitKey()
#대부분 영상 처리의 첫 단계는 그레이 스케일적용.

kernel = np.ones((3,3), np.uint8)
#np.ones 배열을 통한 커널 생성
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
cv2.imshow('morphologh', opening)
#cv2.waitKey() #cv2.waitKey로 imshow결과 확인

#14번 라인의 모폴로지연산은 침식(erosion) 후에 팽창(dilation)을 적용하여
#경계 검출하려는 객체의 형상을 정확하게 얻어내는 기능
#작은 객체를 제거하고 배경을 스무딩하는 효과
#iteration : 반복 횟수

sure_bg = cv2.dilate(opening, kernel, iterations=2)
#cv2.dilation 으로 단독 팽창 작업 2회 반복 수행
cv2.imshow('after dilation iter2', sure_bg)
#cv2.waitKey()

res = cv2.bitwise_and(image, image, mask=sure_bg)
#첫번째 매개변수 : 입력이미지 1
#두번째 매개변수 : 입력이미지 2
#mask : 비트와이즈 연산 수행하려는 마스크 이미지
#bitwise연산은 이미지 처리에서 두 이미지 src1, src2 간 픽셀 연산
#연산이 비트 단위로 작동되기에 비트와이즈 연산
#이미지 특정 영역을 선택할 때 사용하는 연산
#bitwise_and : 비트와이즈의 and연산 and연산이란 논리 A and B 처럼
#두 입력 이미지가 모두 255 (흰) 영역에서만 흰색 출력하고 나머지는 검정 출력
#bitwise_or : 두 대응 이미지 픽셀간 OR 연산 , 두 이미지 중 하나라도 흰 영역이
#있으면 흰색 출력, 모두 검정이면 검정 출력
#bitwise not : 이미지 픽셀값 반전
cv2.imshow('res', res)
#cv2.waitKey()
b,g,r = cv2.split(res)
alpha = np.ones(b.shape, dtype=b.dtype) * 255
alpha[sure_bg>0] = 255
#알파채널 255는 불투명 , 0은 투명
result=cv2.merge((b,g,r,alpha))
cv2.imwrite('result.png', result)
cv2.imshow('original image',image)
cv2.waitKey()