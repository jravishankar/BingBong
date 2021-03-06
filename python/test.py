# -- coding: utf-8 --
import os, csv
import numpy as np
from embedder import FullBodyPoseEmbedder
from bingbongcore import PoseDifferenceEstimator
from videoToCsv import generate_csv_and_anns
import cv2
import mediapipe.python.solutions.drawing_utils as mp_draw
from PIL import Image, ImageDraw, ImageFont


THICKNESS = 3
RED = (0, 0, 255)
GREEN = (0, 255, 0)
SHIFT = 20
RADIUS = 10
CIRCLE_THICKNESS = -1
# fontPIL = "/Library/Fonts/Arial Unicode.ttf"
# fontScale              = 10
# fontColor              = (255,255,255)
# thickness              = 10
# lineType               = 2


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 2
fontColor              = (255,255,255)
thickness              = 3
lineType               = 2

def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL

def cv2_putText_1(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    imgPIL = cv2pil(img)
    draw = ImageDraw.Draw(imgPIL)
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    draw.text(xy = (x,y), text = text, fill = colorRGB, font = fontPIL)


vid = 'completely_wrong'
technique_id = 'forehand_shakehold_furtherTrim'
currDir = os.path.dirname(os.path.realpath(__file__))
userDir = os.path.join(currDir, 'userVideos', 'PengZhiyu')
proVideoDir = os.path.join(currDir, 'proVideos')
vidPath = os.path.join(userDir, vid, vid)
csvPath = os.path.join(userDir, vid, vid + '.csv')

pro_data_csv_path = os.path.join(proVideoDir, technique_id, technique_id + '.csv')

user_landmarks_array = generate_csv_and_anns('user', vidPath)

pose_embedder = FullBodyPoseEmbedder()
difference_estimator = PoseDifferenceEstimator(pose_embedder, pro_data_csv_path)
#user_landmarks_array = difference_estimator._load_technique_sample(csvPath)
max_numeber, power_size, start, end = difference_estimator(user_landmarks_array)

annimg_path = os.path.join(userDir, vid, 'ann_img')
store_path = os.path.join(userDir, vid, 'recommendation')
os.makedirs(store_path, exist_ok=True)
print(power_size)

for frame in range(start, end+1):

    landmark = user_landmarks_array[frame]
    if power_size[frame] > 1:
        longer = 'pro'
    else:
        longer = 'user'
    if max_numeber == 0:
        # 'ltr'
        user_start_point = pose_embedder._get_average_by_names(landmark, 'left_hip', 'right_hip')
        user_end_point = pose_embedder._get_average_by_names(landmark, 'left_shoulder', 'right_shoulder')
    elif max_numeber == 1:
        # 'l_shoulder_elbow'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
    elif max_numeber == 2:
        # 'r_shoulder_elbow'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
    elif max_numeber == 3:
        # 'l_elbow_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
    elif max_numeber == 4:
        # 'r_elbow_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
    elif max_numeber == 5:
        # 'l_hip_knee'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_knee')]
    elif max_numeber == 6:
        # 'r_hip_knee'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_knee')]
    elif max_numeber == 7:
        # 'l_knee_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_knee')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
    elif max_numeber == 8:
        # 'r_knee_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_knee')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
    elif max_numeber == 9:
        # 'l_shoulder_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
    elif max_numeber == 10:
        # 'r_shoulder_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
    elif max_numeber == 11:
        # 'l_hip_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
    elif max_numeber == 12:
        # 'r_hip_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
    elif max_numeber == 13:
        # 'l_hip_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
    elif max_numeber == 14:
        # 'r_hip_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
    elif max_numeber == 15:
        # 'l_shoulder_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
    elif max_numeber == 16:
        # 'r_shoulder_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
    elif max_numeber == 17:
        # 'l_hip_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
    elif max_numeber == 18:
        # 'r_hip_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
    elif max_numeber == 19:
        # 'ltr_elbow'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
    elif max_numeber == 20:
        # 'ltr_knee'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_knee')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_knee')]
    elif max_numeber == 21:
        # 'ltr_wrist'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
    elif max_numeber == 22:
        # 'ltr_ankle'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
        if longer == 'pro':
            improvement = 'Try spreading your legs a bit!'
        else:
            improvement = 'Try bringing in your legs a bit!'
    elif max_numeber == 23:
        # 'l_bent'
        user_start_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
    elif max_numeber == 24:
        # 'r_bent'
        user_start_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
    else:
        print("max_number error")
        user_start_point = user_end_point = 0

    user_center = ((user_start_point[0]+user_end_point[0])/2, (user_start_point[1]+user_end_point[1])/2)

    pro_start_px = (round((user_start_point[0]-user_center[0])*power_size[frame]+user_center[0]),
                    round((user_start_point[1]-user_center[1])*power_size[frame]+user_center[1]))
    pro_end_px = (round((user_end_point[0]-user_center[0])*power_size[frame]+user_center[0]),
                  round((user_end_point[1]-user_center[1])*power_size[frame]+user_center[1]))

    path = os.path.join(annimg_path, "out"+str(frame+1)+"_ann.png")
    ann_image = cv2.imread(path)
    image = ann_image.copy()
    if image.shape[2] != 3:
        raise ValueError('Input image must contain three channel rgb data.')
    user_start_px = (round(user_start_point[0]),round(user_start_point[1]))
    user_end_px = (round(user_end_point[0]),round(user_end_point[1]))

    image_length, image_width, _ = image.shape

    bottomLeftCornerOfText = (10, image_length - 10)

    cv2.arrowedLine(image, user_end_px, pro_end_px, color=GREEN, thickness=THICKNESS)
    cv2.arrowedLine(image, user_start_px, pro_start_px, color=GREEN, thickness=THICKNESS)
    
    # cv2.line(image, pro_start_px, pro_end_px, color=GREEN, thickness=THICKNESS)
    # cv2.circle(image, pro_start_px, RADIUS, color=GREEN, thickness=CIRCLE_THICKNESS)
    # cv2.circle(image, pro_end_px, RADIUS, color=GREEN, thickness=CIRCLE_THICKNESS)
    cv2.circle(image, user_start_px, RADIUS, color=RED, thickness=CIRCLE_THICKNESS)
    cv2.circle(image, user_end_px, RADIUS, color=RED, thickness=CIRCLE_THICKNESS)
    #cv2pil(image)
    #cv2_putText_1(image, improvement, bottomLeftCornerOfText, fontPIL, fontScale, fontColor)
    cv2.putText(image,improvement, 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
    store_name = "out" + str(frame+1) + "_recommendation.png"
    cv2.imwrite(os.path.join(store_path, store_name), image)
os.system('ffmpeg -r 30 -i {}/out%d_recommendation.png {}/recommendation.mp4'.format(store_path, os.path.join(userDir, vid)))


