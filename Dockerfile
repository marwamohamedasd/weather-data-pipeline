# اختيار نسخة بايثون
FROM python:3.11-slim

# تحديد مكان العمل
WORKDIR /app

# تسطيب المكتبات الضرورية
#RUN pip install pandas sqlalchemy psycopg2-binary requests-cache openmeteo-requests retry-requests

# RUN pip install pandas sqlalchemy psycopg2-binary requests-cache openmeteo-requests retry-requests python-dotenv
RUN pip install --default-timeout=1000 pandas sqlalchemy psycopg2-binary requests-cache openmeteo-requests retry-requests python-dotenv

# نسخ ملف الكود بتاعنا للصندوق
# COPY main.py .
COPY . .

# تشغيل الكود
CMD ["python", "main.py"]