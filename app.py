import os
from flask import Flask, request, send_from_directory, jsonify, Response
from analyze_defaults import get_table_data
import tempfile

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/convert-accdb", methods=["POST"])
def convert_accdb():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.lower().endswith('.accdb') or file.filename.lower().endswith('.mdb')):
        # Save file temporarily to disk to use mdbtools
        fd, temp_path = tempfile.mkstemp(suffix=".accdb")
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(file.read())

            df = get_table_data(temp_path, "INPUT_BASIC_ELEMENT_DATA")
            if df is None:
                return jsonify({"error": "Could not extract INPUT_BASIC_ELEMENT_DATA. Make sure mdbtools is installed and it's a valid ACCDB."}), 500

            csv_str = df.to_csv(index=False)
            return Response(
                csv_str,
                mimetype="text/csv",
                headers={"Content-disposition": f"attachment; filename={file.filename}.csv"}
            )
        finally:
            os.remove(temp_path)
    else:
        return jsonify({"error": "Invalid file format. Must be .accdb or .mdb"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
