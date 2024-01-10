import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def draw_delaunay_countour(img_path, output_path):
    img = cv2.imread(img_path)
    assert img is not None, "Image not found"
    height, width = img.shape[:2]

    # グレースケール画像に変換し、しきい値処理を行う
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 輪郭を見つける
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 輪郭上の点を取得する
    points = []
    for contour in contours:
        for point in contour:
            points.append(point[0])
    points = np.array(points)

    # 取得する点の数を入力させる
    print("輪郭上の点の数:", len(points))
    num_points = input("輪郭上の点の数以下で 点の数を入力してください（未入力の場合はすべての点を利用します）: ")

    if num_points == "":
        num_points = len(points)
    else:
        num_points = int(num_points)

    # 必要な点の数だけランダムサンプリング
    if len(points) > num_points:
        np.random.shuffle(points)
        points = points[:num_points]

    # 画像の四隅の点を追加
    points = np.append(points, [[0, 0], [width-1, 0], [0, height-1], [width-1, height-1]], axis=0)

    # 輪郭上の点を描画
    # for point in points:
    #     cv2.circle(img, tuple(point), 3, (0, 0, 255), -1)

    # Delaunay三角形分割
    tri = Delaunay(points)

    # 分割結果を画像に描画
    for triangle in points[tri.simplices]:
        # 三角形の重心の画素値を取得
        centroid = np.mean(triangle, axis=0)
        r, g, b = img[int(centroid[1]), int(centroid[0])]

        # 分割領域内を重心の画素値の色に
        cv2.fillPoly(img, [triangle], (int(r), int(g), int(b)))

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    cv2.imwrite(output_path, img)

if __name__ == "__main__":
    draw_delaunay_countour('./delaunay_img/img/bird.jpg', './delaunay_img/img/bird_contour_2000.png')