from flask import Flask, request, jsonify
import dropbox
import os

app = Flask(__name__)
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    content = file.read()
    filename = file.filename

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    CHUNK_SIZE = 4 * 1024 * 1024
    size = len(content)

    if size <= CHUNK_SIZE:
        dbx.files_upload(content, f"/voiceovers/{filename}", mute=True)
    else:
        start = dbx.files_upload_session_start(content[:CHUNK_SIZE])
        cursor = dropbox.files.UploadSessionCursor(start.session_id, offset=CHUNK_SIZE)
        commit = dropbox.files.CommitInfo(f"/voiceovers/{filename}")

        while cursor.offset < size:
            if (size - cursor.offset) <= CHUNK_SIZE:
                dbx.files_upload_session_finish(content[cursor.offset:], cursor, commit)
                break
            dbx.files_upload_session_append_v2(content[cursor.offset:cursor.offset + CHUNK_SIZE], cursor)
            cursor.offset += CHUNK_SIZE

    link = dbx.sharing_create_shared_link_with_settings(f"/voiceovers/{filename}")
    return jsonify({ "link": link.url.replace("?dl=0", "?raw=1") })
