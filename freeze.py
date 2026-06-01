"""
freeze.py — Static site generator
Run: python freeze.py
Outputs every page as a plain .html file into /build/
That /build/ folder is what gets deployed to GitHub Pages.
"""

from flask_frozen import Freezer
from app import app, load_content, POSTS_DIR, PROJECTS_DIR

# Point Frozen-Flask at our app
freezer = Freezer(app)

# Where the static files land (committed to gh-pages branch)
app.config["FREEZER_DESTINATION"]    = "build"
app.config["FREEZER_RELATIVE_URLS"]  = True   # makes links work without a server

# ── Tell Freezer about dynamic routes ─────────────────────────────────────────
# Flask knows /projects/<slug>/ exists, but Frozen-Flask needs to know
# which slugs actually exist so it can generate a file for each one.

@freezer.register_generator
def project():
    for p in load_content(PROJECTS_DIR):
        yield {"slug": p["slug"]}

@freezer.register_generator
def post():
    for p in load_content(POSTS_DIR):
        yield {"slug": p["slug"]}


if __name__ == "__main__":
    freezer.freeze()
    print("\n✓  Static site built → /build/")
    print("   Next: run  deploy.sh  to push to GitHub Pages\n")