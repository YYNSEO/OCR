import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

#matlplotlib 패키지의 서브패키지인 pyplot : 시각화 도구 (그래프)
#pyplot 은 그래프, 차트, 히스토그램 등 시각화 관련 함수와 프로퍼티 제공
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract'
#테서렉트 커맨더 = 파일위치 설정

plt.style.use('dark_background')
#시각화 도구 어두운 배경 설정
img_ori = cv2.imread("77.jpg")
#cv2의 imread로 원본이미지 불러오기
height,width,channel = img_ori.shape
#이미지 높이 너비 채널 데이터 저장


plt.figure(figsize=(12,10))
#plt로 출력하는 이미지 결과물 사이즈 :  너비 12 인치 높이 12인치 설정
#figure 는 속성 설정

plt.imshow(img_ori,cmap='gray')
#img_ori 는 배열 데이터 (numpy구조)
#cmap 속성으로 gray를 지정하여 이미지를 흑백으로 출력 가능

# plt.show()
# npimg = np.array(cv2.imread('1.jpg'))
# np.set_printoptions(threshold=np.inf)#np 배열 출력옵션 무한대로 설정해서 모든 픽셀 출력가능
# print(npimg)









################step 2 원본 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(img_ori,cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(12,10))
plt.imshow(gray,cmap='gray')
#plt.show()

#그레이스케일의 효과
#노이즈 제거 효과
#명암 대비
#RGB 채널이 단일 채널로 변경되어 연산속도 향상
#조명 차이 평탄화, 조명 변화에 강하다


npgray = np.array(gray)
npori = np.array(img_ori)
# print(npori.shape)#(626, 940, 3) => 3차원 데이터
# print(npgray.shape)#(626, 940) => 2차원 데이터
# 채널이 사라져서 연산속도 향상
#원본이미지와 gray 이미지의 shape 비교

################step 3 임계처리

img_blurred = cv2.GaussianBlur(gray,ksize=(35,35),sigmaX=0)
#가우시안 블러로 이미지 노이즈 제거
#블러는 샤프니스가 줄어 경계선 검출 이전에 적용하는 경우가 많음

img_thresh = cv2.adaptiveThreshold(img_blurred,maxValue=255.0,
                                   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY_INV,
                                   blockSize=19,
                                   C=6)

#adaptive 스레시홀드 : 특정 값 기준 작은 값  0, 큰값 255.0 이진화
#블록사이즈와 C값은 사용자가 조절해서 노이즈 정도 조절
#C가 작아질수록 노이즈가 많아짐
#blocksize 는 주변 범위를 얼마 기준 잡아 노이즈 처리 할 것인지 정하는 값

plt.figure(figsize=(12,10))
plt.imshow(img_thresh,cmap='gray')
#plt.show()




################step 4 윤곽 찾기

contours,hierarchy = cv2.findContours(img_thresh,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_SIMPLE)
# print(type(contours))#class tuple 로 출력, findcontours는 실제 외곽선 데이터와 계층 구조를 같이 리턴해줌
# for i,contour in enumerate(contours):
#     print(f"contour{i+1} dimension: ",contour.shape,":",contour)


#리턴된 컨투어 타입은 튜플

#컨투어 찾을 때 thresh 적용 된 이미지를 넣는다.
#mode = cv2.RETR_LIST : 모든 윤곽을 검색하는 옵션
#cv2.RETR_EXTERNAL : 외부 윤곽만 검색


#method  approximate = 근사화
#cv2.CHAIN_APPROX_SIMPLE 로 설정한 경우 윤곽 근사화를 위해 수직/수평/대각 바향 점을 모두 제거하여 간단하게 처리
#직선 부분은 끝점만 남기고 중간 점들을 제거하여 근사화
#APPROX_SIMPLE 은 중간 점들 제거로 속도가 빠름.

#cv2.CHAIN_APPROX_NONE 모든 육곽 포인트 유지해서 윤곽을 얻음
#모든 윤곽을 얻지만 데이터의 양이 많아 느림






temp_result=np.zeros((height,width,channel),dtype=np.uint8)
#uint8 : 8비트 부호 없는 정수


cv2.drawContours(temp_result,contours=contours,contourIdx=-1,color=(255,255,255))
plt.figure(figsize=(12,10))
plt.imshow(temp_result,'gray')
#plt.show()


#cv2.drawContours 는 컨투어 외곽선 그리는 함수
#contours = contours 는 cv2.findContours 로 찾은 윤곽 정보 담긴 리스트
#contourIdx = -1 은 윤곽인덱스 모두 그리라는 의미
#color 255 255 255 로 흰색으로 그린다.



contour_dict=[]
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(temp_result,pt1=(x,y),pt2=(x+w,y+h),color=(255,255,255),thickness=3)
    contour_dict.append({
        'contour':contour,
        'x':x,
        'y':y,
        'w':w,
        'h':h,
        'cx':x+(w/2),
        'cy':y+(h/2),
    })

#cv2.boundingRect(contour) : 바운딩렉트 함수는 윤곽을 둘러싼 최소 사각형 범위의 좌표 반환
#cv2.rectangle 직사각형 그리는 함수
#pt1 : 상자 왼쪽 위 모퉁이 좌표
#pt2 : 오른쪽 아래 꼭지점 좌표
#contour_dict 는 메모리에 윤곽 정보 저장용
plt.figure(figsize=(12,10))
plt.imshow(temp_result,cmap='gray')
#plt.show()


################step 5 많은 박스 중 어떤게 번호판 박스일까
#이미지에 따라 사용자가 직접 조절가능한 수치를 넣어줘야 한다.

MIN_AREA = 300 #바운딩 박스의 면적
MIN_WIDTH = 2 #바운딩 박스 최소 너비
MIN_HEIGHT = 8 #바운딩 박스 최소 높이
MIN_RATIO = 0.25 #최소 세로 가로 비율
MAX_RATIO = 1.0 # 최대 세로 가로 비율


possible_contours=[]
cnt = 0
for d in contour_dict:
    area=d['w']*d['h']
    ratio = d['w']/d['h']
    if area > MIN_AREA and d['w']>MIN_WIDTH and d['h']>MIN_HEIGHT and MIN_RATIO<ratio<MAX_RATIO:
        d['idx']=cnt
        cnt+=1
        possible_contours.append(d)
#possibe_contours 리스트에 조건을 통과(단일 번호의 렉탱글 조건 부합)하는 딕셔너리만 추가






################step 6  번호판 박스로 보여지는 것들 중 어떤 것이 연속적일까

MAX_DIAG_MULTIPLYER =5  #다이아고날 랭스 : 컨투어 박스 대각 길이 5배수 설정 를 2로 낮추면 앞에 2개가사라진다.
MAX_ANGLE_DIFF = 3 # 첫 박스와 다음 박스의 배치의 각도 차이
MAX_AREA_DIFF = 0.5 # 첫박스와 두번째 박스의 면적 차이
MAX_WIDTH_DIFF = 0.8 # 첫박스와 두번째 박스의 너비 차이
MAX_HEIGHT_DIFF = 0.2 # 첫박스와 두번째 박스의 높이 차이
MIN_N_MATCHED = 4# 연속적으로 몇개가 검출 되어야 유효처리 할 것인가


def find_chars(contour_list):#find_chars함수는 재귀 호출 됨
    matched_result_idx=[]# 최종 선택 결과 인덱스 저장 리스트
    for d1 in contour_list: # A, B 비교를 위한 2중 for 문 구성
        matched_contours_idx=[]
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:#A와 B가 같으면 패스
                continue
            dx=abs(d1['cx']-d2['cx'])#절대값으로 두점 사이 거리 측정
            dy=abs(d1['cy']-d2['cy'])
            diagonal_length1 = np.sqrt(d1['w']**2+d1['h']**2) #w제곱 + h제곱 으로 피타고라스 정리 이용 대각 길이
            distance = np.linalg.norm(np.array([d1['cx'],d1['cy']])-np.array([d2['cx'],d2['cy']]))
            #np.linalg.norm : 두 벡터 사이 거리 계산하는 함수
            if dx == 0:
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy/dx))#역삼각함수 활용 각도 구하는 방식

            area_diff=abs(d1['w']*d1['h']-d2['w']*d2['h'])/(d1['w']*d1['h'])
            width_diff = abs(d1['w']-d2['w'])/d1['w']
            height_diff = abs(d1['h'] - d2['h'])/d1['h']


            if distance<diagonal_length1*MAX_DIAG_MULTIPLYER and angle_diff<MAX_ANGLE_DIFF\
                and area_diff<MAX_AREA_DIFF and width_diff<MAX_WIDTH_DIFF and height_diff<MAX_HEIGHT_DIFF:
                matched_contours_idx.append(d2['idx'])

        matched_contours_idx.append(d1['idx'])

        if len(matched_contours_idx)<MIN_N_MATCHED:
            continue

        matched_result_idx.append(matched_contours_idx)
        unmatched_contours_idx = []
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contours_idx.append(d4['idx'])
        unmatched_contour = np.take(contour_list,unmatched_contours_idx)
        recursive_contour_list = find_chars(unmatched_contour)
        for idx in recursive_contour_list:
            matched_result_idx.append(idx)
        break
    return matched_result_idx

result_idx = find_chars(possible_contours)
matched_result = []
for idx_list in result_idx:
    matched_result.append(np.take(possible_contours,idx_list))
temp_result=np.zeros((height,width,channel),dtype=np.uint8)
for r in matched_result:
    for d in r:
        cv2.rectangle(temp_result,pt1=(d['x'],d['y']),
                      pt2=(d['x']+d['w'],d['y']+d['h']),
                      color=(255,255,255),thickness=2)

plt.figure(figsize=(12,10))
plt.imshow(temp_result,cmap='gray')
#plt.show()




################step 7 얻어낸 번호판 박스들을 수평 정렬
#affine transform 활용

PLATE_WIDTH_PADDING = 1.8
PLATE_HEIGHT_PADDING = 1.5
MIN_PLATE_RATIO = 3
MAX_PLATE_RATIO = 10

plate_imgs=[]
plate_infos=[]

for i, matched_chars in enumerate(matched_result):
    sorted_chars = sorted(matched_chars,key=lambda x:x['cx'])
    plate_cx = (sorted_chars[0]['cx']+sorted_chars[-1]['cx'])/2
    plate_cy = (sorted_chars[0]['cy']+sorted_chars[-1]['cy'])/2
    plate_width = (sorted_chars[-1]['x']+sorted_chars[-1]['w']-sorted_chars[0]['x'])*PLATE_WIDTH_PADDING

    sum_height = 0
    for d in sorted_chars:
        sum_height+=d['h']

    plate_height = int(sum_height/len(sorted_chars)*PLATE_HEIGHT_PADDING)
    triangle_height = sorted_chars[-1]['cy']-sorted_chars[0]['cy']
    triangle_hypotenus = np.linalg.norm(
        np.array([sorted_chars[0]['cx'],sorted_chars[0]['cy']])-
        np.array([sorted_chars[-1]['cx'],sorted_chars[-1]['cy']])
    )
    angle = np.degrees(np.arcsin(triangle_height/triangle_hypotenus))
    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx,plate_cy),angle=angle,scale=1.0)
    img_rotated = cv2.warpAffine(img_thresh,M=rotation_matrix,dsize=(width,height))
    img_cropped = cv2.getRectSubPix(
        img_rotated,
        patchSize=(int(plate_width),int(plate_height)),
        center=(int(plate_cx),int(plate_cy))
    )
    if img_cropped.shape[1]/img_cropped.shape[0]<MIN_PLATE_RATIO or\
        img_cropped.shape[1]/img_cropped.shape[0]<MIN_PLATE_RATIO>MAX_PLATE_RATIO:
        continue

    plate_imgs.append(img_cropped)
    plate_infos.append({
        'x':int(plate_cx-plate_width/2),
        'y':int(plate_cy-plate_height/2),
        'w':int(plate_width),
        'h':int(plate_height)
    })
    plt.figure(figsize=(12,10))
    plt.imshow(img_cropped,cmap='gray')
    #plt.show()







################step 8 현재 img_cropped 이미지 퀄리티로는 OCR의 인식이 떨어진다.
#한번 더 이미지를 정돈하는 작업을 수행.

longest_idx,longest_txt = -1,0
plate_chars=[]

for i , plate_img in enumerate(plate_imgs):
    plate_img = cv2.resize(plate_img,dsize=(0,0),fx=1.6,fy=1.6)
    _,plate_img = cv2.threshold(plate_img,thresh=0.0,maxval=255.0,type=cv2.THRESH_OTSU)

    contours,_ = cv2.findContours(plate_img,mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE)
    plate_min_x,plate_min_y=plate_img.shape[1],plate_img.shape[0]
    plate_max_x,plate_max_y=0,0

    for contour in contours:
        x,y,w,h=cv2.boundingRect(contour)
        area=w*h
        ratio=w/h
        if area>MIN_AREA and w>MIN_WIDTH and h>MIN_HEIGHT and MIN_RATIO<ratio<MAX_RATIO:
            if x<plate_min_x:
                plate_min_x=x
            if y < plate_min_y:
                plate_min_y = y
            if x+w>plate_max_x:
                plate_max_x=x+w
            if y+h>plate_max_y:
                plate_max_y=y+h

    img_result=plate_img[plate_min_y:plate_max_y,plate_min_x:plate_max_x]
    print(img_result.shape)
    plt.figure(figsize=(12,10))
    plt.imshow(img_result,cmap='gray')
    #plt.show()
    img_result=cv2.GaussianBlur(img_result,ksize=(1,1),sigmaX=0)
    _,img_result=cv2.threshold(img_result,thresh=0.0,maxval=255.0,type=cv2.THRESH_OTSU)
    img_result=cv2.copyMakeBorder(img_result, top=20,bottom=20,left=20,right=20,
                                  borderType=cv2.BORDER_CONSTANT,
                                  value=(0,0,0))
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    img_result = cv2.dilate(img_result, k)
    plt.figure(figsize=(12,10))
    plt.imshow(img_result,cmap='gray')
    #plt.show()
chars = pytesseract.image_to_string(img_result,lang='kor+eng',config='--psm 13 --oem 2')
print(chars)