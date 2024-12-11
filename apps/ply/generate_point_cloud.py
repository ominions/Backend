import numpy as np
import pycolmap 
from pathlib import Path
from .extract_from_read_write_model import create_ply_file

def generate_point_cloud(image_dir, output_path):  
    # Create necessary directories
    output_path.mkdir(parents=True, exist_ok=True)
    # mvs_path = output_path / "mvs"         # Path for multi-view stereo (MVS) results
    # mvs_path.mkdir(parents=True, exist_ok=True)
    database_path = output_path / "database.db"

    # Step 1: Extract features
    print("Extracting features...")
    pycolmap.extract_features(database_path, image_dir)
    print("Feature extraction completed.")

    # Step 2: Match features exhaustively
    print("Matching features...")
    pycolmap.match_exhaustive(database_path)
    print("Feature matching completed.")

    # Step 3: Incremental mapping (Sparse Reconstruction)
    print("Performing sparse reconstruction...")
    maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
    maps[0].write(output_path)
    print(f"Sparse reconstruction completed. Results saved to: {output_path}")
    output_path = output_path / '0'
    create_ply_file(output_path)