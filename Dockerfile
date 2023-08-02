FROM alpine:edge

COPY *.py /
COPY requirements.txt /

RUN apk --no-cache add python3 && \
  python3 -m venv /venv && \
  /venv/bin/pip3 install -r /requirements.txt

CMD ["/venv/bin/python3", "main.py"]
