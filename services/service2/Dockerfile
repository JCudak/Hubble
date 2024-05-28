# service2/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY service2.py .
RUN pip install flask requests
CMD ["python", "service2.py"]
