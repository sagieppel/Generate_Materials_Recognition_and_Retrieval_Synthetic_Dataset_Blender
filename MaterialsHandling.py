# Load assign and generate materials (PBR/BSDF)

###############################Dependcies######################################################################################3

import bpy
import math
import numpy as np
import bmesh
import os
import shutil
import random
import json
import sys
import colorsys
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
#sys.path.append("/home/breakeroftime/Desktop/Simulations/ModularVesselContent")
sys.path.append(directory)
os.chdir(directory)


#################################################################################################     

# map node fields to indexes (For the BSDF and Volume Absorbtion)

##############################################################################################
def map_name2indx():
    stm = bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"]
    d={}
    for i in range(len(stm.inputs)):
        fld=stm.inputs[i]
        d[fld.name]=i
    
    stm = bpy.data.materials["TransparentLiquidMaterial"].node_tree.nodes["Volume Absorption"]
    dv={}
    for i in range(len(stm.inputs)):
        fld=stm.inputs[i]
        dv[fld.name]=i
    return d,dv 

###################################################################################################################################

# Transform BSDF Mateiral to dictionary (use to save materials properties for later use)

####################################################################################################################################
def BSDFMaterialToDictionary(bsdf):
    import uuid
    dic={}
    dic["id"] =   str(uuid.uuid4()) # will be use to store and extract material for later use
    for prop in bsdf.inputs:
        if  "array" in str(type(prop.default_value)):
             dic[prop.name] = list(prop.default_value)
        else:
             dic[prop.name] = prop.default_value
        print(prop.name,"=",dic[prop.name])
    return dic
##################################################################################################################################

# LOAD BSDF Mateiral from dictionary (this is use if you want to have same materials in different images

####################################################################################################################################
def BSDFMaterialFromDictionary(bsdf,mat_data_dic):
    for ii,prop in enumerate(bsdf.inputs):
    #   prop.default_value = mat_data_dic[prop.name]     
       bsdf.inputs[ii].default_value  = mat_data_dic[prop.name]    

#####################################################################################3

# Random multiply

#####################################################################################################################
def RandPow(n):
    r=1
    for i in range(int(n)):
        r*=np.random.rand()
    return r






###########################################################################

# Randomize mapping for pbr  (assume existing mapping node in stem and randomize it, stem is a node graph)

###########################################################################
def Randomize_PBR_MaterialMapping(stem):
    # random translation 
    stem["Mapping"].inputs[1].default_value[0] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[1] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[2] = random.uniform(0, 30)
    # random rotation
    stem["Mapping"].inputs[2].default_value[0] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[1] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[2] = random.uniform(0, 6.28318530718)
    # random scalling
    r=10**random.uniform(-2, 0.6)
    stem["Mapping"].inputs[3].default_value[0] = r
    stem["Mapping"].inputs[3].default_value[1] = r
    stem["Mapping"].inputs[3].default_value[2] = r
    if random.random()<0.4:
        stem["Mapping"].inputs[3].default_value[0] = 10**random.uniform(-2, 0.6)
        stem["Mapping"].inputs[3].default_value[1] = 10**random.uniform(-2, 0.6)
        stem["Mapping"].inputs[3].default_value[2] = 10**random.uniform(-2, 0.6)

###########################################################################

# normalize mapping for pbr  (assume existing mapping node )

###########################################################################
def Normalize_PBR_MaterialMapping(stem):
    # random translation 
    stem["Mapping"].inputs[1].default_value[0] = 0
    stem["Mapping"].inputs[1].default_value[1] = 0
    stem["Mapping"].inputs[1].default_value[2] = 0
    # random rotation
    stem["Mapping"].inputs[2].default_value[0] = 0
    stem["Mapping"].inputs[2].default_value[1] = 0
    stem["Mapping"].inputs[2].default_value[2] = 0
    # random scalling
    stem["Mapping"].inputs[3].default_value[0] = 3.0
    stem["Mapping"].inputs[3].default_value[1] = 3.0
    stem["Mapping"].inputs[3].default_value[2] = 3.0
###########################################################################

# Randomize mapping for pbr (assume existing mapping node in stem and randomize it, stem is a node graph)


###########################################################################
def Randomize_RotateTranslate_PBR_MaterialMapping(mat):
    stem =  mat.nodes
    # Random translation
    stem["Mapping"].inputs[1].default_value[0] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[1] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[2] = random.uniform(0, 30)
    #if RotateMaterial: # Random rotation
    stem["Mapping"].inputs[2].default_value[0] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[1] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[2] = random.uniform(0, 6.28318530718)        
######################################################################################

# Translate and rotate randomly the PBR texture map on an object to increase variability

###########################################################################
def Randomize_RotateTranslate_TwoPBR_MaterialMapping(stem1,stem2,RotateMaterial):
    # Random translation
    mat1=stem1["Mapping"].inputs
    mat2=stem1["Mapping"].inputs
    mat1[1].default_value[0] = mat2[2].default_value[0] = random.uniform(0, 30)
    mat1[1].default_value[1] = mat2[2].default_value[0] = random.uniform(0, 30)
    mat1[1].default_value[2] = mat2[2].default_value[0] = random.uniform(0, 30)
    if RotateMaterial: # Random rotation
        mat1[2].default_value[0] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)
        mat1[2].default_value[1] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)
        mat1[2].default_value[2] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)  



#####################################################################################################

# load PBR material
        
########################################################################################################
def load_PBR_material(mat,PbrDir):
    stem = mat.nodes  # node where the material will be loaded
    print("Load material from ",PbrDir)


     
    for Fname in os.listdir(PbrDir):
       if ("olor." in Fname)  or ("COLOR." in Fname) or ("ao." in Fname)  or ("AO." in Fname):
          stem["Image Texture.001"].image=bpy.data.images.load(PbrDir+"/"+Fname)          
          print("Color "+ Fname)
       if ("oughness." in Fname) or ("ROUGH." in Fname) or ("roughness" in Fname) or ("ROUGHNESS" in Fname) or ("roughnness" in Fname):
          stem["Image Texture.002"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Roughness "+ Fname)
       if ("ormal." in Fname)  or ("NORM." in Fname) or ("normal" in Fname)  or ("NORMAL" in Fname) or ("Normal" in Fname):
          stem["Image Texture.003"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Normal "+ Fname)
       if ("eight." in Fname) or ("DISP." in Fname) or ("height" in Fname) or ("displacement" in Fname):
          stem["Image Texture"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Height "+ Fname)
       if ("etallic." in Fname) or ("etalness." in Fname)  or ("etal." in Fname) or ("etalic." in Fname) :
          stem["Image Texture.004"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Metallic "+ Fname)
       if ("pecular."  in Fname):
          stem["Image Texture.005"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Specular "+ Fname)
        
    Normalize_PBR_MaterialMapping(stem)
    return PbrDir
#####################################################################################################

# load random PBR material
        
########################################################################################################
def load_random_PBR_material(mat,materials_lst):
    stem = mat.nodes  # node where the material will be loaded
    rnd=np.random.randint(len(materials_lst)) # pick dataset
    print("Load a random material from the computer hard drive.")
    index = random.randint(0, len(materials_lst[rnd])-1 )
    PbrDir = materials_lst[rnd][index] # pick pbr

     
    for Fname in os.listdir(PbrDir):
       if ("olor." in Fname)  or ("COLOR." in Fname) or ("ao." in Fname)  or ("AO." in Fname):
          stem["Image Texture.001"].image=bpy.data.images.load(PbrDir+"/"+Fname)          
          print("Color "+ Fname)
       if ("oughness." in Fname) or ("ROUGH." in Fname) or ("roughness" in Fname) or ("ROUGHNESS" in Fname) or ("roughnness" in Fname):
          stem["Image Texture.002"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Roughness "+ Fname)
       if ("ormal." in Fname)  or ("NORM." in Fname) or ("normal" in Fname)  or ("NORMAL" in Fname) or ("Normal" in Fname):
          stem["Image Texture.003"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Normal "+ Fname)
       if ("eight." in Fname) or ("DISP." in Fname) or ("height" in Fname) or ("displacement" in Fname):
          stem["Image Texture"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Height "+ Fname)
       if ("etallic." in Fname) or ("etalness." in Fname)  or ("etal." in Fname) or ("etalic." in Fname) :
          stem["Image Texture.004"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Metallic "+ Fname)
       if ("pecular."  in Fname):
          stem["Image Texture.005"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Specular "+ Fname)
        
    Randomize_PBR_MaterialMapping(stem)
    return PbrDir





#*********************************
#******************************
#*********************************



#########################################################################################################################3

# Generate random BSDF material(stem is existing BSDF node)

########################################################################################################
 
def load_random_BSDF_material(stem):  
    print("Generate BSDF material")
    d,dv = map_name2indx()

           
        

# ----------------------------------Select random property for material --------------------------------------------------------------------------------------      
    #-----------Set random properties for material-----------------------------------------------------
    RGB=colorsys.hsv_to_rgb(np.random.rand(), np.random.rand(),np.random.rand()) # Create random HSV and convert to RGB (HSV have better distrobution)
 
    stem.inputs[d['Base Color']].default_value =  (RGB[0], RGB[1],RGB[2], 1)
  
    stem.inputs[d['Subsurface Weight']].default_value = 0
    if np.random.rand()<0.98:
      stem.inputs[d['Transmission Weight']].default_value = np.random.rand() # Transmission
    else:
      stem.inputs[d['Transmission Weight']].default_value = 1 #Transmission
    if np.random.rand()<0.90:
      stem.inputs[d['Roughness']].default_value = np.random.rand()# Roughness*
    else: 
      stem.inputs[d['Roughness']].default_value = 0# Roughness*


    if np.random.rand()<0.8:
      stem.inputs[d['Metallic']].default_value = np.random.rand() # metalic*
    elif np.random.rand()<0.5:
     stem.inputs[d['Metallic']].default_value =0# metalic*
    else:
      stem.inputs[d['Metallic']].default_value =1# metalic*
    stem.inputs[d["IOR"]].default_value = 1+np.random.rand()*2.5 #ior index of reflection for transparen objects  *#https://pixelandpoly.com/ior.html
    if np.random.rand()<0.12: # specular
      stem.inputs[d['Specular IOR Level']].default_value = np.random.rand()# specular
    elif np.random.rand()<0.6:
     stem.inputs[d['Specular IOR Level']].default_value =0.5# specular
    else:
      ior=stem.inputs[d["IOR"]].default_value# specular
      specular=((ior-1)/(ior+1))**2/0.08
      stem.inputs[d['Specular IOR Level']].default_value=specular
#      
#    if np.random.rand()<0.12: # specular tint
#       stem.inputs[d['Specular Tint']].default_value = (np.random.rand()# tint specular
#    else:
    stem.inputs[d['Specular Tint']].default_value =(1,1,1,1)# specular tint

    if np.random.rand()<0.4:
      stem.inputs[d['Anisotropic']].default_value = np.random.rand()# unisotropic*
    else:
       stem.inputs[d['Anisotropic']].default_value = 0# unisotropic*
    if np.random.rand()<0.4:
      stem.inputs[d['Anisotropic Rotation']].default_value = np.random.rand()# unisotropic rotation
    else: 
       stem.inputs[d['Anisotropic Rotation']].default_value = 0# unisotropic rotation
    if np.random.rand()<0.4:
      stem.inputs[d['Sheen Weight']].default_value = np.random.rand()# sheen
    else: 
       stem.inputs[d['Sheen Weight']].default_value = 0# sheen
    if np.random.rand()<0.6:
      stem.inputs[d['Sheen Tint']].default_value = (1, 1, 1, 1) # sheen tint
    else: 
       stem.inputs[d['Sheen Tint']].default_value = (np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand()) # sheen tint
    stem.inputs[d['Coat Weight']].default_value =np.random.rand()*0.03 #Clear Coat
    stem.inputs[d['Coat Roughness']].default_value = np.random.rand()*0.03 
 
  
   
    
#    
#    if np.random.rand()<0.2:
#      stem.inputs[18].default_value = np.random.rand()**2*0.4# transmission rouighness
#    else: 
#       stem.inputs[18].default_value = 0 # transmission rouighness
    
    if np.random.rand()<0.03: # Emission
      stem.inputs[d['Emission Color']].default_value = (np.random.rand(), np.random.rand(),np.random.rand(), 1)# Emission
      stem.inputs[d['Emission Strength']].default_value = (np.random.rand()**2)*100 # emission strengh
    else: 
      stem.inputs[d['Emission Color']].default_value = (0, 0,0, 1)## emmision color
      stem.inputs[d['Emission Strength']].default_value = 0# emision weight
    stem.inputs[d["Alpha"]].default_value=1

    return BSDFMaterialToDictionary(stem)
  
       




#########################################################################################################################3

# Generate random transparent BSDF material (stem is existing BSDF node)

########################################################################################################
def load_transparent_BSDF_material(stem):
    
    print("generate transparent material=========================================================")
    
    d,dv = map_name2indx()

#-----------Set random properties for material-----------------------------------------------------
    if np.random.rand()<0.25: # Color
          RGB=colorsys.hsv_to_rgb(np.random.rand(), np.random.rand(),np.random.rand()) # Create random HSV and convert to RGB (HSV have better distrobution)
          stem.inputs[d['Base Color']].default_value =  (RGB[0], RGB[1],RGB[2], 1)
    else:
        rnd=1-np.random.rand()*0.3
        stem.inputs[d['Base Color']].default_value = (rnd, rnd, rnd, rnd) # color
    # index of refraction
#    stem.inputs[d['subsurface']] = stem.inputs[0] # Subsurface
  

    if np.random.rand()<0.1: # Subsurface
        stem.inputs[d['Subsurface Weight']].default_value = np.random.rand()
    else:
        stem.inputs[d['Subsurface Weight']].default_value = 0
   
    if np.random.rand()<0.2: #Transmission
       stem.inputs[d['Transmission Weight']].default_value = 1-0.2*RandPow(4) # Transmission
    else:
       stem.inputs[d['Transmission Weight']].default_value = 1 #Transmission
       
       
    if np.random.rand()<0.2: # Roughnesss
       stem.inputs[d['Roughness']].default_value = 0.2*RandPow(3) # Roughness*
    else: 
       stem.inputs[d['Roughness']].default_value = 0# Roughness*
  
 
   
       
    if np.random.rand()<0.7:# ior index refraction
         stem.inputs[d["IOR"]].default_value = 0.7+np.random.rand()*2 #ior index of reflection for transparen objects   #ior index of reflection for transparen objects*  
    
    else:
        stem.inputs[d["IOR"]].default_value = 1.415+np.random.rand()*0.115 #ior index of reflection for transparen objects*  
    #https://pixelandpoly.com/ior.html

     

    if np.random.rand()<0.1: # Metalic
       stem.inputs[d['Metallic']].default_value = 0.15*RandPow(3)# metalic*
    else:
      stem.inputs[d['Metallic']].default_value =0# metalic*
      
      
    if np.random.rand()<0.12: # specular
       stem.inputs[d['Specular IOR Level']].default_value = np.random.rand()# specular
    elif np.random.rand()<0.6:
      stem.inputs[d['Specular IOR Level']].default_value =0.5# specular
    else:
      ior=stem.inputs[d['Specular IOR Level']].default_value# specular
      specular=((ior-1)/(ior+1))**2/0.08
      stem.inputs[d['Specular IOR Level']].default_value=specular
      

    stem.inputs[d['Specular Tint']].default_value =(1,1,1,1)# specular tint
  
    if np.random.rand()<0.12: # anisotropic
       stem.inputs[d['Anisotropic']].default_value = np.random.rand()# unisotropic*
    else:
      stem.inputs[d['Anisotropic']].default_value =0.0# unisotropic*
  
    if np.random.rand()<0.12: # anisotropic rotation
       stem.inputs[d['Anisotropic Rotation']].default_value = np.random.rand()# unisotropic rotation
    else:
      stem.inputs[d['Anisotropic Rotation']].default_value =0.0# unisotropic
    
#    if np.random.rand()<0.6: #Transmission Roughness
#         stem.inputs[18].default_value = 0.25*RandPow(4) # transmission rouighness
#    else:
#         stem.inputs[18].default_value = 0 # transmission rouighness
    
      
    if np.random.rand()<0.1: # Clear  coat
       stem.inputs[d['Coat Weight']].default_value = np.random.rand()*0.1
    else:
      stem.inputs[d['Coat Roughness']].default_value =0# 

    if np.random.rand()<0.1: # Clear  coat
       stem.inputs[d['Coat Weight']].default_value = np.random.rand()
    else:
      stem.inputs[d['Coat Weight']].default_value =0.03# 
    stem.inputs[d['Sheen Weight']].default_value = 0 # Sheen 
    stem.inputs[d['Sheen Tint']].default_value = (1, 1, 1, 1) # Sheen tint
    
  

    
    stem.inputs[d['Emission Color']].default_value = (1, 1, 1, 1) # Emission
    stem.inputs[d['Emission Strength']].default_value = 0 # Emission stength
    stem.inputs[d["Alpha"]].default_value = random.uniform(0.6,1) # alpha *


    return BSDFMaterialToDictionary(stem) # turn material propeties into dictionary (for saving)

#######################################################################################################

# Replace material on object, set material be the only material of object obj

##############################################################################################################3
def ReplaceMaterial(obj,material):  

#    # Pick method to wrap PBr around object
#        if random.random()<0.55: 
#               nm='Material_pbr_camera_cord'
#        elif random.random()<0.5:
#               nm='Material_pbr_generated_cord' 
#        else:
#               nm='Material_pbr_object_cord'
        if hasattr(obj,'uv_textures'):
            obj.data.uv_textures.clear() 
            uv_textures=obj.data.uv_textures
            while (len(uv_textures)>0):
                  uv_textures = obj.data.uv_textures
                  uv_textures.remove(uv_textures[0])
        
#        for i in range(len(obj.data.materials)):
#            obj.data.materials[i]=material
        obj.data.materials.clear()
       
        obj.data.materials.append(material)
     #   fdfd=sss

####################################################################################################

#   Change UV mapping (the way the material ovelayed on the object           

########################################################################################################
def ChangeUVmapping(mat,uvmode): # 
    #   'camera' 'generated' 'object'
    if uvmode == 'object':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[3],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'generated':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[0],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'camera':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[4],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'uv':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[2],mat.nodes["Mapping"].inputs[0])
####################################################################################################

#   Change material mode  (load random material into ma         

########################################################################################################
def ChangeMaterialMode(mat,mode, materials_lst): # Change the type of material by connecting bsdf, pbr, or value 0-255 node to the output node 
    #   'bsdf' 'pbr' 'black' 'white'
    matprop={} # material properties
    if mode == 'bsdf':
          if random.random()<0.65:
             matprop=load_random_BSDF_material(mat.nodes["Principled BSDF.001"])
          else:
             matprop=load_transparent_BSDF_material(mat.nodes["Principled BSDF.001"])
            
          mat.links.new(mat.nodes["Principled BSDF.001"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'pbr':
          matprop=load_random_PBR_material(mat,materials_lst)
          mat.links.new(mat.nodes["Principled BSDF"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'white':
           mat.nodes["Value"].outputs[0].default_value = 1
           mat.links.new(mat.nodes["Value"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'black':
           mat.nodes["Value"].outputs[0].default_value = 0
           mat.links.new(mat.nodes["Value"].outputs[0],mat.nodes["Group Output"].inputs[0])
    return matprop
 #    node_groups['NodeGroupPBR_Generated'].nodes["Texture Coordinate"].outputs[1], bpy.data.node_groups['NodeGroupPBR_Generated'].nodes["Mapping"].inputs[0])
####################################################################################################