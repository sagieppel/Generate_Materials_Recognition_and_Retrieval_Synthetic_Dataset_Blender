
import json
import objaverse
import objaverse.xl as oxl
objaverse.__version__
uids = objaverse.load_uids()

#objaverse.load_objects(uids,download_path="/media/deadcrow/6TB/Datasets/all/") # all
lvis_annotations = objaverse.load_lvis_annotations()
for cat in lvis_annotations.keys():
       objaverse.load_objects(lvis_annotations[cat][0:200],download_path="/media/deadcrow/6TB/Datasets/ObjaverseV1/"+cat+"/")
# Writing the dictionary to a JSON file
# with open("/media/deadcrow/6TB/Datasets/ObjaverseV1/annotations.json", 'w') as json_file:
#     json.dump(lvis_annotations, json_file, indent=4)
# objaverse.load_objects(uids,download_path="/media/deadcrow/6TB/Datasets/ObjaverseV1/")
# print(len(uids))
#annotations = objaverse.load_annotations(uids[:10])
#objaverse.load_objects(uids[1:10],download_path="/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Datasets/ObjaverseV1/")
#
# annotations = oxl.get_annotations(
#     download_dir="/media/deadcrow/6TB/Datasets/ObjaverseV1/Downloads/" # default download directory
# )
# ann=annotations[1:10]#[annotations["license"] == "MIT License"]
# #obj = mit[mit["fileType"] == 'obj']
# stl = ann[ann["fileType"] == 'stl']
#
#
#
#
# print(annotations["source"].value_counts())
# print(annotations["fileType"].value_counts())
#
#
# #obj = mit[mit["fileType"] == 'obj']
# oxl.download_objects(annotations.sample(2))#,"/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Data_zoo/objverse/")
# selected = []
# # for i in range(annotations['source'].__len__()):
# #     if annotations["license"][i] == "MIT License":
# #         if annotations["fileType"][i]  == 'obj' or annotations["fileType"][i]  == 'stl':
# #              selected.append(i)
# #         print(len(selected))
# oxl.download_objects(annotations.sample(5),"/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Data_zoo/objverse2/")
# x=3
#
#
# #'fileIdentifier', 'source', 'license', 'fileType', 'sha256'
#