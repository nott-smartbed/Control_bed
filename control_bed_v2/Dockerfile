# Dùng hình ảnh Python làm nền
FROM python:3.10.12-slim

# Cài đặt thư viện OpenCV và các thư viện cần thiết khác
# Cài đặt các công cụ cần thiết cho việc biên dịch và xử lý GPIO
RUN apt update && apt install -y \
    python3-dev

# RUN pip install --no-cache-dir homeassistant
RUN pip install requests

# Sao chép script Python vào container
COPY run.py /run.py

# Khởi chạy script khi container chạy
CMD ["python", "run.py"]
