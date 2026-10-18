"""
StockSense AI - Master Project Packaging Script
Creates the production-ready, interview-ready downloadable ZIP:
Stock_Market_Analysis_Project.zip
"""

import os
import sys
import zipfile
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_OUTPUT = os.path.join(ROOT_DIR, 'Stock_Market_Analysis_Project.zip')

EXCLUDE_DIRS = {
    '__pycache__', '.git', '.github', '.system_generated',
    '.gemini', 'scratch', 'node_modules', 'ai-stock-predictor'
}

EXCLUDE_EXTS = {
    '.pyc', '.pyo', '.pyd', '.tmp', '.log', '.zip'
}

EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db', 'desktop.ini'
}

def should_exclude(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    filename = os.path.basename(rel_path)
    if filename in EXCLUDE_FILES:
        return True
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXCLUDE_EXTS:
        return True
    return False

def create_package():
    print(f"Creating master ZIP package at: {ZIP_OUTPUT}...")
    if os.path.exists(ZIP_OUTPUT):
        os.remove(ZIP_OUTPUT)

    source_items = [
        'apps', 'config', 'templates', 'static', 'tests',
        'ml_models', 'manage.py', 'db.sqlite3', 'requirements.txt',
        '.env.example', 'README.md'
    ]

    total_files = 0
    with zipfile.ZipFile(ZIP_OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 1. Package source_code/
        for item in source_items:
            item_path = os.path.join(ROOT_DIR, item)
            if not os.path.exists(item_path):
                continue
            if os.path.isfile(item_path):
                arcname = os.path.join('Stock_Market_Analysis_Project', 'source_code', item)
                zf.write(item_path, arcname)
                total_files += 1
            else:
                for root, dirs, files in os.walk(item_path):
                    # Filter out excluded dirs in-place
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for f in files:
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, ROOT_DIR)
                        if should_exclude(rel_path):
                            continue
                        arcname = os.path.join('Stock_Market_Analysis_Project', 'source_code', rel_path)
                        zf.write(full_path, arcname)
                        total_files += 1

        # 2. Package root files (README.md, .env.example, requirements.txt)
        root_files = ['README.md', '.env.example', 'requirements.txt']
        for rf in root_files:
            rf_path = os.path.join(ROOT_DIR, rf)
            if os.path.exists(rf_path):
                arcname = os.path.join('Stock_Market_Analysis_Project', rf)
                zf.write(rf_path, arcname)
                total_files += 1

        # 3. Package documentation/
        pdf_path = os.path.join(ROOT_DIR, 'Stock_Market_Analysis_Interview_Notes.pdf')
        if os.path.exists(pdf_path):
            arcname = os.path.join('Stock_Market_Analysis_Project', 'documentation', 'Stock_Market_Analysis_Interview_Notes.pdf')
            zf.write(pdf_path, arcname)
            total_files += 1

        # 4. Package screenshots/
        screenshots_dir = os.path.join(ROOT_DIR, 'screenshots')
        if os.path.exists(screenshots_dir):
            for f in os.listdir(screenshots_dir):
                if f.endswith('.png'):
                    full_p = os.path.join(screenshots_dir, f)
                    arcname = os.path.join('Stock_Market_Analysis_Project', 'screenshots', f)
                    zf.write(full_p, arcname)
                    total_files += 1

        # 5. Package diagrams inside documentation/diagrams/
        diagrams_dir = os.path.join(ROOT_DIR, 'docs', 'diagrams')
        if os.path.exists(diagrams_dir):
            for f in os.listdir(diagrams_dir):
                if f.endswith('.png'):
                    full_p = os.path.join(diagrams_dir, f)
                    arcname = os.path.join('Stock_Market_Analysis_Project', 'documentation', 'diagrams', f)
                    zf.write(full_p, arcname)
                    total_files += 1

    zip_size_mb = os.path.getsize(ZIP_OUTPUT) / (1024 * 1024)
    print(f"Successfully created {ZIP_OUTPUT} ({zip_size_mb:.2f} MB, {total_files} files packaged)!")

def verify_package():
    print(f"Verifying {ZIP_OUTPUT} integrity...")
    with zipfile.ZipFile(ZIP_OUTPUT, 'r') as zf:
        namelist = zf.namelist()
        bad_file = zf.testzip()
        if bad_file:
            print(f"ERROR: Corrupted file found in ZIP: {bad_file}")
            sys.exit(1)
        print(f"ZIP integrity verified! Total entries: {len(namelist)}")
        
        # Check required files
        must_have = [
            'Stock_Market_Analysis_Project/README.md',
            'Stock_Market_Analysis_Project/.env.example',
            'Stock_Market_Analysis_Project/requirements.txt',
            'Stock_Market_Analysis_Project/documentation/Stock_Market_Analysis_Interview_Notes.pdf',
            'Stock_Market_Analysis_Project/source_code/manage.py',
            'Stock_Market_Analysis_Project/source_code/config/settings.py',
            'Stock_Market_Analysis_Project/source_code/apps/news/services.py',
            'Stock_Market_Analysis_Project/source_code/apps/predictions/services/forecasting.py',
            'Stock_Market_Analysis_Project/screenshots/login_page.png',
            'Stock_Market_Analysis_Project/screenshots/stock_dashboard.png',
            'Stock_Market_Analysis_Project/screenshots/stock_chart.png',
            'Stock_Market_Analysis_Project/screenshots/ml_forecasting.png',
            'Stock_Market_Analysis_Project/screenshots/news_sentiment.png'
        ]
        
        for mh in must_have:
            if mh in namelist:
                print(f"  [OK] Found {mh}")
            else:
                print(f"  [MISSING] {mh}")
                sys.exit(1)

    print("All required project files are verified and present in the ZIP archive!")

if __name__ == '__main__':
    create_package()
    verify_package()
