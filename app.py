from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import os

VERSION = "1.1.0"

image_file_types = [
    'jpg', 'jpeg',
    'png',
    'gif',
    'bmp',
    'tiff', 'tif',
    'webp',
    'ico',
    'svg',
    'apng',
    'avif',
    'heif',
    'jp2',
    'jxr',
]

video_file_types = [
    'mp4',
    'webm',
    'ogg',
    'mkv',
    'avi',
    'mov',
    'flv',
    'm4v',
    '3gp',
    'wmv',
    'mpeg',
    'mpg',
    'm2v',
    'ts',
    'mpd'
]

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
upload_folder_path = Path(UPLOAD_FOLDER)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024 # 10 GiB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up a route to serve the HTML form
@app.route('/')
def index():
    filesHTML = ""

    entries = list(upload_folder_path.iterdir())
    dirCount = int(0)

    for dirent in entries:
        if dirent.is_file() == True:
            filesHTML += '<li><a class="f" href="/files/' + dirent.name + '">' + dirent.name + '</a></li>'
        elif dirent.is_dir() == True:
            dirCount += 1

    dirsOmmitedHTML = ""
    if dirCount != 0:
        dirsOmmitedHTML = '<li>' + str(dirCount) + ' dirs ommited</li>'

    if filesHTML == "" and dirsOmmitedHTML == "":
        filesHTML = "<li>nothing yet</li>"

    return render_template('upload.html', files=filesHTML, dirsOmmitedElement=dirsOmmitedHTML, version=VERSION)

# Set up a route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part'

    files = request.files.getlist('files')

    for file in files:
        if file.filename == '':
            return 'Empty file name'

        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    return '<a href="/">Files uploaded successfully!</a>'

# Set up a route to serve the uploaded files
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/gallery")
def gallery_route():
    #get file list
    entries = list(upload_folder_path.iterdir())

    html = ""

    for dirent in entries:
        if dirent.is_file():
            file_extension = dirent.name.lower().split(".")[-1]
            if file_extension in image_file_types:
                #is an image
                #add img html
                html += f'<div class="item"><a href="/files/{dirent.name}"><img src="/files/{dirent.name}" /></a><p>{dirent.name}</p></div>'
            elif file_extension in video_file_types:
                html += f'<div class="item"><video controls><source src="/files/{dirent.name}"></source></video><p>{dirent.name}</p></div>'

    if html == "":
        html = '<p style="color: black; text-align: left; padding: 20px 0">(empty)</p>'

    return render_template("gallery.html", html=html, version=VERSION)

if __name__ == '__main__':
    app.run(port=3031, host="0.0.0.0")
