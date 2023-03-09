# include .env
# export

run:
	streamlit run streamlit_app.py --server.port 8501 --server.headless true --server.address=0.0.0.0
build:
	docker build -t streamlit-app .
run_docker: # make streamlit work with github codespace
	docker run -e OPENAI_API_KEY=${OPENAI_API_KEY} -p 8501:8501 streamlit-app --server.enableXsrfProtection false --server.enableCORS false