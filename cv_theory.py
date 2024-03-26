#opencv 영상처리
import cv2
print(cv2.__version__) #4.9.0 ver 확인

# cv2 : imread videocapture
# cv2는 단일 영상 (frame,이미지) 혹은 video를 다루는 패키지
# 저장된 영상, 실시간 영상에 대한 데이터 처리 가능
# (0)은 기본 카메라 장치, 내장 웹캠 0번
image = cv2.imread("new_image.jpg",cv2.IMREAD_ANYCOLOR)
#CV2.IMREAD 플래그 종류
#IMREAD_ANYCOLOR : 3채널 이미지
#IMREAD_COLOR : BGR 이미지 (3채널)
#IMREAD_UNCHANGED : 원본 사용
#IMPRAD_GRAYSCALE : 흑백 처리 이미지 사용 (1채널)
#IMREAD_REDUCED_GRAYSCALE_2 : 사이즈 1/2로 줄이고, 그레이스케일
cv2.imshow("image", image)
cv2.waitKey()
cv2.destroyAllWindows()

# #capture = cv2.VideoCapture('v.mp4')
# capture = cv2.VideoCapture(0)
# # 프레임 사이즈 정하기
# capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# # set 함수로 카메라 속성 설정 가능
# # 속성명과 밸류 형태로 매개변수 지정
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
# while cv2.waitKey(30) < 0:
#     # 위 waitkey 30 < 0 은 사용자의 키 이벤트 대기 루프
#     # 30ms로 설정하고
#     # 키 입력이 없으면 -1을 반환
#     # 키 입력이 들어오면 ord('x')
#     # 위 조건 아무 키나, 키 이벤트 발생하면
#     ret,frame=capture.read()
#     cv2.imshow("result Frame",frame)
# capture.release()
# cv2.destroyAllWindows()