FROM ubuntu:14.04
MAINTAINER RajR

RUN apt-get -qqy update \
    && apt-get -qqy upgrade --allow-unauthenticated

RUN apt-get install -y --allow-unauthenticated \
    libgmp-dev \
    libffi-dev \
    libssl-dev \
    python \
    python-dev \
    python-gtk2 \
    python-pip \
    python-wxgtk2.8

RUN pip -qq install \
    PyCrypto \
    Twisted \
    gmpy \
    pam \
    pyasn1 \
    pydoctor \
    pyflakes \
    pyopenssl \
    pyserial \
    python-subunit \
    service_identity \
    soappy \
    sphinx \
    twisted-dev-tools \
    twistedchecker

RUN pip install \
    pyicloud

RUN adduser --system user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt-get clean \
    && apt-get purge -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apk/*

WORKDIR /data
ADD show_my_idevices.py show_my_idevices.py
RUN chmod +x show_my_idevices.py

EXPOSE 8000

USER user
CMD  /data/show_my_idevices.py

### TO RUN
## export ITUNES_UNAME='uname'
## export ITUNES_PASSWD='passwd'
## docker run --name show_my_idevices -itd  -p 8000:8000 -e ITUNES_UNAME -e ITUNES_PASSWD show_my_idevices
