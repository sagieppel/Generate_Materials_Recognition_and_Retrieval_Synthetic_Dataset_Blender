
# Generate images of the same  PBR material but on different object/shape but with  differnt orientation and enviroments
# Create material recognition and retrieval dataset multi images of the same material on different object and in different enviroments
# note that this script run with the blend file and refers to some prexisting nodes in the blend it the .py file cannot run stand alone and most run from the blender .blend
###############################Dependcies######################################################################################

import bpy
import math
import numpy as np
import bmesh
import os
import shutil
import random
import json
import sys
filepath = bpy.data.filepath
homedir = os.path.dirname(filepath)
sys.path.append(homedir) # So the system will be able to find local imports
os.chdir(homedir)
import MaterialsHandling as Materials
import ObjectsHandling as Objects
import RenderingAndSaving 
import SetScene
import time
########################################################################################

def ClearMaterials(KeepMaterials): # clean materials from scene
    mtlist=[]
    for nm in bpy.data.materials: 
        if nm.name not in KeepMaterials: mtlist.append(nm)
    for nm in mtlist:
        bpy.data.materials.remove(nm)

################################################################################################################################################################

#                                    Main 

###################################################################################################################################################################


#------------------------Input parameters---------------------------------------------------------------------


#################################Assets folders and output folders##############################################################################

#------------------------Input parameters---------------------------------------------------------------------

# Example HDRI_BackGroundFolder and PBRMaterialsFolder  and ObjectsFolder folders should be in the same folder as the script. 

HDRI_BackGroundFolder=r"HDRI_BackGround//" # Background hdri folder

ObjectMainFolder = r"objects//" #Folder of objects (like objaverseshapenet) 

pbr_folder = r'PBR_Materials//'# folders with PBR materiall each folder will be use with equal chance


OutFolder="output_images_2/" # folder where generated images will be save

#****************************************************************************************************************
#HDRI_BackGroundFolder=r"/media/deadcrow/6TB/Materials_Assets/4k//"
#ObjectMainFolder=r"/media/deadcrow/6TB/Datasets/ObjaverseV1/"#/media/deadcrow/6TB/Datasets/ObjaverseV1/Categories//"
#OutFolder="/media/deadcrow/6TB/python_project/Can_LVM_See3D/All_Tests/10_Everythiong_Different_New_Big_Set_WITH_RESIZE_DISPLACEMENT/" # folder where out put will be save
#pbr_folders = [r'/media/deadcrow/SSD_480GB/PBR_Materials_SEAMLESS_larger_then_512pix//'] # folders with PBR materiall each folder will be use with equal chance

#OutFolder="output_images/" # folder where generated images will be save

#************************************************************

##############################################################################################################


max_renders = 4 # Number of image renders per  PBR material instance 
 
max_materials= 100000 # max different materials to render

orientation = 101 # object orientation if  random_object_orient=False
object_indx = 2#1107# index for the object file that will be loaded for all object (number of the PBR Library)
background_indx = 155# each instance will have different random background (the index is the number of the background HDRI file)
random_object_orient = True #   random object orietnation 
random_texture_orient = False  # each instance will have different random orientation
random_object = True # each instance will have different random object
random_background = True  # each instance will have different random texture
save_masks=True # save objecty mask


use_priodical_exits = False # Exit blender once every few sets to avoid memory leaks, assuming that the script is run inside Run.sh loop that will imidiatly restart blender fresh
 
#==================================================================================================================================================================
#------------------Create PBR list from the PBR material folder-------------------------------------------------------- 
materials_lst = [] # List of all pbr materials folders path
for sdir in  os.listdir(pbr_folder): # go over all pbrs in folder
        if os.path.isdir(pbr_folder+"//"+sdir+"//"):
              materials_lst.append(sdir)
              
#------------------------------------Create list with all hdri files in the folder (for background)-------------------------------------
hdr_list=[]
for hname in os.listdir(HDRI_BackGroundFolder): 
   print("#####",hname)
   if ".hdr" in hname or ".exr" in hname:
         hdr_list.append(HDRI_BackGroundFolder+"//"+hname)


#---------------------------------Take files Create Object list-------------------------------------------------------------------------------------
object_list = []
for dr1 in os.listdir(ObjectMainFolder):   
    path1 = ObjectMainFolder+ "/"+ dr1 
    if os.path.isfile(path1): 
        object_list.append(path1)
    if os.path.isdir(path1): 
         for fl2 in os.listdir(path1):
              path2 = path1 + "/"+ fl2 
              if os.path.isfile(path2): 
                            object_list.append(path2)

#--------------------------Select background/object if they are not random--------------------------------------

if not random_object:# limit object to single one
     object_list = object_list[object_indx:object_indx+1]

if not random_background:  # limit background/enviroment to single one    
       hdr_list = hdr_list[background_indx:background_indx+1]
     


#==============Set Rendering engine parameters (for image creaion)==========================================

bpy.context.scene.render.engine = 'CYCLES' # 
bpy.context.scene.cycles.device = 'GPU' # If you have GPU 


# Ensure we're using the correct context
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'






########################################
#bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL' # Not sure if this is really necessary but might help with sum surface textures
bpy.context.scene.cycles.samples = 120 #200, #900 # This work well for rtx 3090 for weaker hardware this can take lots of time
bpy.context.scene.cycles.preview_samples = 900 # This work well for rtx 3090 for weaker hardware this can take lots of time

bpy.context.scene.render.resolution_x = 512 # output image size 
bpy.context.scene.render.resolution_y = 512 # output image size

bpy.context.scene.cycles.use_preview_denoising = True
bpy.context.scene.cycles.use_denoising = True




#---------------List of materials that are part of the blender structure and will not be deleted------------------------------------------
MaterialsList=["PbrMaterial1","Black","White"] # Material graphs that will be used

#-------------------------Create output folder--------------------------------------------------------------


if not os.path.exists(OutFolder): os.mkdir(OutFolder)



#----------------------------------------------------------------------
######################Main Generation loop##########################################################\

scounter=0 # Count how many scene have been made

#------go over all PBR materials in the PBR list for each generate multiple image of same material in different settings-----------
for nmat,dir_material  in  enumerate(materials_lst):
                   if nmat>max_materials: break
                   path_material = pbr_folder+"/" + dir_material +"/"
                   out_mat_dir=OutFolder +"/" + dir_material +"/"
                   print("********",dir_material)
                   if os.path.exists(out_mat_dir):  continue # avoid reedoing existing materials
                   os.mkdir(out_mat_dir)
                  
                
                   Materials.load_PBR_material(bpy.data.node_groups["Phase1"],path_material) # load material
                   
                  
#------------------------------Generate multiple images of the same material---------------------------                
                   for n_im in range(max_renders):
                        
                           if os.path.exists(out_mat_dir+"//"+str(n_im)+'.jpg'): continue # avoid redo existing 
                           
                           SetScene.CleanScene()  # Delete all objects in scence
                          
                           object_path=object_list[np.random.randint(len(object_list))] # pick random object
                           MainObjectName=Objects.LoadObject([0,0,0],1,object_path) # LOAD OBJECT
                           ####ClearMaterials(KeepMaterials=MaterialsList)
                           MainObject = bpy.data.objects[MainObjectName]     
                           Materials.ReplaceMaterial(MainObject,bpy.data.materials['PbrMaterial1']) # replace material on object
                           SetScene.AddBackground(hdr_list) # Add randonm Background hdri from hdri folder
                           if random_texture_orient: # randomize texture orientation
                                      Materials.Randomize_RotateTranslate_PBR_MaterialMapping(bpy.data.node_groups["Phase1"])
                     
                           if random_object_orient: # randomize the orientation of the object the material appear on
                               for i in range(3): # set object orientation
                                          orientation = np.random.rand()*6.2831853
                                          bpy.data.objects[MainObjectName].rotation_quaternion[i] = orientation
                            # randomize background orientation
                           for i in range(3):   # Select random background 
                                         if random_background:                            
                                                   bpy.data.worlds["World"].node_tree.nodes["Mapping"].inputs[2].default_value[i] = np.random.rand()*6.2831853  # randomize background orientation
                                         else:
                                             bpy.data.worlds["World"].node_tree.nodes["Mapping"].inputs[2].default_value[i] = 0
                          # bpy.data.worlds["World"].node_tree.nodes["Mapping"].inputs[2].default_value[1] = 3.14
                           #bpy.data.worlds["World"].node_tree.nodes["Background.001"].inputs[1].default_value = 1
                           #bpy.data.objects[MainObjectName].rotation_euler=(0,0,0)
                            
                      
                           bpy.context.scene.render.engine = 'CYCLES'
                           SetScene.SetCamera(name="Camera", lens = 32, location=(0,0,0.65+np.random.rand()*0.85),rotation=(0, 0, 0),shift_x=0,shift_y=0)
#                           bpy.data.objects['Camera'].location=(0, 0, 20)
#                           bpy.data.objects['Camera'].rotation_euler=[0,0,0]
            #-------------------------------------------------------Save images--------------------------------------------------------------    
                        
                           RenderingAndSaving.RenderImageAndSave(FileNamePrefix=str(n_im),OutputFolder=out_mat_dir) # Render image and save
                          ### x=sfdsfds
                           if save_masks:  RenderingAndSaving.SaveObjectFullMask([MainObjectName],out_mat_dir + "/"+str(n_im) +"_MASK.png")
        #-------------Delete all objects from scene but keep materials---------------------------
                           objs = []
                           for nm in bpy.data.objects: objs.append(nm)
                           for nm in objs:  bpy.data.objects.remove(nm)
                   imlist=[]
                   for nm in bpy.data.images: imlist.append(nm) 
                   for nm in imlist:
                            bpy.data.images.remove(nm)
                                # Clean materials
                   ClearMaterials(KeepMaterials=MaterialsList)
                   print("========================Finished==================================")
                   SetScene.CleanScene()  # Delete all objects in scence
                   scounter+=1
                   if  scounter>200 and use_priodical_exit: 
                       # Blender have tendency for memory leak and rendering time slowly increaseing over many runs, this wil exit thr blender and will clean memory (Assuming the main script run inside run.sh that will imidiatly restart the script
                       # Use this if you need to collect loots of data and encounter slowing down issues
                               print("quit")
                               bpy.ops.wm.quit_blender()
                                                    
