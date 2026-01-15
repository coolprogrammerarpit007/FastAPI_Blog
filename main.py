from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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


@app.get("/posts")

def get_posts():
    return posts


# Return HTML Response / Title of post in h1 Heading

@app.get("/posts-title",response_class=HTMLResponse,include_in_schema=False)

def post_heading():
    return f"<h1>{posts[0]['title']}</h1>"