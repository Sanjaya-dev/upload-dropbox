from flask import Flask, request, jsonify
import dropbox
import os

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    filename = request.headers.get("X-Filename")
    if not filename:
        return jsonify({"error": "Filename missing in headers"}), 400

    file_data = request.data
    if not file_data:
        return jsonify({"error": "No file uploaded"}), 400

    # Upload ke Dropbox
    dbx = dropbox.Dropbox("sl.u.AFxfj_FaNdO_BoIGd3Ea7oScr1wP4_FH-H9LE57jEv4rRqxfqa4Pso_joCygjeI3jhSuWFH-QVgbZLm8Cr8DB3-OzOLCSIrobw48ArLJapEjVdl0dIya7_a0XcQEPRUI5jdnZ2-a5TT8iPi_SanwmoRtZhzAjGZR6JuRNk-a4YTnqhRO3fhuHVAoTZbFaqnFa1KtGtEHaDaHZ6k3y64BvySmmkH5I-rgfztTBLm7iR-2MAbSE82GT2QY7a-R4NVdOmepuvRbbuiGvsAVJGPYIWppvZNw_VvgwQ8KDW_jPAQWbsQlYZYpywS00zlVjRolf2E99HN5MJ3tE2gHJcvN7vrTJA7keg9Ryol7P-QFFj5Wa-lGcXw-5WZRCrdlXCgv2h6Cy0fSF-OM5pMNM3K46pCWciTJliPSW4ad8XLzBbCSWXi0GR5EoYah9mS8XZgKo4MDVN99pb-IaH7BicHjsJHqRSxXTcYj_PQ8gndFuLVJBEuK-wd_kKd442SIORVPjkiwl7hnJVvHST3KC2ZCHyTjASXt9xnLidlVSwUfYYDL1lDqFWurcsEnoWpSoQ3j8EY5Z_6KRgwvXrDBD96mYaQwx6gPcB5K9ecaFVeRevokIjpUiW1SFYRtVckbfW8ym4-F5CyQE0xKSonIdytlMkGv1vwnN9eh8GfvYq5zS4QDBqUuN_lNQ9MuKuSW7-T-xa9aDwZ8JPBvG5qe5ayJ_h5gud-MXG4yVu7ElmCivLsVIh_c3aH6hZ0E7aYEqCm5NVzz1UoSTYqaEx6u0mG3OVJ8DEc9Wja22yn8gNlJiUe8p1qRseQoTO0HUUTNEylob9MZ5B7FqK668H-SFnCSqjaDuoZ1TRiFAcAWrClY6m9h7CUZqtaeHv-EEpNevxdtZ6e9r19hG82eSG6A-EwvccGG7A9vaKNbAdummF9lStSOf8n7wobzfj23Mq8CPIBQLM-xj0rC5W3euPwDJ6g1WPzQCWf4YiNIXvPCkQY2jiPTGcOZMj0vMzt3Wuz__Bt_MInEZmENRi5mxrW15IapS61cANs8avvQ9rvDsba9-qJJs7gK_e-nZGMnJkuPESkFUCBn6iwNgr_G_YSeO4R2NWRtezWPEWYwEUiTSEVc1kjH78ijbo8TEZJiZ6kuZoUwYH1lcEiC1KxcTcwM7hbg5PC-eO0asISmPvBV3w1B8tgJ7BCjP7PKgmfiqaPKUQYIdPBZK6lZxPKU_sG6TWpfrc45TfPqPfqlybTbMbWVQ6WIzUm-Bz6ckljqCBvNDfmOV-vDxLmu-x61fqiMnSHH9NjQC68C4_t88X8fTPI0smymQcAEA29Wtxerncon2vNjDYi1nRgjadwd4GO5UgLL3HVNVMK0Aud7EX9yZEq_Zu68Czt-09_eSJzXUOp0xq1Xg2s")
    path = f"/uploads/{filename}"
    dbx.files_upload(file_data, path, mute=True)

    # Buat shareable link
    shared_link = dbx.sharing_create_shared_link_with_settings(path).url
    return jsonify({"url": shared_link}), 200
