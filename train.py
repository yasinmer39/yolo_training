import os
import cv2

# 📌 Klasör yolları
image_dir = './valid/images'
label_dir = './valid/labels'
class_file = './classes.txt'  # Eğer sınıf isimleri varsa

# 🎨 Renkler ve font
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
font = cv2.FONT_HERSHEY_SIMPLEX

# 📖 Sınıf adları (isteğe bağlı)
class_names = []
if os.path.exists(class_file):
    with open(class_file, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]

# 🔁 Tüm görüntüleri işle
for filename in os.listdir(image_dir):
    if not filename.endswith(('.jpg', '.png', '.jpeg')):
        continue

    image_path = os.path.join(image_dir, filename)
    label_path = os.path.join(label_dir, os.path.splitext(filename)[0] + '.txt')

    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                class_id = int(parts[0])
                print(list(map(float, parts[1:])))
                x_center, y_center, box_width, box_height = map(float, parts[1:])

                # Koordinatları gerçek piksellere dönüştür
                x1 = int((x_center - box_width / 2) * w)
                y1 = int((y_center - box_height / 2) * h)
                x2 = int((x_center + box_width / 2) * w)
                y2 = int((y_center + box_height / 2) * h)

                color = colors[class_id % len(colors)]
                label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, label, (x1, y1 - 10), font, 0.5, color, 2)

    cv2.imshow('Labeled Image', img)
    key = cv2.waitKey(0)
    if key == 27:  # ESC ile çık
        break

cv2.destroyAllWindows()
