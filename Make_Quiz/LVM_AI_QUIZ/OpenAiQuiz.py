import cv2
import os
import random
import numpy as np
import openai_api_class
import QuizMakingClass

AI_bot = openai_api_class.openai_bot(model="gpt-4o",details="high")

input_dir= r"../test_images/"
error_dir = r"GPT4o_LOGS/"
save_error=True
save_all=True
if __name__ == '__main__':
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir,neg_same_cat = False, max_img_per_object=3)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all)

