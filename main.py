from fastapi import FastAPI, Request
from validate import Validation
from utils import validation, save_json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.post("/update_validation")
def update_validation(v: Validation):
    global validation

    validation = v
    save_json(validation.model_dump(mode="json"), "validation.json")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", context={"validation": validation})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
