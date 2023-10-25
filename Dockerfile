FROM python

ENV PYTHONDONTWRITEDBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /Books
