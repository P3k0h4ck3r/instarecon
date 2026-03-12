import instaloader
import argparse
import json
from flask import Flask, request, render_template_string

loader = instaloader.Instaloader(
    dirname_pattern="downloads/{target}",
    save_metadata=False,
    download_comments=False
)

app = Flask(__name__)

# -------------------------
# ASCII BANNER
# -------------------------

BANNER = r"""

██╗███╗   ██╗███████╗████████╗ █████╗ ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██║██╔██╗ ██║███████╗   ██║   ███████║██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██║██║╚██╗██║╚════██║   ██║   ██╔══██║██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║██║ ╚████║███████║   ██║   ██║  ██║██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

"""

# -------------------------
# CORE FUNCTIONS
# -------------------------

def scan_profile(username):

    try:

        profile = instaloader.Profile.from_username(
            loader.context,
            username
        )

        data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "private": profile.is_private
        }

        return profile, data

    except Exception as e:

        return None, {"error": str(e)}


def download_pfp(profile):

    loader.download_profilepic(profile)


def download_posts(profile, limit=5):

    count = 0

    for post in profile.get_posts():

        loader.download_post(post, target=profile.username)

        count += 1

        if count >= limit:
            break


def download_single(shortcode):

    post = instaloader.Post.from_shortcode(
        loader.context,
        shortcode
    )

    loader.download_post(post, target="single_post")


def extract_shortcode(url):

    try:

        parts = url.split("/")

        if "p" in parts:
            return parts[parts.index("p")+1]

        if "reel" in parts:
            return parts[parts.index("reel")+1]

    except:

        return None


# -------------------------
# WEB UI
# -------------------------

HTML = """

<html>

<head>

<title>InstaRecon</title>

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
text-align:center;
}

.title{
font-size:34px;
color:#00e5ff;
text-shadow:
0 0 5px #00e5ff,
0 0 10px #00e5ff,
0 0 20px #00e5ff,
0 0 40px #0099ff;
}

.github{
font-size:16px;
color:#7dd3fc;
}

.box{
margin-top:80px;
}

input{
padding:10px;
border-radius:5px;
border:none;
width:250px;
}

button{
padding:10px 20px;
background:#3b82f6;
border:none;
border-radius:5px;
color:white;
margin:5px;
cursor:pointer;
}

.result{
margin-top:20px;
width:500px;
margin-left:auto;
margin-right:auto;
background:#1e293b;
padding:20px;
border-radius:10px;
text-align:left;
}

</style>

</head>

<body>

<div class="box">

<h1 class="title">
InstaRecon By Peko Sarshu
<br>
<span class="github">github - p3k0h4ck3r</span>
</h1>

<form method="POST">

<input name="username" placeholder="Instagram username">

<br><br>

<button name="action" value="scan">Scan</button>

<button name="action" value="pfp">Download PFP</button>

<button name="action" value="posts">Download Posts</button>

<br><br>

<input name="postlink" placeholder="Paste Instagram Post Link">

<button name="action" value="single">Download Specific Post</button>

</form>

{% if result %}

<div class="result">

<pre>{{result}}</pre>

</div>

{% endif %}

</div>

</body>

</html>

"""

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        username = request.form.get("username")
        action = request.form.get("action")
        postlink = request.form.get("postlink")

        if action == "scan":

            profile,data = scan_profile(username)
            result = json.dumps(data,indent=2)

        elif action == "pfp":

            profile,data = scan_profile(username)
            download_pfp(profile)
            result = "Profile picture downloaded"

        elif action == "posts":

            profile,data = scan_profile(username)
            download_posts(profile)
            result = "Posts downloaded"

        elif action == "single":

            shortcode = extract_shortcode(postlink)

            if shortcode:

                download_single(shortcode)
                result = "Specific post downloaded"

            else:

                result = "Invalid link"

    return render_template_string(HTML,result=result)


# -------------------------
# CLI MODE
# -------------------------

def main():

    parser = argparse.ArgumentParser(
        prog="InstaRecon",
        description="Instagram Recon & Downloader Tool",
        epilog="""
Examples:

  python instarecon.py nasa
      Scan profile info

  python instarecon.py nasa -dw -pfp
      Download profile picture

  python instarecon.py nasa -dw -p
      Download recent posts

  python instarecon.py nasa -dw -sp DB7aY2xR4vG
      Download specific post

  python instarecon.py -l
      Start Web UI mode
"""
    )

    parser.add_argument("username", nargs="?", help="Instagram username")

    parser.add_argument("-l","--localhost",action="store_true",help="Run Web Interface")

    parser.add_argument("-dw",action="store_true",help="Enable download mode")

    parser.add_argument("-pfp",action="store_true",help="Download profile picture")

    parser.add_argument("-p",action="store_true",help="Download recent posts")

    parser.add_argument("-sp",metavar="SHORTCODE",help="Download specific post")

    args = parser.parse_args()

    print(BANNER)
    print("github    : p3k0h4ck3r")
    print("instagram : @pekopekoboy5\n")

    if not args.username and not args.localhost:

        parser.print_help()
        return


    if args.localhost:

        print("Starting Web UI → http://127.0.0.1:5000")
        app.run()
        return


    profile,data = scan_profile(args.username)

    print(json.dumps(data,indent=2))


    if args.dw:

        if args.pfp:

            download_pfp(profile)
            print("Profile picture downloaded")

        if args.p:

            download_posts(profile)
            print("Posts downloaded")

        if args.sp:

            download_single(args.sp)
            print("Single post downloaded")


if __name__ == "__main__":

    main()