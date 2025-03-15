FROM python:3.9-slim-buster

# Update package sources with mirror and install essential build tools
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages first for better layer caching
COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    uwsgi uwsgi-tools && \
    python3 -m pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8086

CMD ["uwsgi", "--ini", "uwsgi.ini"]