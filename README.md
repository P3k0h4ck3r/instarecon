# 🔥 InstaRecon

**InstaRecon** is a hybrid **Instagram OSINT & media downloader tool** built with Python.
It allows users to gather public Instagram profile information and download media using both a **Command Line Interface (CLI)** and a **browser-based Web UI**.

The tool can scan public profiles to extract details such as name, bio, followers, following, and post count. It also supports downloading **profile pictures, recent posts, and specific posts via shortcode or link**.

---

# 🚀 Features

✔ Instagram profile OSINT scanning
✔ Extract profile information (bio, followers, following, posts)
✔ Download profile pictures
✔ Download recent posts
✔ Download a specific post via shortcode or link
✔ Command Line Interface (CLI) support
✔ Localhost Web UI dashboard
✔ Neon styled web interface
✔ ASCII banner branding in CLI mode
✔ Help menu with usage examples

---

# 🛠 Technologies Used

* **Python**
* **Flask** (Web Interface)
* **Instaloader** (Instagram data access)
* **Argparse** (CLI argument parsing)

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/p3k0h4ck3r/InstaRecon.git
cd InstaRecon
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask instaloader
```

---

# 💻 CLI Usage

Scan profile information:

```bash
python instarecon.py nasa
```

Download profile picture:

```bash
python instarecon.py nasa -dw -pfp
```

Download recent posts:

```bash
python instarecon.py nasa -dw -p
```

Download specific post:

```bash
python instarecon.py nasa -dw -sp SHORTCODE
```

Example:

```bash
python instarecon.py nasa -dw -sp DB7aY2xR4vG
```

---

# 🌐 Web Interface Mode

Run the tool in **Web UI mode**:

```bash
python instarecon.py -l
```

Open in browser:

```
http://127.0.0.1:5000
```

From the web dashboard you can:

* Scan profiles
* Download profile pictures
* Download recent posts
* Paste Instagram post link to download a specific post

---

# 📁 Output Structure

Downloaded files are saved automatically:

```
downloads/
   username/
      profile_pic.jpg
      post1.jpg
      post2.jpg

single_post/
   media.jpg
```

---

# ⚠ Disclaimer

This tool is intended for **educational and OSINT purposes only**.
The developer is not responsible for any misuse or violation of Instagram's terms of service.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Peko Sarshu**

GitHub
https://github.com/p3k0h4ck3r

Instagram
https://instagram.com/pekopekoboy5

---

⭐ If you like this project, consider **starring the repository**!
