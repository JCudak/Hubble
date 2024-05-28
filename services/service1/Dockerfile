# service1/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY service1.py .
RUN pip install flask pymongo
CMD ["python", "service1.py"]
