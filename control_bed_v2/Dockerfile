FROM python:3.10.12-slim

# Cài đặt các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    python3-rpi.gpio \
    python3-dev \
    && apt-get clean

RUN pip install requests
RUN pip install pyserial

COPY run.py /run.py

CMD ["python", "run.py"]
