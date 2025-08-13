# Nulang

Nulang is a custom **Python-interpreted programming language** with syntax restricted to **numpad characters**. 
It features its own interpreter, a web-based documentation site, and a built-in code editor for real-time, in-browser execution.

Originally built for a hackathon, Nulang won the **"Most Technical"** award for its unique language design and full-stack implementation.

---

## 🌐 Live Demo
Visit the live site: **[https://nulang.onrender.com](https://nulang.onrender.com)**  
Type your Nulang code in the editor, click **RUN**, and see the output instantly.

---

## ✨ Features
- **Custom Programming Language** — Syntax limited to numpad characters, with its own interpreter (`src/main.py`).
- **Interactive Playground** — In-browser code editor with instant execution feedback.
- **Built-in Documentation** — Learn the language and test code side-by-side.
- **Secure Execution** — Code runs in a sandboxed Docker environment on Render.
- **Responsive UI** — Styled with CSS for a clean, readable layout.

---

## 📂 Project Structure
```
.
├── pages/           # Frontend (HTML, CSS, JS, docs & playground)
│   ├── docs.html
│   ├── docs.css
│   ├── code.js
│   └── home.html
├── src/             # Backend & Interpreter
│   ├── main.py      # Nulang interpreter
│   └── webserver.py # Flask app serving site + code execution API
├── Dockerfile       # Deployment configuration
├── requirements.txt # Python dependencies
└── .dockerignore    # Files excluded from Docker build
```

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized runs)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally
```bash
python src/webserver.py
```
Open [http://localhost:3000/docs](http://localhost:3000/docs) in your browser.

---

## 🐳 Run with Docker
```bash
docker build -t nulang .
docker run -p 3000:3000 nulang
```
Visit [http://localhost:3000/docs](http://localhost:3000/docs).

---

## 🌍 Deployment
Nulang is deployed on [Render](https://render.com) using Docker:
1. Push code to GitHub.
2. Create a new **Docker Web Service** in Render.
3. Render builds and deploys the container from `Dockerfile`.
4. Live at: `https://<your-render-url>/docs`

---

## 🏆 Hackathon Achievement
- **Award:** *Most Technical*  
- **Event:** Hackathon 2024  
- Recognized for creating a fully functional interpreted language and an interactive web-based development environment in under 48 hours.

---

## 📜 Example Nulang Program

**Program:**
```
# Assign 1 to variable 1001
-.1001./.1./

# Loop from 1 to 10, printing each number
00.-.i./.1./.--/.i./.11./.-.i.++.i./.1./
.947.i
```

**Explanation:**
- `-.1001./.1./` → Assigns integer value `1` to variable `1001`.
- `00.` → For-loop construct.
- `.947.i` → Prints the value of `i`.

**Output:**
```
1
2
3
4
5
6
7
8
9
10
```

---
