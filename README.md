![](Assests/suit_github.png)
## SUIT Co-Align Full Disc Images

This package is designed to co-align SUIT 2k images using the image cross-correlation method. It produces co-aligned images and movies for PR purposes and returns a CSV file with the shift values applied to each image. Additionally, aligned FITS images can be produced.

### Features

- **Co-alignment**: Co-align SUIT 2k images using the cross-correlation method.
- **Outputs**:
  - Co-aligned images.
  - Movies for PR purposes.
  - CSV file of shift values applied for each image.
  - Option to produce aligned FITS images.
#### **Under Development**: 
- Co-alignment for ROIs (Region of Interests) will be added soon.
- Flux conserved Image Rotation
- Drift correction for ROIs
- NB03 Difference movie
- Compare L1 images to Earth observer frame

## Installation

Pull this GitHub repository along with the required dependency files.

## Usage

```python
import suitkit_image.suit_co_align_fd_imgs

# Set the directory containing the 2k images
search_fold = 'path/to/2k/images/directory'

# Specify the filter name ('NB03' or 'NB04' based on availability)
filter_name = 'NB03'

# Define paths to logo images
logo_paths = {
    "logo1": 'path/to/suit_white.png',
    "logo2": 'path/to/sun_iucaa.png',
    "logo3": 'path/to/iucaaisro.png'
}

# Call the main function to start the co-alignment process
suit_co_align_fd_imgs.main(
    search_fold=search_fold,
    filter_name=filter_name,
    logo_paths=logo_paths,
    batch_size=10,   # Optional: default is 10
    rate=30,        # Optional: set the frame rate of the output video
    ref_idx=0,      # Optional: Template index in the sorted array for cross-correlation
    Test_mode=False, # Optional: If True, processes a slice of the array for testing
    start_idx=0,    # Optional: Start index for test mode
    end_idx=11      # Optional: End index for test mode
)
```

### Authors
- Adithya H. N.
- Sreejith P.

### Contact
- *Adithyabhattsringeri@gmail.com*
