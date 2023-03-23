import uvicorn

host = "0.0.0.0"
port = 8000
app_name = "app:app"

if __name__ == '__main__':
	uvicorn.run(app_name, host=host, port=port, workers=10)
