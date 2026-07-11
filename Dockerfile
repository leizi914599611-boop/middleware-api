FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY middleware.py .
EXPOSE 5000
CMD ["python", "middleware.py"]
