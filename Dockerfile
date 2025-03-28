# Base image with Python and necessary dependencies
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install and configure Spark
ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=3

RUN wget -qO - https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar xz -C /opt
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH="${SPARK_HOME}/bin:${PATH}"

# Define environment variables for Kafka & Elasticsearch
ENV KAFKA_BROKER="kafka:9092"
ENV ELASTICSEARCH_HOST="http://elasticsearch:9200"

# Expose necessary ports
EXPOSE 9092 9200 3000 4040

# Start processing pipeline
CMD ["python", "spark_streaming.py"]
