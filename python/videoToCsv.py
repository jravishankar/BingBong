import cv2, os, sys, csv
import mediapipe as mp
import numpy as np
from natsort import natsorted, ns
from embedder import FullBodyPoseEmbedder
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

import platform
if platform.system().lower() == 'windows':
    pathSeparator = '\\'
else:
    pathSeparator = '/'

def generate_csv_and_anns(caller, videoDir):
    if caller == 'user':
        # in this case videoDir is actually the path to the video itself
        
        videoPath = videoDir
        techniqueDir = pathSeparator.join(videoDir.split(pathSeparator)[:-1])
        imgDir = os.path.join(techniqueDir, 'img')
        os.makedirs(imgDir, exist_ok = False)
        print(videoPath)
        print(imgDir)
        os.system('ffmpeg -i {} -vf fps=60 {}/out%d.png'.format(videoPath, imgDir))

    else:
        techniqueDir = videoDir
    print(techniqueDir)
    technique_name = techniqueDir.split(pathSeparator)[-1]
    imgDir = os.path.join(techniqueDir, 'img')
    image_files = [os.path.join(imgDir, imageName) for imageName in natsorted(os.listdir(imgDir)) if not imageName.startswith('.')]
    embedder = FullBodyPoseEmbedder()
    annImgDir = os.path.join(techniqueDir, 'ann_img')
    os.makedirs(annImgDir, exist_ok = False)
    BG_COLOR = (192, 192, 192) # gray
    csvPath = os.path.join(techniqueDir, technique_name + '.csv')
    pose_landmarks_array = []
    with open(csvPath, 'w', newline='') as csvFile:
        csv_out_writer = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
          for idx, file in enumerate(image_files):
            #print(file)
            image = cv2.imread(file)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            input_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(input_frame)
            
            if not results.pose_landmarks:
                print("Pose landmarks could not be read from file: {}".format(file))
                continue

            ## For annotated images

            annotated_image = image.copy()
            # Draw segmentation on the image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            #condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            #bg_image = np.zeros(image.shape, dtype=np.uint8)
            #bg_image[:] = BG_COLOR
            #annotated_image = np.where(condition, annotated_image, bg_image)
            #annotated_image = 
            # Draw pose landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            file_name = file.split(pathSeparator)[-1].split('.')[0]
            ann_image_name = file_name + '_ann' + '.png'
            ann_file_path = os.path.join(annImgDir, ann_image_name)
            #print(ann_file_path)
            cv2.imwrite(ann_file_path, annotated_image)
            # Plot pose world landmarks.
            #mp_drawing.plot_landmarks(
            #    results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

            ## For actually writing the csv file
            pose_landmarks = results.pose_landmarks

            

            pose_landmarks = np.array(
                [[lmk.x * image_width, lmk.y * image_height, lmk.z * image_width]
                 for lmk in pose_landmarks.landmark],
                dtype=np.float32)
            assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)
            pose_landmarks_array.append(pose_landmarks)
            pose_size = embedder._get_pose_size(pose_landmarks, embedder._torso_size_multiplier)
            csv_out_writer.writerow([file] + pose_landmarks.flatten().astype(np.str).tolist())


    if caller == "user": 
        ## in main file logic, we create all the necessary data (anns, csv) for visualizations 
        ## and then return the user data for calculation processing immediately
        return pose_landmarks_array


def write_annotated_recommendation(annimg_path, store_path, user_video_dir, user_landmarks_array, embedder, diff_tuple):

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 2
    fontColor              = (255,255,255)
    thickness              = 3
    lineType               = 2
    pose_embedder = embedder

    THICKNESS = 3
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    SHIFT = 10
    RADIUS = 10
    CIRCLE_THICKNESS = -1
    max_number, power_size, start, end = diff_tuple
    for frame in range(start, end+1):

        landmark = user_landmarks_array[frame]
        if power_size[frame] > 1:
            longer = 'pro'
        else:
            longer = 'user'
        if max_number == 0:
            # 'ltr'
            user_start_point = pose_embedder._get_average_by_names(landmark, 'left_hip', 'right_hip')
            user_end_point = pose_embedder._get_average_by_names(landmark, 'left_shoulder', 'right_shoulder')
        elif max_number == 1:
            # 'l_shoulder_elbow'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
        elif max_number == 2:
            # 'r_shoulder_elbow'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
        elif max_number == 3:
            # 'l_elbow_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        elif max_number == 4:
            # 'r_elbow_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        elif max_number == 5:
            # 'l_hip_knee'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_knee')]
        elif max_number == 6:
            # 'r_hip_knee'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_knee')]
        elif max_number == 7:
            # 'l_knee_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_knee')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
        elif max_number == 8:
            # 'r_knee_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_knee')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
        elif max_number == 9:
            # 'l_shoulder_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        elif max_number == 10:
            # 'r_shoulder_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        elif max_number == 11:
            # 'l_hip_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
        elif max_number == 12:
            # 'r_hip_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
        elif max_number == 13:
            # 'l_hip_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        elif max_number == 14:
            # 'r_hip_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        elif max_number == 15:
            # 'l_shoulder_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
        elif max_number == 16:
            # 'r_shoulder_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_shoulder')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
        elif max_number == 17:
            # 'l_hip_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
        elif max_number == 18:
            # 'r_hip_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('right_hip')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        elif max_number == 19:
            # 'ltr_elbow'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_elbow')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_elbow')]
        elif max_number == 20:
            # 'ltr_knee'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_knee')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_knee')]
        elif max_number == 21:
            # 'ltr_wrist'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_wrist')]
        elif max_number == 22:
            # 'ltr_ankle'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
            user_end_point = landmark[pose_embedder._landmark_names.index('right_ankle')]
            if longer == 'pro':
                improvement = 'Try spreading your legs a bit!'
            else:
                improvement = 'Try bringing in your legs a bit!'
        elif max_number == 23:
            # 'l_bent'
            user_start_point = landmark[pose_embedder._landmark_names.index('left_wrist')]
            user_end_point = landmark[pose_embedder._landmark_names.index('left_ankle')]
        elif max_number == 24:
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
    os.system('ffmpeg -r 30 -i {}/out%d_recommendation.png {}/recommendation.mp4'.format(store_path, user_video_dir))





if __name__ == "__main__":
    currDir = os.path.dirname(os.path.realpath(__file__))
    proVideoDir = os.path.join(currDir, 'proVideos')
    userVideoDir = os.path.join(currDir, 'userVideos')
    caller = sys.argv[1]
    if caller == "user":
        assert len(sys.argv) == 4, print("Argument error")
        userId, videoId = sys.argv[2], sys.argv[3]
        videoDir = os.path.join(userVideoDir, userId, videoId)
        videoPath = os.path.join(videoDir, videoId)
    elif caller == "pro":
        technique = sys.argv[2]
        videoDir = os.path.join(proVideoDir, technique)
        videoPath = os.path.join(videoDir, technique)
    else:
        print("Can only call videoToCsv on user or pro videos (There are no other types of videos!)")
    imgDir = os.path.join(videoDir, 'img')
    os.makedirs(imgDir, exist_ok = False)
    os.system('ffmpeg -i {}.mp4 -vf fps=60 {}/out%d.png'.format(videoPath, imgDir))
    generate_csv_and_anns(caller, videoDir)







