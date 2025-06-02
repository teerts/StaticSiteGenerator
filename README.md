# 🚀✨ Static Site Generator ✨🚀

A simple, extensible static site generator written in Python. 🐍📄

---

## Usage:

1. **Add Markdown Content**  
   Place `.md` files in `content/` (e.g. `index.md`, `about.md`).

2. **Customize Template**  
   Edit `template.html` (use `{{ Title }}` and `{{ Content }}`).

3. **Add Static Files to Reference in Markdown Files**  
   Put images, CSS, etc. in `static/`.

4. **Build Locally using main.sh**  
Output is in `docs/`.

5. **Build for GitHub Pages:**  or **Navigate to your local webserver**
For GitHub: Edit `build.sh` with your repo name -> Push built contents. 
For local web server: https://{yourip}:{port}/{destinationfolder}

6. Go to https://USERNAME.github.io/REPONAME/ (i.e https://teerts.github.io/StaticSiteGenerator/)

