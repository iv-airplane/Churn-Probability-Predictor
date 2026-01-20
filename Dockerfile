# 1. Use a slim version of Python to keep the image small
FROM python:3.12-slim

# 2. Set up a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# 3. Set the working directory
WORKDIR /app

# 4. Copy requirements and install dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# 5. Copy all project files into the container
# This includes main.py, utilities.py, and the .joblib model
COPY --chown=user:user . .

# 6. Expose the specific port HF Spaces expects
EXPOSE 7860

# 7. Launch the app using Uvicorn
# We bind to 0.0.0.0 so the container can accept external traffic
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]