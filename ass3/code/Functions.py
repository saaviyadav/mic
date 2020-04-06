import numpy as np
from skimage.transform import radon, iradon

FILTER_TYPES = ['ram-lak', 'shepp-logan', 'cosine']

BANDLIMITS = ['full', 'half']


def rrmse(original_image, reconstructed_image):
    return np.linalg.norm(original_image - reconstructed_image) / np.linalg.norm(original_image)


def forward_transform(image, projection_angles=np.arange(0, 180, 1)):
    return radon(image,
                 theta=projection_angles,
                 circle=False)


def back_projection(sinogram, projection_angles=np.arange(0, 180, 1), filtering=False):
    if filtering:
        return iradon(sinogram,
                      theta=projection_angles,
                      circle=False)
    else:
        return iradon(sinogram,
                      theta=projection_angles,
                      filter=None,
                      circle=False)


def myFilter(len, filter_type='ram-lak', bandlimit='full'):
    fft_frequencies = 2 * np.fft.fftfreq(len)
    abs_fft_frequencies = np.abs(fft_frequencies)

    if bandlimit == 'full':
        L = abs_fft_frequencies.max()
    elif bandlimit == 'half':
        L = abs_fft_frequencies.max() / 2
    else:
        L = bandlimit

    rectL = np.zeros(shape=len)
    rectL[abs_fft_frequencies <= L] = 1

    fourier_filter = np.zeros(shape=len)
    if filter_type == 'ram-lak':
        fourier_filter[1:] = abs_fft_frequencies[1:] * rectL[1:]
    elif filter_type == 'shepp-logan':
        fourier_filter[1:] = abs_fft_frequencies[1:] * rectL[1:] * \
                             np.sin((np.pi * fft_frequencies[1:]) / (2 * L)) / ((np.pi * fft_frequencies[1:]) / (2 * L))
    else:
        fourier_filter[1:] = abs_fft_frequencies[1:] * rectL[1:] * \
                             np.cos((np.pi * fft_frequencies[1:]) / (2 * L))

    return fourier_filter[:, np.newaxis]