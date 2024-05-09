FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip3 install requests
COPY get_node_metrics.py .

CMD ["python3", "get_node_metrics.py"]
