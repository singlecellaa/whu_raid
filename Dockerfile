FROM python:3.9-buster

# Update package sources and install vim
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y vim

WORKDIR /etc/uwsgi/whu_raid_django

# Install Python packages
RUN python3 -m pip install uwsgi uwsgi-tools -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# Add application files
ADD . /etc/uwsgi/whu_raid_django

EXPOSE 8086

CMD ["uwsgi", "--ini", "/etc/uwsgi/whu_raid_django/uwsgi.ini"]
