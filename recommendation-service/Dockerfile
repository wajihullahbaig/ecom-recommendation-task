FROM python:3.11.8-slim

# Create pyuser
RUN groupadd --gid 1000 pyuser && useradd --uid 1000 --gid 1000 -m pyuser \
    && apt update && apt install -y sudo \
    && echo pyuser ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/pyuser && chmod 0440 /etc/sudoers.d/pyuser \
    && apt clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



USER pyuser
RUN mkdir /home/pyuser/recommendation-service
WORKDIR /home/pyuser/recommendation-service
COPY ./app .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
