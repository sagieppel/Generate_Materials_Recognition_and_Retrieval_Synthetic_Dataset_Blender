import os
import cv2
import numpy as np
import shutil
indir = "/media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/All_Test/" # input filter dir
####max_seg=1 # maximum number of none connected segment in object mask
min_occupancy=0.04 # minimum fraction of image occupied by mask
trash_dir= "/media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/All_Tests_trash/" # where filtered files will be saved
##############Recursive scan####################################################################3
def recursive_filter(in_dir,out_dir):
    if not os.path.exists(out_dir): os.mkdir(out_dir)
    for fl in os.listdir(in_dir):
        in_path = in_dir + "//" + fl
        out_path = out_dir + "//" + fl
        if os.path.isdir(in_path):
            recursive_filter(in_path, out_path)

        if "_MASK.png" in fl:
            im=cv2.imread(in_path,0)
            print(in_path)
            im = (im>30).astype(np.uint8)

            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(im, connectivity=8)
            To_Filter=True
            mx_ocp=0
            for ii in np.unique(labels):
                if ii==0: continue
                if (labels ==ii).mean()> mx_ocp: mx_ocp=(labels ==ii).mean()
                if  (labels ==ii).mean()>min_occupancy:
                    To_Filter=False
                    break
            print(num_labels)
            if  To_Filter:
                      shutil.move(in_path, out_path)
                      shutil.move(in_path.replace("_MASK.png",".jpg"), out_path.replace("_MASK.png",".jpg"))
                      print("move",in_path, out_path)
                      #
                      # cv2.destroyAllWindows()
                      # cv2.imshow(str(mx_ocp),im*255)
                      # cv2.waitKey()


######################################################################################################
recursive_filter(indir,trash_dir)