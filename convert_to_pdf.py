"""
Convert Markdown to PDF using markdown2pdf or alternative method
"""
import os
import subprocess
import markdown
from pathlib import Path

def convert_md_to_html(md_file, html_file):
    """Convert markdown to styled HTML"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'tables', 'fenced_code', 'toc']
    )
    
    # Create full HTML with styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resource Monitoring System - Component 8</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }}
            
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
            }}
            
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 8px;
                margin-top: 25px;
            }}
            
            h3 {{
                color: #555;
                margin-top: 20px;
            }}
            
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 0.9em;
                color: #c7254e;
            }}
            
            pre {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-left: 4px solid #3498db;
                padding: 15px;
                border-radius: 4px;
                overflow-x: auto;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                color: #333;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            
            th {{
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
                border: 1px solid #2980b9;
            }}
            
            td {{
                padding: 10px;
                border: 1px solid #ddd;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                padding-left: 20px;
                margin-left: 0;
                color: #555;
                font-style: italic;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #eee;
                margin: 30px 0;
            }}
            
            @media print {{
                body {{
                    max-width: 100%;
                }}
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                pre, table {{
                    page-break-inside: avoid;
                }}
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ Created HTML: {html_file}")
    return html_file

def convert_html_to_pdf_chrome(html_file, pdf_file):
    """Convert HTML to PDF using Chrome/Edge headless"""
    
    # Try different browser paths
    browser_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    
    browser_exe = None
    for path in browser_paths:
        if os.path.exists(path):
            browser_exe = path
            break
    
    if not browser_exe:
        print("✗ Chrome or Edge not found. Please use the HTML file and print to PDF manually.")
        return False
    
    # Convert HTML to absolute path
    abs_html = os.path.abspath(html_file)
    abs_pdf = os.path.abspath(pdf_file)
    
    # Run headless browser to convert to PDF
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf=" + abs_pdf,
        abs_html
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        print(f"✓ Created PDF: {pdf_file}")
        return True
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Converting Markdown to PDF")
    print("="*60)
    
    files_to_convert = [
        ("Component_8_Resource_Monitoring_System.md", 
         "Component_8_Resource_Monitoring_System"),
        ("Component_8_Quick_Reference.md", 
         "Component_8_Quick_Reference"),
        ("Component_8_INDEX.md", 
         "Component_8_INDEX"),
    ]
    
    for md_file, base_name in files_to_convert:
        if os.path.exists(md_file):
            print(f"\nProcessing: {md_file}")
            
            # Convert to HTML
            html_file = base_name + ".html"
            convert_md_to_html(md_file, html_file)
            
            # Try to convert to PDF
            pdf_file = base_name + ".pdf"
            success = convert_html_to_pdf_chrome(html_file, pdf_file)
            
            if not success:
                print(f"\n💡 Alternative: Open {html_file} in your browser and use Ctrl+P to save as PDF")
        else:
            print(f"✗ File not found: {md_file}")
    
    print("\n" + "="*60)
    print("Conversion Complete!")
    print("="*60)
    print("\n📄 HTML files created - you can:")
    print("  1. Open them in a browser")
    print("  2. Press Ctrl+P (Print)")
    print("  3. Select 'Save as PDF'")
    print("\nOr if PDF was created successfully, you can use it directly.")
