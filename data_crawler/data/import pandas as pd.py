import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# Đọc dữ liệu từ tệp CSV vào DataFrame
data = pd.read_csv('data_crawler/data/newproducts.csv',header=None)

# Tạo thư mục để lưu trữ hình ảnh tải về (tuỳ chọn)
import os
if not os.path.exists('data_crawler/data/images'):
    os.makedirs('data_crawler/data/images')

# Lặp qua từng hàng của DataFrame và tải xuống hình ảnh
for index, row in data.iterrows():
    image_url = 'http://' + row[0]  # Thêm schema 'http://' vào đầu URL
    response = requests.get(image_url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(f'data_crawler/data/images/image_{index}.jpg')  # Lưu hình ảnh với tên duy nhất (có thể dựa trên index)
    else:
        print(f"Không thể tải hình ảnh từ URL: {image_url}")