import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
import Functions as functions


def partAsubA():
    # Defining list of projection angles
    projection_angles = np.arange(0, 180, 3)

    # Calculating forward projection
    sinogram = functions.forward_transform(image, projection_angles)

    # Calculating unfiltered back projection
    back_projection = functions.back_projection(sinogram, projection_angles, filtering=False)

    # Calculating filtered back projection
    filtered_back_projection = functions.back_projection(sinogram, projection_angles, filtering=True)

    # Printing Reconstruction Results
    print('Back Projection RRMSE: {}'.format(round(functions.rrmse(image, back_projection), 5)))
    print('Filtered Back Projection RRMSE: {}'.format(round(functions.rrmse(image, filtered_back_projection), 5)))

    plt.figure(num='Image, it\'s Radon Transform and Back Projection', figsize=(16.0, 10.0))
    plt.suptitle('SheppLogan256', fontsize=18, fontweight='bold')
    plt.get_current_fig_manager().full_screen_toggle()
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(2, 2, 2)
    plt.title(r'Original Image: $f(x, y)$')
    plt.imshow(image,
               cmap='gray',
               aspect='equal',
               extent=(-1 * image.shape[1] // 2,
                       image.shape[1] // 2,
                       -1 * image.shape[0] // 2,
                       image.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.subplot(1, 2, 1)
    plt.title(r'Forward Projection / Radon Transform: $\mathcal{R}f(t, \theta) = h(t, \theta)$')
    plt.imshow(sinogram,
               cmap='gray',
               aspect=0.1,
               extent=(0,
                       sinogram.shape[1],
                       sinogram.shape[0] // 2,
                       -1 * sinogram.shape[0] // 2)
               )
    plt.xlabel(r'$- \theta \rightarrow$')
    plt.ylabel(r'$\leftarrow t -$')
    plt.colorbar()

    plt.subplot(2, 2, 4)
    plt.title(r'Back Projection: $\mathcal{BR}f(x, y) = \mathcal{B}h(x, y)$')
    plt.imshow(back_projection,
               cmap='gray',
               aspect='equal',
               extent=(-1 * back_projection.shape[1] // 2,
                       back_projection.shape[1] // 2,
                       -1 * back_projection.shape[0] // 2,
                       back_projection.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.savefig(os.path.join(results_folder_path, 'Question 1a1.png'))
    plt.show()


def partAsubB():
    # Defining list of projection angles
    projection_angles = np.arange(0, 180, 3)

    for filter_type in functions.FILTER_TYPES:
        for bandlimit in functions.BANDLIMITS:

            # Calculating forward projection
            sinogram = functions.forward_transform(image, projection_angles)

            # Calculating FFT
            fft = np.fft.fft(sinogram, axis=0)

            # Filtering in Frequency Domain
            fourier_filter = functions.myFilter(fft.shape[0], filter_type=filter_type, bandlimit=bandlimit)
            filtered_fft = fourier_filter * fft

            # Calculating iFFT
            filtered_sinogram = np.real(np.fft.ifft(filtered_fft, axis=0))

            # Reconstructing
            filtered_back_projection = functions.back_projection(filtered_sinogram, projection_angles, filtering=False)

            plt.figure(num='Frequency Filter: "{}" & Bandlimit (L): "{}"'.format(filter_type, bandlimit), figsize=(16, 10))
            plt.subplots_adjust(hspace=0.3)
            plt.suptitle('Frequency Filter Type: {}\nBandlimit $(L)$: {}'.format(filter_type, bandlimit), fontsize='18', fontweight='bold')

            plt.subplot(2, 2, 1)
            plt.title(r'Sinogram: $\mathcal{R}f(t, \theta) = h(t, \theta)$')
            plt.imshow(sinogram,
                       cmap='gray',
                       aspect=0.1,
                       extent=(0,
                               sinogram.shape[1],
                               sinogram.shape[0] // 2,
                               -1 * sinogram.shape[0] // 2)
                       )
            plt.xlabel(r'$- \theta \rightarrow$')
            plt.ylabel(r'$\leftarrow t -$')
            plt.colorbar()

            plt.subplot(2, 2, 3)
            plt.title(r'Filtered Sinogram: $\tilde{h}(t, \theta)$')
            plt.imshow(filtered_sinogram,
                       cmap='gray',
                       aspect=0.1,
                       extent=(0,
                               filtered_sinogram.shape[1],
                               filtered_sinogram.shape[0] // 2,
                               -1 * filtered_sinogram.shape[0] // 2)
                       )
            plt.xlabel(r'$- \theta \rightarrow$')
            plt.ylabel(r'$\leftarrow t -$')
            plt.colorbar()

            random_theta_idx = len(projection_angles) // 2
            plt.subplot(1, 2, 2)
            plt.title(
                r'Filtering in Frequency Domain: $|\omega| \cdot rect_L \cdot C(\omega) \cdot \mathcal{F}h(\omega, \theta); \theta=$' + str(
                    projection_angles[random_theta_idx]) + '°')
            plt.plot(np.fft.fftshift(np.fft.fftfreq(fft.shape[0])),
                     np.log(np.fft.fftshift(fft[:, random_theta_idx])),
                     'blue',
                     label='log(fft)')
            plt.plot(np.fft.fftshift(np.fft.fftfreq(fft.shape[0])),
                     np.log(np.fft.fftshift(filtered_fft[:, random_theta_idx])),
                     'green',
                     label='log(filtered_fft)')
            plt.plot(np.fft.fftshift(np.fft.fftfreq(fft.shape[0])),
                     10 * np.fft.fftshift(fourier_filter[:, 0]),
                     'red',
                     label='10 × {}'.format(filter_type))
            plt.ylim(bottom=0)
            plt.grid(axis='both', which='both')
            plt.legend()
            plt.xlabel(r'$- \omega \rightarrow$')
            plt.ylabel(r'$- \log(\mathcal{F}h(\omega, \theta)) \rightarrow$')
            plt.savefig(os.path.join(results_folder_path, 'Question 1a2 ({}) ({}) ({}).png'.format(filter_type, bandlimit, 'filtering')))

            plt.figure(num='Original Image vs Reconstructed Image', figsize=(16, 10))
            plt.suptitle('Frequency Filter Type: {}\nBandlimit $(L)$: {}'.format(filter_type, bandlimit), fontsize='18', fontweight='bold')

            plt.subplot(1, 3, 1)
            plt.title(r'Original Image: $f(x, y)$')
            plt.imshow(image,
                       cmap='gray',
                       aspect='equal',
                       extent=(-1 * image.shape[1] // 2,
                               image.shape[1] // 2,
                               -1 * image.shape[0] // 2,
                               image.shape[0] // 2)
                       )
            plt.xlabel(r'$- x \rightarrow$')
            plt.ylabel(r'$- y \rightarrow$')
            plt.colorbar()

            plt.subplot(1, 3, 2)
            plt.title(r'Reconstructed Image: $\tilde{\mathcal{B}}h(t, \theta)$')
            plt.imshow(filtered_back_projection,
                       cmap='gray',
                       aspect='equal',
                       extent=(-1 * filtered_back_projection.shape[1] // 2,
                               filtered_back_projection.shape[1] // 2,
                               -1 * filtered_back_projection.shape[0] // 2,
                               filtered_back_projection.shape[0] // 2)
                       )
            plt.xlabel(r'$- x \rightarrow$')
            plt.ylabel(r'$- y \rightarrow$')
            plt.colorbar()

            plt.subplot(1, 3, 3)
            plt.title('RRMSE={}\nAbsolute of Difference'.format(round(functions.rrmse(image, filtered_back_projection), 3)))
            plt.imshow(np.abs(image - filtered_back_projection),
                       cmap='gray',
                       aspect='equal',
                       extent=(-1 * image.shape[1] // 2,
                               image.shape[1] // 2,
                               -1 * image.shape[0] // 2,
                               image.shape[0] // 2)
                       )
            plt.xlabel(r'$- x \rightarrow$')
            plt.ylabel(r'$- y \rightarrow$')
            plt.colorbar()

            plt.savefig(os.path.join(results_folder_path, 'Question 1a2 ({}) ({}) ({}).png'.format(filter_type, bandlimit, 'reconstructing')))
            plt.show()


def partA():
    partAsubA()
    partAsubB()


def partB():
    projection_angles = np.arange(0, 180, 3)

    for sigma in [0, 1, 5]:
        if sigma == 0:
            blurred_image = image.copy()
        else:
            blurred_image = cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=sigma, sigmaY=sigma,
                                             borderType=cv2.BORDER_REPLICATE)

        # Calculating forward projection
        sinogram = functions.forward_transform(blurred_image, projection_angles)

        # Calculating FFT
        fft = np.fft.fft(sinogram, axis=0)

        # Filtering in Frequency Domain
        fourier_filter = functions.myFilter(fft.shape[0], filter_type='ram-lak', bandlimit='full')
        filtered_fft = fourier_filter * fft

        # Calculating iFFT
        filtered_sinogram = np.real(np.fft.ifft(filtered_fft, axis=0))

        # Reconstructing
        filtered_back_projection = functions.back_projection(filtered_sinogram, projection_angles, filtering=False)

        plt.figure(num='Original Image, Gaussian Blurred with Sigma = {} vs Reconstructed Image'.format(sigma), figsize=(16, 10))
        plt.suptitle(r'Blurred with Gaussian Filter with $\sigma = $ {}'.format(sigma), fontsize=18, fontweight='bold')

        plt.subplot(1, 3, 1)
        plt.title(r'$f(x, y) * G_{}(x, y)$'.format(sigma))
        plt.imshow(blurred_image,
                   cmap='gray',
                   aspect='equal',
                   extent=(-1 * blurred_image.shape[1] // 2,
                           blurred_image.shape[1] // 2,
                           -1 * blurred_image.shape[0] // 2,
                           blurred_image.shape[0] // 2)
                   )
        plt.xlabel(r'$- x \rightarrow$')
        plt.ylabel(r'$- y \rightarrow$')
        plt.colorbar()

        plt.subplot(1, 3, 2)
        plt.title(r'Reconstructed Image: $\tilde{\mathcal{B}}h(t, \theta)$')
        plt.imshow(filtered_back_projection,
                   cmap='gray',
                   aspect='equal',
                   extent=(-1 * filtered_back_projection.shape[1] // 2,
                           filtered_back_projection.shape[1] // 2,
                           -1 * filtered_back_projection.shape[0] // 2,
                           filtered_back_projection.shape[0] // 2)
                   )
        plt.xlabel(r'$- x \rightarrow$')
        plt.ylabel(r'$- y \rightarrow$')
        plt.colorbar()

        plt.subplot(1, 3, 3)
        plt.title('RRMSE={}\nAbsolute of Difference'.format(round(functions.rrmse(blurred_image, filtered_back_projection), 3)))
        plt.imshow(np.abs(blurred_image - filtered_back_projection),
                   cmap='gray',
                   aspect='equal',
                   extent=(-1 * blurred_image.shape[1] // 2,
                           blurred_image.shape[1] // 2,
                           -1 * blurred_image.shape[0] // 2,
                           blurred_image.shape[0] // 2)
                   )
        plt.xlabel(r'$- x \rightarrow$')
        plt.ylabel(r'$- y \rightarrow$')
        plt.colorbar()

        plt.savefig(os.path.join(results_folder_path, 'Question 1b (Blurred with σ={}).png'.format(sigma)))
        plt.show()


def partC():

    projection_angles = np.arange(0, 180, 3)
    sigmas = np.array([0, 1, 5])
    bandlimits = np.arange(1, np.pi * 2, 0.1)
    rrmses = np.zeros(shape=(sigmas.shape[0], bandlimits.shape[0]))

    for sigma_idx in range(len(sigmas)):
        if sigmas[sigma_idx] == 0:
            blurred_image = image.copy()
        else:
            blurred_image = cv2.GaussianBlur(image, ksize=(9, 9),
                                             sigmaX=sigmas[sigma_idx],
                                             sigmaY=sigmas[sigma_idx],
                                             borderType=cv2.BORDER_REPLICATE)

        for bandlimit_idx in range(len(bandlimits)):
            # Calculating forward projection
            sinogram = functions.forward_transform(blurred_image, projection_angles)

            # Calculating FFT
            fft = np.fft.fft(sinogram, axis=0)

            # Filtering in Frequency Domain
            fourier_filter = functions.myFilter(fft.shape[0],
                                                filter_type='ram-lak',
                                                bandlimit=bandlimits[bandlimit_idx] / (np.pi * 2))
            filtered_fft = fourier_filter * fft

            # Calculating iFFT
            filtered_sinogram = np.real(np.fft.ifft(filtered_fft, axis=0))

            # Reconstructing
            filtered_back_projection = functions.back_projection(filtered_sinogram, projection_angles, filtering=False)

            rrmses[sigma_idx, bandlimit_idx] = functions.rrmse(blurred_image, filtered_back_projection)

    plt.figure('L vs RRMSE', figsize=(16, 10))
    plt.suptitle(r'Bandlimit $(L)$ vs RRMSE', fontsize=18, fontweight='bold')

    plt.subplot(1, 3, 1)
    plt.title(r'$S_0$')
    plt.plot(bandlimits, rrmses[0], 'r-')
    plt.plot(bandlimits[::10], rrmses[0, ::10], 'ro')
    plt.xlabel(r'$L$')
    plt.ylabel('RRMSE')

    plt.subplot(1, 3, 2)
    plt.title(r'$S_1$')
    plt.plot(bandlimits, rrmses[1], 'g-')
    plt.plot(bandlimits[::10], rrmses[1, ::10], 'go')
    plt.xlabel(r'$L$')
    plt.ylabel('RRMSE')

    plt.subplot(1, 3, 3)
    plt.title(r'$S_5$')
    plt.plot(bandlimits, rrmses[2], 'b-')
    plt.plot(bandlimits[::10], rrmses[2, ::10], 'bo')
    plt.xlabel(r'$L$')
    plt.ylabel('RRMSE')

    plt.savefig(os.path.join(results_folder_path, 'Question 1c.png'))
    plt.show()


# Building important folder locations
project_folder_path = os.path.abspath('..')
code_folder_path = os.path.join(project_folder_path, 'code')
data_folder_path = os.path.join(project_folder_path, 'data')
results_folder_path = os.path.join(project_folder_path, 'results')

# Reading image
image = np.asarray(cv2.imread(os.path.join(data_folder_path, 'SheppLogan256.png'), cv2.IMREAD_GRAYSCALE),
                   dtype=np.float) / 255

partA()
partB()
partC()