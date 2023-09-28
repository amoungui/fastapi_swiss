FROM  python:3.11.4
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
