FROM python:3.12-slim AS build-stage

WORKDIR /app
COPY requirement.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libopenblas-dev \
    gfortran

RUN pip install --upgrade pip && \
    pip install --prefer-binary -r requirement.txt


FROM python:3.12-alpine

WORKDIR /app
COPY --from=build-stage /app /app


COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

