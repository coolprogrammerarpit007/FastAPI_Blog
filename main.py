from fastapi import FastAPI,Request,HTTPException,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


# Check Application Health
@app.get("/")

def get_root():
    return {"msg":"Application working successfully!"}


# Route to return list of posts/dictionary





# Return HTML Response / Title of post in h1 Heading

# @app.get("/posts-title",response_class=HTMLResponse,include_in_schema=False)

# ***************** WEB/BROWSER Routes **********************************
@app.get("/home",include_in_schema=False,name="home")

def home(request:Request):
    # return f"<h1>{posts[0]['title']}</h1>"
    return templates.TemplateResponse(request,"home.html",{"posts":posts,"title":"HOME"})

@app.get("/posts/{post_id}",include_in_schema=False)
def post_page(request:Request,post_id:int):
    for post in posts:
        title = post["title"][:50]
        if post.get("id") == post_id:
            return templates.TemplateResponse(request,"post.html",{"post":post,"title":title})
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Post Not Found!")




# ********************** API Routes ******************************

# API TO GET ALL THE POSTS
@app.get("/api/posts")
def get_posts():
    return posts


# API TO GET SINGLE POST
@app.get("/api/posts/{post_id}")
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return {"Post":post}
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Post Not Found!")


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )