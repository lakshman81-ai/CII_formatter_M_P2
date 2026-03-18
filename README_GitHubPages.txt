CAESAR II Neutral File Generator (GitHub Pages Serverless Edition)

This package contains everything you need to host the CAESAR II tool 100% serverless on GitHub Pages. 

KEY FEATURES:
- No Server Required: The Python script runs natively in the browser via PyScript/Pyodide.
- Middle-Layer CSV Input: Users fill out the generated `middle_layer_template.csv` with their piping geometry (DX, DY, DZ, Diameter). 
- Auto-Calculation: The in-browser Python parses the CSV, injects your custom global defaults from `config.py`, pads everything else with -1.0101d0 to trigger CAESAR II standard code magic calculations, and generates a perfect 0-byte `.cii` file instantly.

HOW TO HOST:
1. Unzip this package.
2. Push the files to a public GitHub repository.
3. Enable "GitHub Pages" in the repository settings (deploy from main branch).
4. The tool is now live on the internet! 

Note: MS Access `.ACCDB` files cannot be parsed securely in web browsers due to binary format constraints. To process `.ACCDB` files natively, you must run the local Flask server provided in the prior deliverable (`app.py`), or use `generate_middle_csv.py` to copy your Access Data into the CSV template first.
