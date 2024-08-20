import markdown
import pdfkit

def preprocess_markdown_table(markdown_content):
    """Preprocess the markdown content to ensure it's in clean HTML format without unnecessary breaks."""
    processed_content = []
    for line in markdown_content.splitlines():
        # Process each cell in the table line by line
        cells = line.split('|')
        processed_cells = [cell.strip() for cell in cells]
        processed_content.append(' | '.join(processed_cells))
    return '\n'.join(processed_content)  # Return properly joined lines without <br>

def generate_pdf_from_markdown(markdown_content, output_pdf_file):
    """Convert markdown content to PDF with improved formatting."""
    try:
        # Preprocess markdown content for cleaner HTML
        processed_markdown = preprocess_markdown_table(markdown_content)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(processed_markdown)
        
        # Add CSS styling for the table
        css_style = """
        <style>
        body {
            font-size: 9pt;
            font-family: Courier, monospace;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        th, td {
            padding: 5px;
            text-align: left;
            border: 1px solid #ddd;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        td {
            width: 100px;
        }
        </style>
        """
        
        # Combine the CSS with the HTML content
        full_html_content = f"{css_style}{html_content}"
        
        # PDF options (landscape orientation)
        options = {
            'orientation': 'Landscape',
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'zoom': 0.8
        }
        
        # Convert HTML to PDF and save
        pdfkit.from_string(full_html_content, output_pdf_file, options=options)
        print(f"PDF generated successfully: {output_pdf_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")