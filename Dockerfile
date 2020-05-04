FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 setup.py sdist bdist_wheel
RUN pip install dist/*.whl

RUN git config --global user.email "goji-bot@goji"
RUN git config --global user.name "Goji Bot"

CMD [ "goji", "server" ]

