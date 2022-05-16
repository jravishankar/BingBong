import os, sys


def main():
	os.system('ffmpeg -i {}.mp4 -vf fps=60 {}/out%d.png'.format(os.path.join(techniqueDir, technique), imgDir))
	os.system('python proLandmarkGenerator.py {}'.format(technique))

if __name__ == "__main__":
    currDir = os.path.dirname(os.path.realpath(__file__))
    proVideoDir = os.path.join(currDir, 'proVideos')
    technique = sys.argv[1]
    techniqueDir = os.path.join(proVideoDir, technique)
    imgDir = os.path.join(techniqueDir, 'img')
    os.makedirs(imgDir, exist_ok = False)
    main()