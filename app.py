"""
app.py — Main Flask application
Reads markdown files from content/ and serves them as pages.
Run with: python app.py  (local dev)
Build with: python freeze.py  (generates static site for deployment)
"""

import os
import json
from flask import Flask, render_template, abort
import frontmatter   # reads the --- metadata block at top of .md files
import markdown      # converts markdown text → HTML

app = Flask(__name__)

# Content directories
POSTS_DIR    = "content/posts"
PROJECTS_DIR = "content/projects"

# Site config
SITE = {
    "name":      "Parinwaris (Hui) Pangprasertgul",
    "title":     "Computer Science & Design · SUTD",
    "bio":       "Passionate in backend engineering, data systems, data science, and smart cities.",
    "email":     "parinwaris.pangprasertgul@gmail.com",
    "github":    "https://github.com/parinwarishui",
    "linkedin":  "https://linkedin.com/in/parinwaris-pangprasertgul",
    "photo":     "/static/img/parinwaris.jpg",
}

# Markdown render
def render_md(text):
    """Convert a markdown string to safe HTML.
    Extensions used:
      fenced_code  — ``` code blocks with optional language label
      tables       — | col | col | table syntax
      attr_list    — {.class} attribute shorthand on elements
      nl2br        — single newlines become <br> tags
    """
    return markdown.markdown(text, extensions=[
        "fenced_code",
        "tables",
        "attr_list",
        "nl2br",
    ])


# Content loader
def load_content(directory):
    """
    Load every .md file in `directory` (skipping _templates).
    Returns list of dicts, sorted newest-first by date.

    Each dict has:
      slug     — filename without .md  (used in the URL)
      title    — from frontmatter
      date     — from frontmatter (string)
      tags     — list of strings from frontmatter
      summary  — short description from frontmatter
      image    — optional hero image path from frontmatter
      content  — HTML string rendered from the markdown body
    """
    items = []

    for filename in os.listdir(directory):
        # Skip non-markdown and private template files
        if not filename.endswith(".md") or filename.startswith("_"):
            continue

        filepath = os.path.join(directory, filename)
        post = frontmatter.load(filepath)       # parses --- block + body
        slug = filename.replace(".md", "")

        items.append({
            "slug":    slug,
            "title":   post.get("title",   "Untitled"),
            "date":    str(post.get("date", "")),
            "tags":    post.get("tags",    []),
            "summary": post.get("summary", ""),
            "image":   post.get("image",   None),
            "content": render_md(post.content),
        })

    # Newest date first
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


# Routes
@app.route("/")
def home():
    return render_template("home.html", site=SITE, page="home")


@app.route("/projects/")
def projects():
    all_projects = load_content(PROJECTS_DIR)
    return render_template("projects.html", site=SITE, projects=all_projects, page="projects")


@app.route("/projects/<slug>/")
def project(slug):
    for p in load_content(PROJECTS_DIR):
        if p["slug"] == slug:
            return render_template("project.html", site=SITE, project=p, page="projects")
    abort(404)


@app.route("/blog/")
def blog():
    all_posts = load_content(POSTS_DIR)
    return render_template("blog.html", site=SITE, posts=all_posts, page="blog")


@app.route("/blog/<slug>/")
def post(slug):
    for p in load_content(POSTS_DIR):
        if p["slug"] == slug:
            return render_template("post.html", site=SITE, post=p, page="blog")
    abort(404)


@app.route("/cv/")
def cv():
    return render_template("cv.html", site=SITE, page="cv")


@app.route("/search/")
def search():
    """
    Build a JSON index of all posts + projects and pass it to the template.
    The search page uses vanilla JS to filter that index — no backend needed,
    which means it works after Frozen-Flask turns everything into static HTML.
    """
    posts    = load_content(POSTS_DIR)
    projects = load_content(PROJECTS_DIR)

    index = []
    for p in posts:
        index.append({
            "title":   p["title"],
            "summary": p["summary"],
            "tags":    p["tags"],
            "date":    p["date"],
            "url":     f"/blog/{p['slug']}/",
            "type":    "post",
        })
    for p in projects:
        index.append({
            "title":   p["title"],
            "summary": p["summary"],
            "tags":    p["tags"],
            "date":    p["date"],
            "url":     f"/projects/{p['slug']}/",
            "type":    "project",
        })

    return render_template(
        "search.html",
        site=SITE,
        page="search",
        search_index=json.dumps(index),   # serialised for inline JS
    )


# dev server
if __name__ == "__main__":
    app.run(debug=True)   # http://127.0.0.1:5000