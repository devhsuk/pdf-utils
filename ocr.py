import os, requests, cv2, numpy as np
from PIL import Image, ImageOps

def cvt_image(image, size=(224, 224)):
    image = Image.fromarray(image)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image = np.asarray(image)
    return image

def morph(image):
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    morph = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, np.ones((5,4), np.uint8))
    thr   = cv2.adaptiveThreshold(morph, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 30)
    morph2= cv2.morphologyEx(thr, cv2.MORPH_CLOSE, np.ones((10,55)))
    return { "morph": morph, "morph2": morph2 }

def extract_images_fom_pdf():
    pass


KEY = [ r"2cfb2e9e5edb8798a89c6d44fb0ecfc1", r"2cfb2e9e5edb8798a89c6d44fb0ecfc1" ][0]
HEADERS = { "Authorization" : f"KakaoAK {KEY}" }
API_URL = r"https://dapi.kakao.com/v2/vision/text/ocr"

if __name__=="__main__":
    file_names = os.listdir(r"./data/") 
    print(len(file_names))

    for file_name in file_names:
        
        if file_name[-4:] == ".txt":  continue
        print(file_name)

        image = cv2.imread(f"./data/{file_name}")
        assert image is not None, "file read error"

        image = cvt_image(image)
        # res = morph(image) # morph
        jpeg_image = cv2.imencode(".jpg", image)[1]
        # jpeg_image = cv2.imencode(".jpg", image)[1]
        data = jpeg_image.tobytes()

        ocr_json = requests.post(API_URL, headers=HEADERS, files={"image": data})
        result = ocr_json.json()["result"]

        for box in result:
            words = box["recognition_words"]
            # points = box["boxes"]
            # left top left bottom right bottom right top
        words = ','.join([ box["recognition_words"][0] for box in result ])
        print(words)

        with open(f"./output2/{file_name[:-4]}.txt", 'w') as f:
            f.write(words)
        print(f"{'='*10}")