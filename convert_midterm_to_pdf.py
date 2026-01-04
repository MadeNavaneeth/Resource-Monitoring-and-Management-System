"""
Convert Mid-Term Report to PDF
"""
import os
import subprocess
import markdown

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
        <title>Mid-Term Report - Resource Monitoring System</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
            }}
            
            body {{
                font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 210mm;
                margin: 0 auto;
                padding: 20px;
            }}
            
            h1 {{
                color: #1a237e;
                text-align: center;
                border-bottom: 3px solid #1a237e;
                padding-bottom: 15px;
                margin-top: 30px;
                margin-bottom: 25px;
                font-size: 1.8em;
                page-break-after: avoid;
            }}
            
            h2 {{
                color: #283593;
                border-bottom: 2px solid #5c6bc0;
                padding-bottom: 10px;
                margin-top: 30px;
                margin-bottom: 20px;
                font-size: 1.5em;
                page-break-after: avoid;
            }}
            
            h3 {{
                color: #3949ab;
                margin-top: 25px;
                margin-bottom: 15px;
                font-size: 1.2em;
                page-break-after: avoid;
            }}
            
            code {{
                background-color: #f5f5f5;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 0.9em;
                color: #d32f2f;
            }}
            
            pre {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-left: 4px solid #1a237e;
                padding: 15px;
                border-radius: 4px;
                overflow-x: auto;
                page-break-inside: avoid;
                margin: 20px 0;
                font-size: 0.85em;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                color: #212529;
                font-size: 1em;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                page-break-inside: avoid;
                font-size: 0.9em;
            }}
            
            th {{
                background-color: #1a237e;
                color: white;
                padding: 12px 10px;
                text-align: left;
                border: 1px solid #0d1642;
                font-weight: 600;
            }}
            
            td {{
                padding: 10px;
                border: 1px solid #dee2e6;
                vertical-align: top;
            }}
            
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            
            blockquote {{
                border-left: 4px solid #5c6bc0;
                padding-left: 20px;
                margin-left: 0;
                color: #555;
                font-style: italic;
                background-color: #f5f7fa;
                padding: 10px 20px;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #e0e0e0;
                margin: 30px 0;
            }}
            
            ul, ol {{
                margin: 15px 0;
                padding-left: 35px;
            }}
            
            li {{
                margin: 8px 0;
                line-height: 1.6;
            }}
            
            strong {{
                color: #1a237e;
                font-weight: 600;
            }}
            
            a {{
                color: #3949ab;
                text-decoration: none;
            }}
            
            .center {{
                text-align: center;
            }}
            
            @media print {{
                body {{
                    max-width: 100%;
                }}
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                pre, table, blockquote {{
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
        print("✗ Chrome or Edge not found.")
        return False
    
    # Convert HTML to absolute path
    abs_html = os.path.abspath(html_file)
    abs_pdf = os.path.abspath(pdf_file)
    
    # Run headless browser
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
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("Converting Mid-Term Report to PDF")
    print("="*70)
    
    md_file = "MidTerm_Report_Database_Project.md"
    
    if os.path.exists(md_file):
        print(f"\nProcessing: {md_file}")
        
        # Convert to HTML
        html_file = "MidTerm_Report_Database_Project.html"
        convert_md_to_html(md_file, html_file)
        
        # Convert to PDF
        pdf_file = "MidTerm_Report_Database_Project.pdf"
        success = convert_html_to_pdf_chrome(html_file, pdf_file)
        
        if not success:
            print(f"\n💡 Open {html_file} in browser and press Ctrl+P to save as PDF")
    else:
        print(f"✗ File not found: {md_file}")
    
    print("\n" + "="*70)
    print("Conversion Complete!")
    print("="*70)
