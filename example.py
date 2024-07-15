import git_suit_co_align_imgs

search_fold = '/scratch/suit_data/level1fits/2024/06/03/normal_2k/'  # Custom Folder
filter_name = 'NB03'
logo_paths = {
        "logo1": '/data/sreejith/MCNS_POC/Daily_Movies/suit_white.png',
        "logo2": '/data/sreejith/MCNS_POC/Daily_Movies/sun_iucaa.png',
        "logo3": '/data/sreejith/MCNS_POC/Daily_Movies/iucaaisro.png'}

#testmode
#git_suit_co_align_imgs.suit_co_align_fd_imgs(search_fold,filter_name,logo_paths,Test_mode=True,start_idx=0,end_idx=31)
#common usage
git_suit_co_align_imgs.suit_co_align_fd_imgs(search_fold,filter_name,logo_paths)