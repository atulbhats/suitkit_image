'''
Created on 2 June 2024

@Author: Adithya H.N.

Modification History:

- Variable to toggle Logo. 16 Jul 2024 - @atulbhats

'''

import os
import matplotlib.pyplot as plt
import astropy.units as u
import sunpy.map
import glob
import datetime
from sunkit_image.coalignment import calculate_match_template_shift, apply_shifts
from datetime import timedelta
import timeit
import pathlib
from colormap import filterColor
from astropy.coordinates import SkyCoord, SkyOffsetFrame
import numpy as np
from PIL import Image
import ImagesToMovie_pkg

def suit_co_align_fd_imgs(search_fold,filter_name,add_logos,batch_size=10,rate=30,ref_idx=0,Save_fits=False,test_mode=False,start_idx=0,end_idx=21):
    global base_fold
    start = timeit.default_timer()
    now = datetime.datetime.now() - timedelta(days=1)
    print("Starting up now: ", datetime.datetime.now())
    print(f'Searching for {filter_name} images in {search_fold} folder')
    #print('Path: ',os.getcwd())
    base_fold=os.getcwd()
    Fetch and sort files
    files = get_sorted_files(search_fold, filter_name)
    if test_mode:
        files=files[start_idx:end_idx]
    print('Total files:', len(files))

    ref_img = sunpy.map.Map(files[0])
    ref_submap = get_submap(ref_img)

    # Create directories
    fl_date = datetime.datetime.fromisoformat(str(ref_img.date))
    fol_nm, jpg_fold, algn_dir = create_directories(fl_date,Save_fits)

    o_x, o_y, o_d, od, x_arry, y_arry, aln_imgs = [], [], [], [], [], [], []

    for i in range(0, len(files), batch_size):
        batch_files = [files[0]] + files[i:i + batch_size]
        batch_results = process_batch(batch_files, ref_submap, add_logos, jpg_fold,Save_fits,algn_dir)
        o_x.extend(batch_results[0])
        o_y.extend(batch_results[1])
        o_d.extend(batch_results[2])
        od.extend(batch_results[3])
        x_arry.extend(batch_results[4])
        y_arry.extend(batch_results[5])
        aln_imgs.extend(batch_results[6])

    # Save results and create movie
    save_results(fl_date, o_x, o_y, o_d, x_arry, y_arry, aln_imgs)
    create_movie(jpg_fold, fl_date,rate)

    stop = timeit.default_timer()
    print('Done bro, Time: ', datetime.datetime.now())
    print('Run Time: ', (stop - start) / 60, 'Mins')

def get_sorted_files(search_fold, filter_name):
    fdir = search_fold 
    files = glob.glob(fdir + f'*2{filter_name}.fits')
    files = sorted(files, key=lambda file_name: datetime.datetime.strptime(os.path.basename(file_name).split('_')[5], "%Y-%m-%dT%H.%M.%S.%f"))
    return files

def get_submap(ref_img):
    #top_right = SkyCoord(550 * u.arcsec, 1050 * u.arcsec, frame=ref_img.coordinate_frame)
    #bottom_left = SkyCoord(-700 * u.arcsec, 850 * u.arcsec, frame=ref_img.coordinate_frame)
    center_coord = SkyCoord(0 * u.arcsec, 950* u.arcsec, frame=ref_img.coordinate_frame) #54,157
    width = 1100 * u.arcsec
    height =300 * u.arcsec   
    
    ref_img.meta.update({'CROTA2':0})
    #print('rot',ref_img.meta.get('CROTA2')) 
    offset_frame = SkyOffsetFrame(origin=center_coord, rotation=0*u.deg)
    rectangle = SkyCoord(lon=[-1/2, 1/2] * width, lat=[-1/2, 1/2] * height, frame=offset_frame)
    ref_submap = ref_img.submap(rectangle) #bottom_left, top_right=top_right)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection=ref_submap)
    ref_submap.plot(axes=ax)
    
    plt.savefig('Template.jpg')
    #plt.show()
    plt.close()
    
    return ref_submap

def create_directories(fl_date,Save_fits):
    fol_nm = f'{base_fold}/{str(fl_date.day).zfill(2)}_{str(fl_date.month).zfill(2)}_{str(fl_date.year).zfill(2)}'
    jpg_fold = f'{fol_nm}/FD_imgs'
    video_fold=f'{base_fold}/Website_Movies'
    algn_dir = f'{fol_nm}/Aligned_Fits'
    
    pathlib.Path(jpg_fold).mkdir(parents=True, exist_ok=True)
    
    pathlib.Path(video_fold).mkdir(parents=True, exist_ok=True)
    if Save_fits:
        pathlib.Path(algn_dir).mkdir(parents=True, exist_ok=True)

    
    return fol_nm, jpg_fold, algn_dir

def process_batch(files, ref_submap, add_logos, jpg_fold,Save_fits,algn_dir):
    o_x, o_y, o_d, od, x_arry, y_arry, aln_imgs = [], [], [], [], [], [], []
    ref_head=ref_submap.fits_header
    ref_cdel=ref_head['CDELT1']

    Sequence = sunpy.map.Map(files, sequence=True)
    for l in range(len(Sequence) - 1):
        o_x.append(Sequence[l + 1].meta.get('CRPIX1'))
        o_y.append(Sequence[l + 1].meta.get('CRPIX2'))
        o_d.append(datetime.datetime.fromisoformat(str(Sequence[l + 1].date)))
        od.append(str(Sequence[l + 1].date))

    align_shift = calculate_match_template_shift(Sequence, template=ref_submap)
    x_arry.extend(align_shift['x'].value[1:] / ref_cdel * -1)  # avoiding the inserted image data
    y_arry.extend(align_shift['y'].value[1:] / ref_cdel * -1)
    shift_xPix = align_shift['x'].value / ref_cdel * -1
    shift_yPix = align_shift['y'].value / ref_cdel * -1

    aligned_maps = apply_shifts(Sequence, yshift=shift_yPix * u.pixel, xshift=shift_xPix * u.pixel, clip=False)
    for k in range(len(aligned_maps) - 1):  # account for inserted image, j=0 is reference image
        j = k + 1
        img_head = aligned_maps[j].fits_header
        img_head['CRPIX1'] = ref_head['CRPIX1'] + shift_xPix[j]
        img_head['CRPIX2'] = ref_head['CRPIX2'] + shift_yPix[j]

        # Image enhancement
        limb_enh_data = enhance_image(aligned_maps[j], img_head)
        aligned_img = sunpy.map.Map(aligned_maps[j].data, img_head)
        if Save_fits:
            fits_fnm=f'{algn_dir}/{os.path.basename(files[j])}'
            aligned_img.save(fits_fnm,overwrite=True)

        aln_imgs.append(os.path.basename(files[j]))  # element is added to sequence not original file list so k is correct than j
        fl_nm = f'{jpg_fold}/{os.path.basename(files[j])[:-4]}jpg'
        save_image(aligned_img, add_logos, fl_nm)

    return o_x, o_y, o_d, od, x_arry, y_arry, aln_imgs

def enhance_image(aligned_map, img_head):
    off_limb_len = 100  # pixels beyond off limb
    amp = 10  # off disk amplification factor
    h, w = aligned_map.data.shape
    col, row, radius = img_head['CRPIX1'] - 3, img_head['CRPIX2'] - 4, img_head['R_SUN']
    mask = np.ones((h, w)) * create_circular_mask(h, w, col, row, radius)
    mask = np.where(mask < 1, amp, mask)  # contains amplification factor (amp) for off disk feature
    offdisk = aligned_map.data * mask
    outermask = np.ones((h, w)) * create_circular_mask(h, w, col, row, radius + off_limb_len)  # controls the size of outer mask
    limb_enh_data = offdisk * outermask
    return limb_enh_data

def create_circular_mask(h, w, col, row, radius):
    '''
    Creates circular mask of desired size.
    - h, w: height and width of canvas
    - col, row: column and row of circle center
    - radius: radius of circle
    '''
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - col) ** 2 + (Y - row) ** 2)
    mask = dist_from_center <= radius
    return mask

def save_image(aligned_img, add_logos, fl_nm):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection=aligned_img)
    aligned_img.plot(title=False, cmap=filterColor['NB03'], vmin=np.percentile(aligned_img.data,1), vmax=np.percentile(aligned_img.data, 99.5))
    plot_str = str(aligned_img.date) + '          ' + 'NB03 Mg II k 279 nm'
    
    if add_logos == 1:
        logo_paths = {
            #Picking Up Relevant Logos.
            "logo1": '/assets/suit_white.png',
            "logo2": '/assets/sun_iucaa.png',
            "logo3": '/assets/iucaaisro.png'
        }
        logo_image3 = Image.open(logo_paths['logo3'])  # suit_logo, top left
        logo_image2 = Image.open(logo_paths['logo2'])  # sun at iucaa top right
        logo_image1 = Image.open(logo_paths['logo1'])  # suitlogo bottom right

        logo_image3 = logo_image3.resize((100, 76))  # Adjust the size as needed
        logo_image2 = logo_image2.resize((53, 53))
        logo_image1 = logo_image1.resize((73, 50))

        logo_image1 = np.array(logo_image1)
        logo_image2 = np.array(logo_image2)
        logo_image3 = np.array(logo_image3)

        fig.figimage(logo_image1, xo=880, yo=20, zorder=3, alpha=1)
        fig.figimage(logo_image2, xo=890, yo=890, zorder=3, alpha=1)
        fig.figimage(logo_image3, xo=12, yo=880, zorder=3, alpha=1)

    ax.text(50, 50, plot_str, color='white', weight='bold', fontsize=18)

    plt.draw()
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.tight_layout()
    plt.savefig(fl_nm, bbox_inches='tight', transparent="True", pad_inches=0)
    plt.close()

def save_results(fl_date, o_x, o_y, o_d, x_arry, y_arry, aln_imgs):
    data = np.column_stack((aln_imgs, o_d, x_arry, y_arry, o_x, o_y))
    months = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    output_file = f'{base_fold}/{months[int(fl_date.month)]}{str(fl_date.day).zfill(2)}_1.1fits_Jitter_shift.csv'
    np.savetxt(output_file, data, delimiter=',', header='File names, Date, delX, delY, CR-X, CR-Y', fmt='%s')

def create_movie(jpg_fold, fl_date,rate=30):
    months = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    dat_dir=jpg_fold+'/'
    shiftFile=f'{base_fold}/'+f'{months[int(fl_date.month)]}{str(fl_date.day).zfill(2)}_1.1fits_Jitter_shift.csv'
    ImagesToMovie_pkg.Filter_imgs(shiftFile,dat_dir)
    movie_name = f'{base_fold}/Website_Movies/{months[int(fl_date.month)]}{str(fl_date.day).zfill(2)}_1.1_movie.mp4'
    ImagesToMovie_pkg.Make_movie(jpg_fold, movie_name, rate)

if __name__ == "__main__":
    search_fold = '/path/to/2k_images/'  # Custom Folder
    filter_name = 'NB03'
    add_logos = 1
    
    '''
    # Other Optional parameters

    batch_size=10
    rate=30
    ref_idx=0 # Template index in sorted array
    test_mode=False , if True, consider slice of array
    start_idx=0
    end_idx=11
    '''

    suit_co_align_fd_imgs(search_fold,filter_name,add_logos)
