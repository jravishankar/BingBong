# -- coding: utf-8 --
import os, csv
import numpy as np
from embedder import FullBodyPoseEmbedder
from bingbongcore import PoseDifferenceEstimator
from videoToCsv import generate_csv_and_anns


def load_technique_sample(technique_csv_path):
    """Loads the technique data from the csv file created by proLandmarkGenerator"""
    landmarks_by_frame = [] # a list containing f landmark arrays ( of dimension n_landmarks x n_dimensions ) where f is the number of frames used
    with open(technique_csv_path) as csvFile:
        csv_reader = csv.reader(csvFile)
        for row in csv_reader:
            assert len(row) == 33 * 3 + 1, 'Wrong number of values: {}'.format(len(row))
            landmarks = np.array(row[1:-1], np.float32).reshape([33 , 3])
            landmarks_by_frame.append(landmarks)
    return landmarks_by_frame

vid = 'forehand_shakehold'
technique_id = 'forehand_shakehold_furtherTrim'
currDir = os.path.dirname(os.path.realpath(__file__))
userDir = os.path.join(currDir, 'userVideos', 'WhiteMan')
proVideoDir = os.path.join(currDir, 'proVideos')
vidPath = os.path.join(userDir, vid, vid)
csvPath = os.path.join(userDir, vid, vid + '.csv')

pro_data_csv_path = os.path.join(proVideoDir, technique_id, technique_id + '.csv')

user_landmarks_array = generate_csv_and_anns('user', vidPath)
#user_landmarks_array = load_technique_sample(csvPath)
pose_embedder = FullBodyPoseEmbedder()
difference_estimator = PoseDifferenceEstimator(pose_embedder, pro_data_csv_path)
difference_estimator(user_landmarks_array)


