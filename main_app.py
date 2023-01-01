import numpy as np
import streamlit as st
from PIL import Image


def to_binary(im: np.ndarray, threshold: float):
    bin_im = im.copy()
    bin_im[im >= threshold] = 1
    bin_im[im < threshold] = 0
    return bin_im


def calc_black_percent(bin_im: np.ndarray):
    return 1 - bin_im.sum() / bin_im.size


def get_black_area(im, bin_threshold):
    im = np.asarray(Image.open(im).convert('L'))
    im = (im.max() - im) / (im.max() - im.min())
    bin_input = to_binary(im, bin_threshold)
    black_area = bin_input.size - bin_input.sum()
    return black_area, bin_input


def show_black_area_data(im_file, threshold, st_col, im_name):
    black_area, bin_im = get_black_area(im_file, threshold)
    st_col.subheader(f"binary image - {im_name}")
    st_col.image(bin_im)
    st_col.title(f"black Area in {im_name} (pixels)  = {black_area}")
    return black_area, bin_im


if __name__ == '__main__':
    threshold_for_binary = st.number_input("Threshold value", min_value=0., max_value=1., step=0.1, value=0.5)
    all_cell_im = st.file_uploader("Upload your ALL CELL image")
    scar_image = st.file_uploader("Upload your SCAR image")
    if all_cell_im and scar_image:
        col1, col2 = st.columns(2)
        all_cell_area, all_cell_bin_im = show_black_area_data(all_cell_im,
                                                              threshold_for_binary,
                                                              col1,
                                                              "ALL CELL")
        scar_area, scar_bin_im = show_black_area_data(scar_image,
                                                      threshold_for_binary,
                                                      col2,
                                                      "SCAR")
        scar_percent = scar_area / all_cell_area
        st.title(f"Scar percent: {scar_percent*100:.3f}%")
        st.title(f"Scar number {scar_area}")
