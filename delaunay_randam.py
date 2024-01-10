import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def create_random_points(img_path, output_path, num_points):
    img = cv2.imread(img_path)
    assert img is not None, "Image not found"
    height, width = img.shape[:2]

    # ランダムな点を生成
    random_points = np.random.randint(0, width, size=(num_points, 2))
    # 画像の範囲内に収まるように調整
    random_points = np.clip(random_points, 0, [width-1, height-1])

    # 画像の四隅の点を追加
    random_points = np.append(random_points, [[0, 0], [width-1, 0], [0, height-1], [width-1, height-1]], axis=0)

    # Delaunay三角形分割
    tri = Delaunay(random_points)

    # 分割結果を画像に描画
    for triangle in random_points[tri.simplices]:
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
    create_random_points('./delaunay_img/img/lena.png', './delaunay_img/img/lena_5000.png', 5000)
