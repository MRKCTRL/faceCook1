FROM python:3.10-slim AS development

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

COPY requirments.txt . 

RUN pip install --no-cache-dir -r requirements.txt 

COPY package*.json ./
RUN npm install 

COPY . . 

RUN npm run build:css 

ENV FLASK_APP=run.py 
ENV FLASK_ENV=development



EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

FROM python:3.10-slim AS production

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from development stage
COPY --from=development /app .

# Set environment variables for production
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose port for Gunicorn
EXPOSE 8000

# Command to run Gunicorn for production
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "run:app"]