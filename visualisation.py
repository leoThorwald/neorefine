import marimo as mo
import base64
from io import BytesIO
from PIL import Image  # Requires: pip install pillow (or conda install pillow)
import pandas as pd    # For CSV handling; requires: conda install pandas

# Cell 1: Create a file upload UI element
# Supports single/multiple files, optional file type filters (e.g., ['.csv', '.png'])
# Max file size: 100MB per file
mo.ui.file(filetypes=[".png", ".jpg"], multiple=True)

# Cell 2: Display the uploader widget
uploader

# Cell 3: Reactive handling of uploaded files
# Access via uploader.value (list of dicts with 'name' and 'contents' (bytes))
if uploader.value:
    mo.md(f"### Uploaded {len(uploader.value)} file(s)")
    
    for file_info in uploader.value:
        name = file_info["name"]
        contents = file_info["contents"]
        
        mo.md(f"**File:** {name}")
        
        # Handle different file types
        if name.endswith((".png", ".jpg", ".jpeg")):
            # Decode and display image
            img_data = base64.b64encode(contents).decode()
            mo.html(f'<img src="data:image/png;base64,{img_data}" width="300" />')
        elif name.endswith(".csv"):
            # Load and display as DataFrame
            df = pd.read_csv(BytesIO(contents))
            df
        elif name.endswith(".txt"):
            # Display text content
            text = contents.decode("utf-8")
            mo.md(f"**Content:**\n```text\n{text}\n```")
        else:
            # Generic: Show first 200 bytes as text
            preview = contents[:200].decode("utf-8", errors="ignore")
            mo.md(f"**Preview:**\n```text\n{preview}...\n```")

else:
    mo.md("No files uploaded yet. Drag-and-drop or click to select.")

# Cell 4: Optional - Button to clear uploads
clear_btn = mo.ui.button(label="Clear Uploads", on_click=lambda: setattr(uploader, "value", []))
clear_btn