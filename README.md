# 🧠 training-app-3000

A Flask-based web interface for browsing image/audio training sets stored in a filesystem.
It dynamically loads training sets, displays corresponding `.jpg` and `.m4a` files,
and provides simple navigation and diagnostics.

![Screenshot of training-app-3000](/screenshots/training-app-3000_screen1.jpg)


---

## 🚀 Features

- Browse through training image/audio pairs
- Auto-indexes training sets on startup
- Serves media content with safe path joining
- Environment-configurable root directory and logging
- Diagnostic `/about` page with environment and platform info

---

## 📁 Directory Structure

The app expects a directory like:

```
training_sets/
  ├── set1/
  │    ├── img001.jpg
  │    ├── img001.m4a
  │    └── ...
  └── set2/
       ├── ...
```

Each subdirectory under `TRAINING_SET_ROOT_DIR` is treated as a training set.

---

## 🔧 Configuration

Set environment variables before running:

| Variable               | Description                                                | Default           |
|------------------------|------------------------------------------------------------|-------------------|
| `TRAINING_SET_ROOT_DIR`| Path to training sets directory                            | `training_sets`   |
| `LOG_LEVEL`            | Log verbosity (`DEBUG`, `INFO`, etc.)                      | `INFO`            |

---

## 📦 Installation

```bash
git clone <your-repo-url>
cd <your-project>
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
export TRAINING_SET_ROOT_DIR=path/to/training_sets
export LOG_LEVEL=DEBUG
python app.py
```

Runs on: [http://0.0.0.0:5000](http://0.0.0.0:5000)

---

## 🌐 Routes

### `/` or `/viewer`
- Displays image/audio pairs
- Query params:
  - `set`: training set name
  - `index`: image index (default = 0)

### `/training_sets/<set_name>/<filename>`
- Serves media files (image or audio) securely

### `/about`
- Shows app metadata, environment vars, and diagnostics

---

## 📄 Templates Required

Ensure the following are present in `templates/`:

- `viewer.html`
- `about.html`

---

## 🛠 Logging

- Logging is set up via `log_config.setup_logging()`
- Supports log rotation
- Middleware: `ProxyFix` (for reverse proxy support)

---

## 🧠 Core Logic

- Caches training sets and image names on startup
- Randomizes image order for variety
- Uses safe file joining to avoid directory traversal
- Handles errors gracefully with logging

---

## ⚠️ Notes

- Only `.jpg` images and `.m4a` audio files are supported.
- Audio is optional but must share the same base name as the image.
- Make sure training sets are readable and properly structured.

---

## 📋 License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2025 Daniel Brenk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.