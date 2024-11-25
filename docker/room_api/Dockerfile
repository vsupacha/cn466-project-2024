FROM python:3.11

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 80
CMD ["flask", "--app", "app", "--debug", "run", "--host=0.0.0.0", "--port=5002"]