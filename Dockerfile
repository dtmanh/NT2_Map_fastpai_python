FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
# FROM python:3.9

# # 
# WORKDIR /app

# # 
# COPY ./requirements.txt /app/requirements.txt

# # 
# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# # 
# COPY ./app /app/

# 
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

