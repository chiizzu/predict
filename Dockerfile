FROM python:3.12-alpine


WORKDIR /app

RUN apk update && \
    apk add --no-cache ca-certificates libffi-dev musl-dev  gcc gfortran openblas-dev


COPY requirement.txt .



RUN pip install --upgrade pip && \
    pip install --prefer-binary -r requirement.txt

COPY . .

ENV PYTHONUNBUFFERED=1


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


