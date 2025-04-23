FROM python:3.12-alpine

WORKDIR /app

# Install build tools dan dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openblas-dev \
    gfortran \
    musl-dev \
    linux-headers \
    jpeg-dev \
    zlib-dev

# Install python packages
COPY requirement.txt .
RUN pip install --upgrade pip && \
    pip install --prefer-binary -r requirement.txt

# Copy project files
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
