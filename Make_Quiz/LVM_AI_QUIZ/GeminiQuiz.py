import cv2
import os
import random
import numpy as np
import gemini_api_class
import QuizMakingClass
#gemini-1.5-pro,"gemini-2.0-flash-exp"

AI_bot = gemini_api_class.gemini_bot(model="gemini-2.0-flash-exp")

input_dir= r"../test_images/"
error_dir = r"GEMINI_LOGS_2.0-flash-exp/"
save_error=True
save_all=True
if __name__ == '__main__':
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir,neg_same_cat = False, max_img_per_object=3)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all)

