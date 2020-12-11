# Bài tập lớn Nhập môn Trí tuệ nhân tạo

## Đề tài  
Điều khiển trò chơi Rắn săn mồi bằng nhận diện cử chỉ bàn tay

## Mục lục
[1. Cài đặt](#1-Cài-đặt)  
[2. Chạy chương trình](#2-Chạy-chương-trình)  
[3. Điều khiển](#3-Điều-khiển)  


## 1. Cài đặt
### 1.1. Phiên bản Python  
``` 3.8.2```

### 1.2. Cài đặt thư viện
Có thể cài trực tiếp vào global environment hoặc dùng virtual environment.  
Với VS Code xem thêm hướng dẫn ở [đây](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages).    
Tiến hành cài đặt: 
- Cài các thư viện trong requirements.txt: 
```bash
pip install -r requirements.txt
```
- Lỗi liên quan đến ```tf.gfile.GFile```:   
Tìm và sửa file ```label_map_util.py``` (đường dẫn có trong thông báo lỗi): sửa ```tf.gfile.GFile``` thành ```tf.io.gfile.GFile```


Hoặc tải trực tiếp folder ```.venv``` tại [đây](https://drive.google.com/file/d/1ruM0_h4wbADF-029CosUpzho6rvf8Vq3/view?usp=sharing)
- Thêm vào project  
- Dùng virtual environment (hướng dẫn bên dưới dành cho VS Code)  
```bash
.venv\scripts\activate
```
- Chọn new environment:   
Mở Command Palette (Ctrl + Shift + P): Tìm chọn ```Python: Select Interpreter```, chọn ```.venv``` 

## 2. Chạy chương trình:  
Chạy file ```SnakeGame.py```  
Để vào game => Nhấn phím a  
Để thoát game/camera => Nhấn phím q  

## 3. Điều khiển:

Điều khiển đi lên - UP

![up](/screenshot/up.png)

Điều khiển đi xuống - DOWN

![down](/screenshot/down.png)

Điều khiển sang trái - LEFT

![left](/screenshot/left.png)

Điều khiển sang phải - DOWN
 
![right](/screenshot/right.png)
