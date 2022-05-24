import cv2, os, sys, csv
import mediapipe as mp
import numpy as np
from natsort import natsorted, ns
from embedder import FullBodyPoseEmbedder
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def generate_csv_and_anns(caller, videoDir):
    if caller == 'user':
        # in this case videoDir is actually the path to the video itself
        
        videoPath = videoDir
        techniqueDir = ('/').join(videoDir.split('/')[:-1])
        imgDir = os.path.join(techniqueDir, 'img')
        os.makedirs(imgDir, exist_ok = False)
        print(videoPath)
        print(imgDir)
        os.system('ffmpeg -i {}.mp4 -vf fps=60 {}/out%d.png'.format(videoPath, imgDir))

    else:
        techniqueDir = videoDir
    print(techniqueDir)
    technique_name = techniqueDir.split('/')[-1]
    imgDir = os.path.join(techniqueDir, 'img')
    image_files = [os.path.join(imgDir, imageName) for imageName in natsorted(os.listdir(imgDir)) if not imageName.startswith('.')]
    embedder = FullBodyPoseEmbedder()
    annImgDir = os.path.join(techniqueDir, 'ann_img')
    os.makedirs(annImgDir, exist_ok = True)
    BG_COLOR = (192, 192, 192) # gray
    csvPath = os.path.join(techniqueDir, technique_name + '.csv')
    pose_landmarks_array = []
    with open(csvPath, 'w') as csvFile:
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
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            file_name = file.split("/")[-1].split('.')[0] 
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
            csv_out_writer.writerow([file] + pose_landmarks.flatten().astype(np.str).tolist() + [pose_size])


    if caller == "user": 
        ## in main file logic, we create all the necessary data (anns, csv) for visualizations 
        ## and then return the user data for calculation processing immediately
        return pose_landmarks_array


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







