import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app",
        host='localhost',
        port=8000,
        log_level="debug",
        reload=True,
        proxy_headers=True
    )
