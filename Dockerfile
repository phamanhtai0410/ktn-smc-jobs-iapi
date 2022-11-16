FROM 968557029040.dkr.ecr.ap-southeast-1.amazonaws.com/esollabs/cicd:sh-python-ba4ec63-dirty

COPY . /webapps
WORKDIR /webapps

RUN apk update && apk add --no-cache  tzdata git make  build-base supervisor

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/* /subprocess/* /logs/*

RUN pip --no-cache-dir install --upgrade pip setuptools wheel
RUN pip --no-cache-dir install -r ./lib/requirements.txt
RUN pip --no-cache-dir install -r ./requirements.txt
COPY conf/supervisor/ /etc/supervisor.d/

RUN mkdir -p /subprocess
RUN mkdir -p /logs