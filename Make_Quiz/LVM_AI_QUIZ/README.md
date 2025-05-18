# Run 3d shape matching test for AI API
Test Large Vision Language Models on multichoice visual matching test. Work for GPT,LLAMA,Claude, and Gemini.
The classes are general **api_class.py are classes for visual query of the main models (gemini,LLama,Claude,Gemini).
QuizMakingClass.py Assume that the images in the test folder and with .jpg. And that each leaf subfolder contain images of same instance.
Generate 4 panel image in panel A and another random panel belong to same instance (Sub folders) and the rest of the images are of different instances.
Use this images to test the models.

# How to use:
Get API keys and set models API key in API_KEYS.py.
In **Quiz.py set path to image dir in in_dir parameter (You cant use the test_images folder supplied).
Set path to output folder where results will be saved to out_folder.
Run script.

###  For more details see [Do large language vision models understand 3D shapes?](https://arxiv.org/pdf/2412.10908)

Sample test images are available [here](https://github.com/sagieppel/Can-vision-language-models-understand-and-match-3D-shapes/tree/main/Make_Quiz/test_images).

Large set of test images are vailable [here](https://drive.google.com/file/d/1NAPLUJSemckBSlbnRZYRKiO7McINuPXL/view?usp=sharing).

