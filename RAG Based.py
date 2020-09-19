import glob
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage import data, segmentation
from skimage.future import graph
from scipy.spatial.distance import directed_hausdorff
import cv2

def imagedesprictor(image):

    labels = segmentation.slic(image, compactness=30, n_segments=400)
    g = graph.rag_mean_color(image, labels)
    u1 = g.edges()
    a = 0

    for x, y in u1:
        u = g.get_edge_data(x, y)
        a = a + u['weight']

    max1 = max(y for x, y in u1)
    max2 = max(x for x, y in u1)
    max3 = max(max1, max2)
    b1 = np.zeros((max3 + 1))
    l = len(u1)

    for i in range(max3 + 1):
        b = 0
        Ai = g.edges(i)
        for x, y in Ai:
            u = g.get_edge_data(x, y)
            b = b + u['weight']
        b1[i] = b / a

    array1 = np.zeros((l, 2))
    i = 0
    for x, y in u1:
        array1[i, 0] = b1[x]
        array1[i, 1] = b1[y]
        i = i + 1

    return array1

def Cdistance(array1, array2):

    t = directed_hausdorff(array1, array2)[0] * 1000
    t1 = directed_hausdorff(array2, array1)[0] * 1000
    return max(t,t1)

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

    distances = [(index, Cdistance(input_describe,describe)) for index, describe in enumerate(all_describe)]
    distances.sort(key=lambda x: x[1])

    top_images = distances[:5]
    img = [cv2.imread(file) for file in glob.glob(data_path + "/*.png")]
    for index, distance in top_images:
        r=img[index]
        r1 = r.copy()
        r1 = cv2.resize(r1, (w1, h1))
        a = ssim(input_image, r1, gradient=False, data_range=None, multichannel=True, gaussian_weights=False,full=False)
        print(a)
        h=r.shape[0]
        w=r.shape[1]
        r1=np.zeros((h,w,3))
        r1[:,:,0]=r[:,:,2]
        r1[:, :, 1] = r[:, :, 1]
        r1[:, :, 2] = r[:, :, 0]
        Image.fromarray(np.asarray(r1, dtype=np.uint8)).show()