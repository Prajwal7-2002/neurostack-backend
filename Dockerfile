FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port
EXPOSE 7860

# Run Django with gunicorn
CMD ["gunicorn", "copilot_backend.wsgi:application", "--bind", "0.0.0.0:7860"]
