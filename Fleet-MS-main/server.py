import uvicorn

if __name__ == "__main__":
    uvicorn.run("MyFMS.asgi:application", reload=True, port=7000)
