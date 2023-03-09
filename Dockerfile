FROM python:3.9-slim

WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt

ADD streamlit_app.py /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]