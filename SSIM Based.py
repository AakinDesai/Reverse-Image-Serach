import glob
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

data_path = r'C:\Users\aakin\Desktop\vacation-image-search-engine\dataset'
input_path = r'C:\Users\aakin\Desktop\vacation-image-search-engine\queries\108100.png'
input_image = cv2.imread(input_path)
h1=input_image.shape[0]
w1=input_image.shape[1]
s=list()
i=0

for imagePath in glob.glob(data_path + "/*.png"):

    image = cv2.imread(imagePath)
    input_image = cv2.imread(input_path)
    r1 = image.copy()
    r1 = cv2.resize(image, (w1, h1))
    a = [(i,-1*ssim(input_image, r1, gradient=False, data_range=None, multichannel=True, gaussian_weights=False, full=False))]
    s.extend(a)
    i=i+1

s.sort(key=lambda x: x[1])
print(s)

top_images = s[:5]
img =[cv2.imread(file) for file in glob.glob(data_path + "/*.png")]
for index, distance in top_images:
        r=img[index]
        h=r.shape[0]
        w=r.shape[1]
        r1=np.zeros((h,w,3))
        r1[:,:,0]=r[:,:,2]
        r1[:, :, 1] = r[:, :, 1]
        r1[:, :, 2] = r[:, :, 0]
        Image.fromarray(np.asarray(r1, dtype=np.uint8)).show()