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

5. **Build & Preview Your Site:**

   - **For GitHub Pages:**  
     1. Edit `build.sh` and set your repo name:  
        ```
        python3 src/main.py "/YOUR_REPO_NAME/"
        ```
     2. Run the script:  
        ```
        ./build.sh
        ```
     3. Push the contents of the `docs/` folder to your repository’s main branch.
     4. In your GitHub repo settings, set Pages to serve from `/docs`.
     5. Go to https://USERNAME.github.io/REPONAME/ (i.e https://teerts.github.io/StaticSiteGenerator/)

   - **For Local Web Server:**  
     1. After building, serve the `docs/` folder with your favorite web server.  
     2. Open in your browser:  
        ```
        http://{your-ip}:{port}/docs/
        ```




