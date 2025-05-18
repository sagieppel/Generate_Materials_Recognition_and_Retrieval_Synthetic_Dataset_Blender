#https://ai.google.dev/gemini-api/docs/quickstart?lang=python
#https://ai.google.dev/gemini-api/docs/billing
#https://ai.google.dev/gemini-api/docs/models/gemini
#https://aistudio.google.com/plan_information
import os
import base64
import google.generativeai as genai
import API_KEYS
import cv2

# Set your API key
genai.configure(api_key=API_KEYS.gemini_api_key)
sleep_time=3

import PIL.Image

class gemini_bot():
  def __init__(self,model):
          self.model = genai.GenerativeModel(model_name=model)

  ###########################Question text image##########################################################################################
  def question_text_image(self,text,image):
          image_path="temp_im.jpg"
          cv2.imwrite(image_path,image)
          img = PIL.Image.open(image_path)
          for i in range(500):
              try:
                    response = self.model.generate_content([img, text])
                    break
              except:
                  import time
                  print("Fail contact gemini sleeping ",sleep_time," seconds and retry")
                  time.sleep(sleep_time)
          return response.text
###########################Question text##########################################################################################
  def question_text(self, text):
      for i in range(500):
          try:
              response = self.model.generate_content([text])
              break
          except:
              import time
              print("Fail contact gemini sleeping ",sleep_time," seconds and retry")
              time.sleep(sleep_time)
      return response.text
###########################Full questions############################################################################################
  def answer_question(self,image):
      # various
      queries=[ # the queries will be given in this order the next query will be given only if the model will refuse to answer the previous one
           ("Which of the panels contain object with identical 3d shape  to the object in panel A. Your answer must come as a single letter"),

         ("Which of the panels contain object that is identical in 3d shape to the object in panel A. Your answer must come as a single letter: B,C,D"),

         ("Carefully analyze the image. In panel A, there is an object with a specific shape. Your task is to identify which other panel (B, C, or D) contains an object that"
          "\n1) Has the exact same 3d shape as the object in panel A."
          "\n2) Might Have a different orientation compared to the object in panel A."
          "\n3) Might have a different texture compared to the object in panel A."
          "Respond with ONLY the letter of the panel (B, C, or D) that meets all these criteria."),

          (    "The image contain 4 panels (A,B,C,D). "
            "The each panel contain object. "   
           "One of the panels C-D contain object that is identical in shape to the object in panel A."# #but  have different  background"#, orientation and texture. "
           "Which panel is this? Your answer must be a single letter (B,C or D)")]


      #-----------------repeat queries until getting correct format of answr (b,c,d)
      for ii in range(len(queries)):
          all_text = "\n\n query: " + queries[ii]+"\n"  # use to record full interaction
          ky = self.question_text_image(queries[ii], image)
          all_text += str(ii) + ") response:  " + ky +"\n"

          if len(ky) > 1 or ky.lower() not in ['b', 'c', 'd']:
              ky=self.question_text("Take the following response and reduce it to a single letter:\n"+ky)
              all_text += str(ii) +")Take the following response and reduce it to a single letter: response:  " + ky
              if len(ky)>1:
                  if (" B" in ky) and (" C" not in ky) and (" D" not in ky): ky = "B"
                  if (" B" not in ky) and (" C" in ky) and (" D" not in ky): ky = "C"
                  if (" B" not in ky) and (" C" not in ky) and (" D" in ky): ky = "D"
                  all_text += str(ii) + ")Extracting answer"+str(ii)

          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
               return ky, all_text



