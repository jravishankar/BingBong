import cv2, os, sys
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def generate_csv(techniqueDir):
    technique_name = techniqueDir.split('/')[-1]
    imgDir = os.path.join(techniqueDir, 'img')
    image_files = [os.path.join(imgDir, imageName) for imageName in sorted(os.listdir(imgDir))]
    annImgDir = os.path.join(techniqueDir, 'ann_img')
    os.makedirs(annImgDir, exist_ok = True)

    
    
    BG_COLOR = (192, 192, 192) # gray
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:
      for idx, file in enumerate(image_files):
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            print("No Pose landmarks: {}".format(file))
            continue

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
        file_name = file.split(".")[0]
        ann_image_name = file_name + '_ann' + '.png'
        cv2.imwrite(os.path.join(annImgDir, ann_image_name), annotated_image)
        # Plot pose world landmarks.
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

if __name__ == "__main__":
    currDir = os.path.dirname(os.path.realpath(__file__))
    proVideoDir = os.path.join(currDir, 'proVideos')
    technique = sys.argv[1]
    techniqueDir = os.path.join(proVideoDir, technique)
    generate_csv(technique, techniqueDir)



