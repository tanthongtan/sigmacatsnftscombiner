import subprocess
import os
from PIL import Image
import re

for layer in os.listdir("layers"):
    for filename in os.listdir(f"layers/{layer}"):
        oldfilename = f"layers/{layer}/{filename}"
        
        temp_filename = re.search("^[^#|.]+",filename).group().strip()
        temp_filename = temp_filename + ".png"
        newfilename = f"layers_web/{layer}/{temp_filename}"
        new_img = Image.open(oldfilename) 
        new_img = new_img.resize((600,600),Image.ANTIALIAS)
        os.makedirs(os.path.dirname(newfilename), exist_ok=True)
        new_img.save(newfilename,optimize=True)
        subprocess.call(f"pngquant.exe --speed 1 --strip \"{newfilename}\" -o \"{newfilename}\" --force", shell=True)