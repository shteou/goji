FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update
RUN apt install -y git
RUN apt clean

COPY goji goji
COPY setup.py .
COPY README.md .

RUN python3 setup.py sdist bdist_wheel
RUN pip install dist/*.whl

RUN rm -Rf /usr/src/app

RUN groupadd -g 999 goji && \
    useradd -mr -u 999 -g goji goji
USER goji
WORKDIR /home/goji

COPY askpass.py .

RUN git config --global user.email "goji-bot@goji"
RUN git config --global user.name "Goji Bot"

CMD [ "goji", "server" ]

