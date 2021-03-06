import face_recognition as fr
import numpy as np
from PIL import Image
from matplotlib import pyplot


def image_to_array(im):
    return np.array(im)


def array_to_image(array):
    return Image.fromarray(array)


def get_key_points_from_landmarks(landmarks):
    chin = landmarks["chin"]
    nose_bridge = landmarks["nose_bridge"]
    left_eyebrow = landmarks["left_eyebrow"]
    right_eyebrow = landmarks["right_eyebrow"]
    center = nose_bridge[3]
    key_points = (
            list(chin[i] for i in [0, 4, 6, 8, 10, 12, 16])
            + list(right_eyebrow[i] for i in [4, 2, 0])
            + list(left_eyebrow[i] for i in [4, 2, 0])
    )
    return np.array(center), [np.array(kp) for kp in key_points]


def get_triangles(center, orbits):
    return [
        [center, orbit1, orbit2] for orbit1, orbit2 in zip(orbits, orbits[1:] + [orbits[0]])
    ]
    


file_name = "obama_trump2.jpg"

if __name__ == "__main__":
    im = Image.open(file_name)
    face_landmarks = fr.face_landmarks(fr.load_image_file(file_name))[1]
    center, key_points = get_key_points_from_landmarks(face_landmarks)
    triangles = get_triangles(center, key_points)

    ar = image_to_array(im)
    pyplot.imshow(ar)
    for triangle in triangles:
        for p1, p2 in zip(triangle, triangle[1:] + [triangle[0]]):
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
            pyplot.plot(np.linspace(x1, x2, endpoint=True), np.linspace(y1, y2, endpoint=True))
    pyplot.show()

