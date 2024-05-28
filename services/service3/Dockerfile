# service3/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY service3.py .
RUN pip install flask requests
CMD ["python", "service3.py"]
