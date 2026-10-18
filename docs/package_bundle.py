"""
StockSense AI - Documentation & Interview Preparation Bundle Packager
Packages all 4 generated PDFs, presentation deck, markdown source, and diagrams
into StockSense_AI_Documentation_Bundle.zip at the project root.
"""

import os
import zipfile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP = os.path.join(ROOT_DIR, 'StockSense_AI_Documentation_Bundle.zip')

FILES_TO_BUNDLE = [
    ('AI_Stock_Market_Project_Complete_Notes.pdf', 'AI_Stock_Market_Project_Complete_Notes.pdf'),
    ('AI_Stock_Market_Project_Interview_QA.pdf', 'AI_Stock_Market_Project_Interview_QA.pdf'),
    ('AI_Stock_Market_Quick_Revision.pdf', 'AI_Stock_Market_Quick_Revision.pdf'),
    ('AI_Stock_Market_Architecture_Diagrams.pdf', 'AI_Stock_Market_Architecture_Diagrams.pdf'),
    ('AI_Stock_Market_Project_Notes.md', 'AI_Stock_Market_Project_Notes.md'),
    ('AI_Stock_Market_Project_Interview_Presentation.pptx', 'AI_Stock_Market_Project_Interview_Presentation.pptx'),
    ('docs/diagrams/architecture_system.png', 'diagrams/architecture_system.png'),
    ('docs/diagrams/architecture_ml_pipeline.png', 'diagrams/architecture_ml_pipeline.png'),
    ('docs/diagrams/architecture_data_flow.png', 'diagrams/architecture_data_flow.png'),
    ('docs/diagrams/architecture_auth_flow.png', 'diagrams/architecture_auth_flow.png'),
    ('docs/diagrams/architecture_database_erd.png', 'diagrams/architecture_database_erd.png'),
    ('docs/diagrams/architecture_sentiment_assistant.png', 'diagrams/architecture_sentiment_assistant.png'),
]

def create_bundle():
    print(f"Creating Zip Bundle: {OUTPUT_ZIP}")
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for rel_src, arcname in FILES_TO_BUNDLE:
            full_src = os.path.join(ROOT_DIR, rel_src)
            if os.path.exists(full_src):
                zf.write(full_src, arcname=arcname)
                print(f"  Added: {arcname} ({os.path.getsize(full_src):,} bytes)")
            else:
                print(f"  WARNING: Missing {full_src}")

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\nBundle successfully created: {OUTPUT_ZIP} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    create_bundle()
