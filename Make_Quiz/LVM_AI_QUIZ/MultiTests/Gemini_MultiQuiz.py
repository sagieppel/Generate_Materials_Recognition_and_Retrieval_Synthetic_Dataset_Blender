import cv2
import os
import random
import numpy as np
import gemini_api_class
import QuizMakingClass
#gemini-1.5-pro,"gemini-2.0-flash-exp"

AI_bot = gemini_api_class.gemini_bot(model="gemini-1.5-pro")

main_in_dir = "/media/deadcrow/6TB/python_project/Can_LVM_See3D/All_Tests/"
main_out_dir = "/media/deadcrow/6TB/python_project/Can_LVM_See3D/Results_gemini_1.5pro/"
if not os.path.exists(main_out_dir): os.mkdir(main_out_dir)
for sdir in os.listdir(main_in_dir):

    input_dir =  main_in_dir + "//" + sdir + "//"
    print(input_dir)
    if not os.path.isdir(input_dir): continue
    error_dir = main_out_dir +  "//"  + sdir + "//"
    if os.path.exists(error_dir + "/logs.txt"): continue
    save_error=True
    save_all=True
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir,neg_same_cat = False, max_img_per_object=3)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all)

