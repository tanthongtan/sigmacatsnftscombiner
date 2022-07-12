from PIL import Image
import os
import re
import numpy as np
import hashlib as h
import json

size = (2048,2048)
layers = ["Background", "Item", "Body", "Eyes", "Shirt", "Earrings", "Head", "Mouth"]
collection_size = 2000

#generate probabilities
layer_probabilities = []
layer_files = []
for layer in layers:
    weights = []
    files = []
    for filename in os.listdir(os.path.join("layers",layer)):
        weight=re.search("#(\d+)|$", filename).group(1)
        if weight:
            weights.append(float(weight))
        else:
            weights.append(1.0)
        files.append(filename)
    weights_sum = sum(weights)
    layer_probabilities.append([weight/weights_sum for weight in weights])
    layer_files.append(files)

#generate images
dna_set = set()
id=1
while id <= collection_size:
    metadata = {
        "name": f"Sigma Cat #{id}",
        "description": "Sigma Cats: To Spark Greatness in Every Sigma",
        "image": "To be declared",
        "attributes": []
        }
    
    dna = ""
    for i,layer in enumerate(layers):        
        current_path = os.path.join("layers",layer)
        filename = np.random.choice(layer_files[i],p=layer_probabilities[i])
        dna+=filename
        new_img = Image.open(os.path.join(current_path, filename)) 
        new_img = new_img.resize(size,Image.ANTIALIAS)
        
        if len(re.findall("Blank#|Blank |Blank\.|blank#|blank |blank\.|none#|none |none\.|None#|None |None\.",filename))==0:
            metadata['attributes'].append({'trait_type':layer,'value':re.search("^[^#|.]+",filename).group().strip()})
        
        if i == 0:
            current_img = new_img
        else:
            current_img.paste(new_img, (0,0), mask = new_img)
            
    dna = h.sha256(dna.encode("utf8")).hexdigest()
    if dna in dna_set:
        print("Duplicate dna!", dna)
    else:
        dna_set.add(dna)
        image_filename = os.path.join("images",str(id)+".png")
        os.makedirs(os.path.dirname(image_filename), exist_ok=True)
        current_img.save(image_filename,optimize=True)
        
        metadata_filename = os.path.join("metadata",f"{id}")
        os.makedirs(os.path.dirname(metadata_filename), exist_ok=True)
        with open(metadata_filename, "w") as file:
            json.dump(metadata, file)
        id+=1
            
            