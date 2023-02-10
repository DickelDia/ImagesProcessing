import cv2
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
import json

def preprocess(raw):
    image = cv2.resize(raw, (900, 600), interpolation = cv2.INTER_AREA)                                          
    image = image.reshape(image.shape[0]*image.shape[1], 3)
    return image

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        hex_color += ("{:02x}".format(int(i)))
    return hex_color

def analyze(img):
    clf = KMeans(n_clusters = 5)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]

    return hex_colors

def get_image(url):
    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def process_images(image_urls):
    results = []
    for url in image_urls:
        image = get_image(url)
        processed_image = preprocess(image)
        colors = analyze(processed_image)
        results.append({
            "url": url,
            "colors": colors
        })
    return results

def main(image_urls):
    results = process_images(image_urls)
    with open("results.json", "w") as f:
        f.write(json.dumps(results))

if __name__ == "__main__":
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        # ...
    ]
    main(image_urls)
   