from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database_backend import search, add  # Imported database functions

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"message": "Hello from FastAPI!"})

@app.post("/shorten", response_class=HTMLResponse)
async def shorten_page(request: Request):
    return templates.TemplateResponse(request, "shorten.html", {"message": "Shorten Link"})

@app.post("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse(request, "search.html", {"message": "Search Links"})

@app.post("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse(request, "success.html", {"message": "Success!"})

# Fixed function name to prevent infinite recursion
@app.post("/backend-search")
async def backend_search(link: str = Form(...)):
    data = search(link)  # Calls the imported database search function
    
    if not data:
        raise HTTPException(status_code=404, detail="Code or URL not found in database.")
    
    url_value = data["url"] 
    return RedirectResponse(url=url_value, status_code=302)

@app.post("/backend_shorten")
async def shorten(code: str = Form(...), link: str = Form(...)):
    add(code, link)
    return RedirectResponse(url="/success", status_code=303)