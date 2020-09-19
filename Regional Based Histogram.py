import glob
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def imagedesprictor(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    describe= []
    height = image.shape[0]
    width=image.shape[1]
    centerx = int(width * 0.5)
    centery = int(height * 0.5)
    parts = [(0, centerx, 0, centery), (centerx, width, 0, centery), (centerx, width, centery, height),(0, centerx, centery, height)]
    centerMask = np.zeros(image.shape[:2], dtype="uint8")
    sx=int(centerx/2)
    sy = int(centery / 2)
    ex = int(width-(centerx / 2))
    ey = int(height-(centery / 2))
    cv2.rectangle(centerMask, (sx, sy), (ex, ey), 255, -1)

    for (sX, eX, sY, eY) in parts:
        rectangleMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(rectangleMask, (sX, sY), (eX, eY), 255, -1)
        rectangleMask = cv2.subtract(rectangleMask, centerMask)
        histogram = cv2.calcHist([image], [0, 1, 2], rectangleMask, bins,[0, 180, 0, 256, 0, 256])
        histogram = cv2.normalize(histogram, histogram).flatten()
        describe.extend(histogram)

    histogram = cv2.calcHist([image], [0, 1, 2], centerMask, bins, [0, 180, 0, 256, 0, 256])
    histogram = cv2.normalize(histogram, histogram).flatten()
    describe.extend(histogram)

    return describe

bins = (8, 12, 3)

def Cdistance(histogramA, histogramB, eps=1e-10):

    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histogramA, histogramB)])
    return d

if __name__ == '__main__':

    all_describe = list()
    data_path = r'C:\Users\aakin\Desktop\vacation-image-search-engine\dataset'
    input_path = r'C:\Users\aakin\Desktop\vacation-image-search-engine\queries\103300.png'

    for imagePath in glob.glob(data_path + "/*.png"):

        image = cv2.imread(imagePath)
        describe = imagedesprictor(image)
        all_describe.append(describe)

    input_image = cv2.imread(input_path)
    input_describe = imagedesprictor(input_image)
    h1 = input_image.shape[0]
    w1 = input_image.shape[1]
    immg = np.zeros((h1,w1,3))
    immg[:, :, 0] = input_image[:, :, 2]
    immg[:, :, 1] = input_image[:, :, 1]
    immg[:, :, 2] = input_image[:, :, 0]
    Image.fromarray(np.asarray(immg, dtype=np.uint8)).show()

    distances = [(index, Cdistance(input_describe,describe)) for index, describe in enumerate(all_describe)]
    distances.sort(key=lambda x: x[1])


    top_images = distances[:5]
    img = [cv2.imread(file) for file in glob.glob(data_path + "/*.png")]
    for index, distance in top_images:
        r=img[index]
        r1 = r.copy()
        r1 = cv2.resize(r1, (w1, h1))
        a = ssim(input_image, r1, gradient=False, data_range=None, multichannel=True, gaussian_weights=False,full=False)
        h=r.shape[0]
        w=r.shape[1]
        r1=np.zeros((h,w,3))
        r1[:,:,0]=r[:,:,2]
        r1[:, :, 1] = r[:, :, 1]
        r1[:, :, 2] = r[:, :, 0]
        Image.fromarray(np.asarray(r1, dtype=np.uint8)).show()
		