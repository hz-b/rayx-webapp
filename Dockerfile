FROM python:3.13

WORKDIR /app

COPY pyproject.toml .

# Does not use the Lock-File
RUN pip install -e . 

COPY . .

EXPOSE 5000

CMD ["flask", "-A", "app.py", "run", "-h", "0.0.0.0", "-p", "5000"]
