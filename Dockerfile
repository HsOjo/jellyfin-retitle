FROM alpine:edge

COPY *.py /
COPY requirements.txt /

ARG ALPINE_MIRROR
RUN if [ ${ALPINE_MIRROR} ]; then \
  sed -i "s/https:\/\/dl-cdn.alpinelinux.org/$(echo $ALPINE_MIRROR|sed 's/\//\\\//g')/g" /etc/apk/repositories; \
fi

RUN apk --no-cache add python3 && \
  python3 -m venv /venv

ARG PYPI_MIRROR
RUN if [ ${PYPI_MIRROR} ]; then \
  /venv/bin/pip3 config set global.index-url ${PYPI_MIRROR}; \
fi

RUN /venv/bin/pip3 install -r /requirements.txt

CMD ["/venv/bin/python3", "main.py"]
