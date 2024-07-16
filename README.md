![](assets/suit_header.png)
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
search_fold = 'path/to/2k_images/'

# Specify the filter ('NB03' or 'NB04' based on availability)
filter_name = 'NB03'  # # For More Info on various Filters, refer https://suit.iucaa.in

# Call the main function to start the co-alignment process
suit_co_align_fd_imgs.main(
    search_fold=search_fold,
    filter_name=filter_name,
    add_logos=1         # Optional: Display Logos / default is 1 
    batch_size=10,      # Optional: Number of Images to be used for aligngs / default is 10
    rate=30,            # Optional: Frame rate for Output video. [fps]
    ref_idx=0,          # Optional: Template index in the sorted array for cross-correlation
    Test_mode=False,    # Optional: If True, processes a slice of the array for testing
    start_idx=0,        # Optional: Start index for test mode
    end_idx=11          # Optional: End index for test mode
)
```

### Authors
- Adithya H. N. (@adithya-hn)
- Sreejith Padinhatteeri (@sreejithpa)
- Atul Bhat (@atulbhats)

### Contact
- [adithyabhattsringeri@gmail.com](mailto:adithyabhattsringeri@gmail.com)
