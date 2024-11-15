# Freesurfer Multi-Scale Atlas Processing

## Overview
This Python package provides functionality for processing T1-weighted MRI images using FreeSurfer and the Lausanne 2018 multi-scale atlas parcellation scheme. The implementation includes surface-based and volumetric processing across five different scales of brain parcellation.

## Configuration
### Environment Setup (`setup_environment.json`)
Make this file in the root directory and fill in the paths to your FreeSurfer installation and subjects directory where freesurfer templates are stored.

```json
{
    "FREESURFER_HOME": "/Applications/freesurfer/7.3.2/",
    "SUBJECTS_DIR": "subjects"
}
```

Download example subject directory from [here](https://www.dropbox.com/scl/fo/4km2t62of7vq2ojxk6g6t/AOK9sTli7lkXqKK9zADFUV4?rlkey=a5f963omu20x6929k6xnudadx&dl=0) and place it in the `subjects` directory.

## Class: Multiscaleatlas

### Constructor
```python
def __init__(self, t1, subjectID, output_dir=None)
```
**Parameters:**
- `t1` (str): Path to T1-weighted MRI image
- `subjectID` (str): Unique identifier for the subject
- `output_dir` (str, optional): Custom output directory path

### Methods

#### `setup_environment()`
Configures the FreeSurfer environment variables and initializes the FreeSurfer setup.

#### `recon_all()`
Executes FreeSurfer's recon-all pipeline for structural MRI processing.
- Performs complete reconstruction including cortical surface generation

#### `lausanne2018scale1()` through `lausanne2018scale5()`
Implements the Lausanne 2018 atlas parcellation at five different scales. Each method:
1. Performs surface-to-surface mapping for both hemispheres
2. Calculates anatomical statistics
3. Converts aparc to aseg format
4. Converts output to NIfTI format

Common processing steps for each scale:
- Surface-to-surface mapping (left and right hemispheres)
- Anatomical statistics computation
- Parcellation conversion (MGZ to NIfTI)

#### `move_output()`
Relocates processed data to a specified output directory if provided.

## Command Line Interface
```bash
python freesurfer.py -t1 <t1_image_path> -s <subject_id> [-o <output_directory>]
```

**Arguments:**
- `-t1`: Path to T1-weighted image (required)
- `-s`: Subject ID (required)
- `-o`: Output directory (optional)

## Dependencies
- FreeSurfer (v7)
- Python standard libraries:
  - `os`
  - `subprocess`
  - `json`
  - `argparse`

## Usage Example
```python
# Initialize processor
processor = Multiscaleatlas(
    t1="/path/to/t1.nii.gz",
    subjectID="sub-001",
    output_dir="/path/to/output"
)

# Run full reconstruction
processor.recon_all()

# Process specific scale
processor.lausanne2018scale1()

# Move results to output directory
processor.move_output()
```

## Notes
1. Requires FreeSurfer to be properly installed and configured
2. Environment variables are loaded from `setup_environment.json`
3. All scales (1-5) of the Lausanne 2018 atlas are supported
4. Output includes both surface (.annot) and volumetric (.mgz, .nii.gz) formats

## Output Directory Structure
```
subject_id/
├── label/
│   ├── lh.lausanne2018.scale*.annot
│   └── rh.lausanne2018.scale*.annot
├── stats/
│   ├── lh.lausanne2018.scale*.stats
│   └── rh.lausanne2018.scale*.stats
└── mri/
    ├── lausanne2018.scale*.mgz
    └── lausanne2018.scale*.nii.gz
```
Where * represents scales 1 through 5.