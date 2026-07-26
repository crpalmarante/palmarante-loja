import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.procurement.core.infrastructure.api.procurement_api import router

app = FastAPI(title='BusinessCore — Procurement Platform', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

for route in router.routes:
    app.routes.append(route)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8011)
