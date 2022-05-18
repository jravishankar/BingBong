# -- coding: utf-8 --
import os, csv
import numpy as np
from embedder import FullBodyPoseEmbedder
from bingbongcore import PoseDifferenceEstimator as Pose

user_test = "IMG_1064"
technique = "forehandDrive"

pose_embedder = FullBodyPoseEmbedder()

# load user's csv
currDir = os.path.dirname(os.path.realpath(__file__))
userDir = os.path.join(currDir, 'user_test')
csvPath = os.path.join(userDir, user_test, user_test+'.csv')
with open(csvPath) as csvFile:
    embedding_by_frame = []
    csv_reader = csv.reader(csvFile, delimiter=',')
    for row in csv_reader:
        landmarks = np.array(row[1:], np.float32).reshape([33, 3])
        embedding_by_frame.append(pose_embedder(landmarks))

pose_difference = Pose(pose_embedder, technique)
user_embedding = pose_difference(embedding_by_frame)
