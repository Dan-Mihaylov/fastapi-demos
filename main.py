import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return {'message': 'Hello World'}


@app.get('/hello/{name}')
async def greeting(name: str):
    message = f'Hello {name}!'
    return {'message': message}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
