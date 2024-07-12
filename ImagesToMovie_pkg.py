
import pandas as pd
import numpy as np
import glob
import os
import cv2
from datetime import datetime
import pathlib
import shutil
#
def move_files(mv_list_files,folder_files,f_source,f_dest):
    rm_fl=[]
    for t in mv_list_files:
        idx=np.where(folder_files==t)
        #print(idx,t)
        try:
            shutil.move((os.path.join(f_source,(folder_files[idx[0]][0])+'.jpg')),f_dest)
            rm_fl.append(folder_files[idx[0]][0])
            #print(rm_fl)

        except:
            pass
    return rm_fl

def Filter_imgs(jitFile,DataFold):
    d=[]
    data= (pd.read_csv(jitFile, sep=',')).transpose()
    Data=data.values
    mvDir=os.path.join(DataFold,'Bad_images')
    pathlib.Path(mvDir).mkdir(parents=True, exist_ok=True)
    pos1=np.where(abs(Data[2])>50)
    files = sorted(glob.glob(DataFold+'*.jpg'))
    fold_fnm=np.array([ (os.path.basename(f))[:-4] for f in files]) #jpg
    list_fnm=np.array([ f[:-5] for f in Data[0]]) #fits
    pos1=np.array(pos1)

    mv_list_files=list_fnm[pos1[0]]
    print('====================')
    print("Found few off images: ",mv_list_files)
    rm_file=move_files(mv_list_files,fold_fnm,DataFold,mvDir)
    print('Moved Bad images (x):',rm_file)
    pos4=np.where(abs(Data[3])>50)
    mv_list_files2=list_fnm[pos4[0]]
    rm_file=move_files(mv_list_files2,fold_fnm,DataFold,mvDir)
    print("Found few off images: ",mv_list_files2)
    print('Moved Bad images (y):',rm_file)
    print('====================')


def Make_movie(image_folder, video_name, frame_rate):
    # Get list of images
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()  # Ensure the images are in order

    # Get dimensions of the images
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_name, fourcc, frame_rate, (width, height))

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release the video writer object
    video.release()
    print(f"Video {video_name} created successfully.")
