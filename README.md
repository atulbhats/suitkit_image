# SUIT Co aligne full disc images
--------
- Co align SUIT 2k images using image cross corellation method.
- Pakage will produce the coaligned images and movie for the PR purposes.
- Will return the csv file of shift value applied for each image.
- Aligned FITS image can can also be produced.
- co align ROIs (will be added soon)

## Usage
Pull this github repository along with dependency files.

import suit_co_align_imgs.suit_co_align_fd_imgs

search_fold = 'path/to/2k/images/directory'
filter_name = 'NB03' # or 'NB04' ,  based on the availablity
logo_paths = {
        "logo1": 'path/to/suit_white.png',
        "logo2": 'path/to/sun_iucaa.png',
        "logo3": 'path/to/iucaaisro.png'
    }

###### Optional parameters
batch_size=10  #default is 10
rate=30 #set the framerate of the output video
ref_idx=0 #Template index in sorted array for the cross corellation
Test_mode=False , if True, consider slice of array, will get you the sample output for the images between images of index start_idx to end_idx
start_idx=0
end_idx=11

