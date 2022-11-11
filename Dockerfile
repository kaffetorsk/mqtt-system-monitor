FROM python

# Unbuffered logging
ENV PYTHONUNBUFFERED=TRUE

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY *.py ./

ENTRYPOINT ["python", "main.py"]
