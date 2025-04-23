FROM python:3.12-slim-bookworm AS build

WORKDIR /app
COPY requirement.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libopenblas-dev \
    gfortran \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirement.txt

# Stage final
FROM python:3.12-slim-bookworm

WORKDIR /app
COPY --from=build /app /app
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
