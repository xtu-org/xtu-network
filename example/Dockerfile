FROM python:3.12-alpine

RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

RUN apk add ca-certificates

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
    && apk add --update --no-cache python3 py3-pip \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip config set global.index-url https://pypi.proxy.yangrucheng.top/simple \
    && pip config set global.trusted-host pypi.proxy.yangrucheng.top \
    && pip install --upgrade pip --break-system-packages \
    && pip install --user -r requirements.txt --break-system-packages

COPY . /app

CMD ["python3", "app.py"]