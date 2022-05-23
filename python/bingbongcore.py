import numpy as np
import os, csv, math, copy
import matplotlib.pyplot as plt


class PoseDifferenceEstimator(object):
    """Calculates differences between user and pro pose landmarks."""

    def __init__(self,
                 pose_embedder,
                 technique,
                 file_extension='csv',
                 file_separator=',',
                 n_landmarks=33,
                 n_dimensions=3,
                 top_n_by_max_distance=30,
                 top_n_by_mean_distance=10,
                 axes_weights=(1., 1., 0.2)):
        currDir = os.path.dirname(os.path.realpath(__file__))
        self.proVideoDir = os.path.join(currDir, 'proVideos')
        self._pose_embedder = pose_embedder
        # self._technique = technique
        self._n_landmarks = n_landmarks
        self._n_dimensions = n_dimensions
        self._top_n_by_max_distance = top_n_by_max_distance
        self._top_n_by_mean_distance = top_n_by_mean_distance
        self._axes_weights = axes_weights
        self._pro_embedding_by_frame = self._load_technique_sample(technique)
        self.file_extension = file_extension
        self.file_separator = file_separator

        self.score_x = 1/6


    def _load_technique_sample(self, technique):
        """Loads the technique data from the csv file created by proLandmarkGenerator"""
        csvPath = os.path.join(self.proVideoDir, technique, technique+'.csv')
        embedding_by_frame = [] # a list containing f landmark arrays ( of dimension n_landmarks x n_dimensions ) where f is the number of frames used
        with open(csvPath) as csvFile:
            csv_reader = csv.reader(csvFile, delimiter=self.file_separator)
            for row in csv_reader:
                assert len(row) == self._n_landmarks * self._n_dimensions + 1, 'Wrong number of values: {}'.format(len(row))
                landmarks = np.array(row[1:], np.float32).reshape([self._n_landmarks , self._n_dimensions])
                embedding_by_frame.append(self._pose_embedder(landmarks))
        return embedding_by_frame

    
    def __call__(self, user_landmarks_by_frame):
        """Calculates the difference between the pro video and the given user video
    
        NOTE: Input is a list of user LANDMARKS not embedding, embedding will be done within the call itself
        """
        user_embedding_by_frame = [self._pose_embedder(user_lmks) for user_lmks in user_landmarks_by_frame]
        flip_user_embedding_by_frame = [self._pose_embedder(user_lmks * np.array([-1, 1, 1])) for user_lmks in user_landmarks_by_frame]
        user_embedding_tuple = (user_embedding_by_frame. flip_user_embedding_by_frame)

        aligned_user_embedding_by_frame = self._align_user_and_pro(user_embedding_tuple)
        assert len(aligned_user_embedding_by_frame) == len(self._pro_embedding_by_frame), "Alignment error"

        scores = self._computation_scores_framewise(aligned_user_embedding_by_frame, self._pro_embedding_by_frame) # frame by frame scores
        embedding_names = self._pose_embedder._get_embedding_names

        # plot
        plt.bar(range(len(embedding_names)), scores, align='center')
        plt.show()

        
        # calculate errors (might want to use self._computation_scores_embeddingwise to make it easier to tell which sections of pose are more off)

        # 1. Is elbow close enough to body
        # 2. Are knees bent enough
        # 3. Is rotation being done properly



    def _align_user_and_pro(self, user_embedding_tuple):
        user_embedding_by_frame = user_embedding_tuple[0]
        flip_user_embedding_by_frame = user_embedding_tuple[1]
        
        num_frames_pro = len(self._pro_embedding_by_frame)
        num_frames_user = len(user_embedding_by_frame)

        # use first and last frames of pro video to get relevant segment of user video
        pro_start_embedding = self._pro_embedding_by_frame[0]
        pro_end_embedding = self._pro_embedding_by_frame[-1]

        user_start_tuple = self._most_similar_pose(user_embedding_by_frame, pro_start_embedding)
        user_end_tuple = self._most_similar_pose(user_embedding_by_frame, pro_end_embedding)

        flip_user_start_tuple = self._most_similar_pose(flip_user_embedding_by_frame, pro_start_embedding)
        flip_user_end_tuple = self._most_similar_pose(flip_user_embedding_by_frame, pro_end_embedding)

        assert user_start_tuple[1] < user_end_tuple[1] or flip_user_start_tuple[1] < flip_user_end_tuple[1], 'Alignment could not be performed because of frame matching error'
        
        ## if flipped embedding causes alignment error, just use original
        ## if original embedding causes alignment error, just use flipped
        if flip_user_start_tuple[1] >= flip_user_end_tuple[1]:
            user_embedding_by_frame_seg = user_embedding_by_frame[user_start_tuple[1]:user_end_tuple[1]+1]
        elif user_start_tuple[1] >= user_end_tuple[1]:
            user_embedding_by_frame_seg = flip_user_embedding_by_frame[flip_user_start_tuple[1]:flip_user_end_tuple[1]+1]
        else:
            ## if neither cause alignment error, choose embedding with least total dissimilarity on alignment frames
            dissimilarity = user_start_tuple[0] + user_end_tuple[0]
            flip_dissimilarity = flip_user_start_tuple[0] + flip_user_end_tuple[0]
            if dissimilarity < flip_dissimilarity:
                user_embedding_by_frame_seg = user_embedding_by_frame[user_start_tuple[1]:user_end_tuple[1]+1]
            else:
                user_embedding_by_frame_seg = flip_user_embedding_by_frame[flip_user_start_tuple[1]:flip_user_end_tuple[1]+1]




        # At this point there are 3 possible cases (regarding user_embedding_by_frame_seg and self._pro_embedding_by_frame)

        
        u_frame_count = len(user_embedding_by_frame_seg)
        p_frame_count = len(self._pro_embedding_by_frame)

        if u_frame_count < p_frame_count: # 1. User has less frames than pro
            aligned_user_embedding_by_frame = self._extend_pose_embedding_by_frame(user_embedding_by_frame, p_frame_count - u_frame_count)

        elif u_frame_count > p_frame_count:  # 2. User has more frames than pro
            self.pro_embedding_by_frame = self._extend_pose_embedding_by_frame(self._pro_embedding_by_frame, u_frame_count - p_frame_count)
            aligned_user_embedding_by_frame = user_embedding_by_frame
       
        else: # 3. Same number of frames
            aligned_user_embedding_by_frame = user_embedding_by_frame

        assert len(aligned_user_embedding_by_frame) == len(self._pro_embedding_by_frame), print("Our extension mechanism doesn't work properly")

        ### original user video
        ### pro video



        # 3. User and pro have an equal amount of frames (likely still misaligned)


        return aligned_user_embedding_by_frame


    def _extend_pose_embedding_by_frame(self, pose_embedding_by_frame, target_frame_count):
        current_frame_count = len(pose_embedding_by_frame)
        assert target_frame_count > current_frame_count, "Error with extending pose embedding, target "
        step = target_frame_count - current_frame_count + 1
        chunks = []
        copies = []
        for i in range(0, current_frame_count, step):
            chunk = copy.deepcopy(pose_embedding_by_frame[i:i+step])
            copies.append(chunk)

        return_embedding_by_frame = []
        for chunk in chunks[:-1]:
            return_embedding_by_frame += chunk + [chunk[-1]]

        return_embedding_by_frame += chunks[-1]
        return return_embedding_by_frame


    def _computation_scores_framewise(self, target_embedding_1, target_embedding_2):
    	# Compute the mean distance between embeddings on each frame
    	# Length of results vector is equal to number of frames i.e. len(target_embedding_1)
        scores = []
        for frame_1, frame_2 in zip(target_embedding_1, target_embedding_2):
            mean_dist = np.mean(np.abs(frame_1 - frame_2) * self._axes_weights)
            print(mean_dist)
            scores.append(math.atan(self.score_x * mean_dist)/(math.pi/2))

        return scores

    def _computation_scores_embeddingwise(self, target_embedding_1, target_embedding_2):
    	# Compute the mean distance of each portion of embedding across all frames
    	# Length of results vector is equal to number of embeddings i.e. target_embedding_1[0].shape[0]
    	num_frames = len(target_embedding_1)
    	embedding_shape = target_embedding_1[0].shape
    	scores_by_embedding = np.zeros(embedding_shape[0])

    	for frame_1, frame_2 in zip(target_embedding_1, target_embedding_2):
            scores_by_embedding += np.mean(np.abs(frame_1 - frame_2) * self._axes_weights, axis = 1)

        return scores_by_embedding/num_frames


    def _most_similar_pose(self, pose_embedding_by_frame, target_embedding):
        min_dist = math.inf
        min_dist_index = 0
        for i, frame_embedding in enumerate(pose_embedding_by_frame):
            mean_dist = np.mean(np.abs(frame_embedding - target_embedding) * self._axes_weights)

            if min_dist > mean_dist:
                min_dist = mean_dist
                min_dist_index = i

        return (min_dist, min_dist_index)



