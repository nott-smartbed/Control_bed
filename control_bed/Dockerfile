FROM python:3.10-slim

# Cài đặt các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    python3-rpi.gpio \
    && apt-get clean
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    python3-dev \
    python3-rpi.gpio \
    && apt-get clean

RUN pip install lgpio

# Cài đặt thư viện Python
#RUN pip install lgpio
#RUN pip install flask gpiozero
RUN pip install pyserial
# Copy mã nguồn
WORKDIR /app
COPY run.py .

# Chạy ứng dụng
CMD ["python3", "run.py"]