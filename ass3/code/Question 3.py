import numpy as np
import Functions as functions
import os
import cv2
import math
from skimage.transform import radon, iradon
from matplotlib import pyplot as plt

def partA():
    starting_angles = np.arange(0, 180, 0.5)
    rrmses1 = np.zeros_like(starting_angles, dtype=np.float)
    rrmses2 = np.zeros_like(starting_angles, dtype=np.float)
    for idx in range(len(starting_angles)):
        projection_angles = np.arange(starting_angles[idx], starting_angles[idx] + 150, 1)
        sinogram1 = radon(image1, theta=projection_angles, circle=False)
        sinogram2 = radon(image2, theta=projection_angles, circle=False)
        filtered_back_projection1 = iradon(sinogram1, projection_angles, circle=False)
        filtered_back_projection2 = iradon(sinogram2, projection_angles, circle=False)
        rrmses1[idx] = functions.rrmse(image1, filtered_back_projection1)
        rrmses2[idx] = functions.rrmse(image2, filtered_back_projection2)

    optimal_theta1 = starting_angles[rrmses1.argmin()]
    min_rrmse1 = rrmses1.min()
    optimal_theta2 = starting_angles[rrmses2.argmin()]
    min_rrmse2 = rrmses2.min()

    print('For ChestCT Image,\n\tMinimum RRMSE = {}, achieved at starting theta = {}°'.format(round(min_rrmse1, 3), optimal_theta1))
    print('For SheppLogan256 Image,\n\tMinimum RRMSE = {}, achieved at starting theta = {}°'.format(round(min_rrmse2, 3), optimal_theta2))

    plt.figure('RRMSE vs Starting Angles', figsize=(16.0, 10.0))

    plt.subplot(1, 2, 1)
    plt.title('ChestCT Image', fontweight='bold')
    plt.plot(starting_angles[::2], rrmses1[::2], 'r-')
    plt.plot(optimal_theta1, min_rrmse1, 'go')
    text_coordinates = (0,
                        plt.ylim()[1] - (plt.ylim()[1] - plt.ylim()[0]) / 10)
    plt.text(x=text_coordinates[0],
             y=text_coordinates[1],
             s=r'RRMSE: {}'.format(round(min_rrmse1, 3)) + '\n' + r'Corresponding $\theta: {}\degree$'.format(optimal_theta1),
             bbox=dict(facecolor='white', alpha=0.5))
    plt.xlabel(r'$- \theta_{start} \rightarrow$')
    plt.ylabel(r'$-$ RRMSE $\rightarrow$')
    plt.grid(axis='both', which='both')

    plt.subplot(1, 2, 2)
    plt.title('SheppLogan256 Image', fontweight='bold')
    plt.plot(starting_angles[::2], rrmses2[::2], 'r-')
    plt.plot(optimal_theta2, min_rrmse2, 'go')
    text_coordinates = (100,
                        plt.ylim()[1] - (plt.ylim()[1] - plt.ylim()[0]) / 10)
    plt.text(x=text_coordinates[0],
             y=text_coordinates[1],
             s=r'RRMSE: {}'.format(round(min_rrmse2, 3)) + '\n' + r'Corresponding $\theta: {}\degree$'.format(optimal_theta2),
             bbox=dict(facecolor='white', alpha=0.5))
    plt.xlabel(r'$- \theta_{start} \rightarrow$')
    plt.ylabel(r'$-$ RRMSE $\rightarrow$')
    plt.grid(axis='both', which='both')
    plt.savefig(os.path.join(results_folder_path, 'Question 3a.png'))

    plt.show()

def partB():
    starting_angles = np.arange(0, 180, 0.5)
    rrmses1 = np.zeros_like(starting_angles, dtype=np.float)
    rrmses2 = np.zeros_like(starting_angles, dtype=np.float)
    for idx in range(len(starting_angles)):
        projection_angles = np.arange(starting_angles[idx], starting_angles[idx] + 150, 1)
        sinogram1 = radon(image1, theta=projection_angles, circle=False)
        sinogram2 = radon(image2, theta=projection_angles, circle=False)
        filtered_back_projection1 = iradon(sinogram1, projection_angles, circle=False)
        filtered_back_projection2 = iradon(sinogram2, projection_angles, circle=False)
        rrmses1[idx] = functions.rrmse(image1, filtered_back_projection1)
        rrmses2[idx] = functions.rrmse(image2, filtered_back_projection2)

    optimal_theta1 = starting_angles[rrmses1.argmin()]
    optimal_theta2 = starting_angles[rrmses2.argmin()]
    projection_angles1 = np.arange(optimal_theta1, optimal_theta1 + 150, 1)
    projection_angles2 = np.arange(optimal_theta2, optimal_theta2 + 150, 1)
    sinogram1 = radon(image1, theta=projection_angles1, circle=False)
    sinogram2 = radon(image2, theta=projection_angles2, circle=False)
    filtered_back_projection1 = iradon(sinogram1, projection_angles1, circle=False)
    filtered_back_projection2 = iradon(sinogram2, projection_angles2, circle=False)


    plt.figure(num='ChestCT')
    plt.suptitle('ChestCT', fontsize=26, fontweight='bold')

    plt.subplot(1, 3, 1)
    plt.title(r'Original Image: $f(x, y)$')
    plt.imshow(image1,
               cmap='gray',
               aspect='equal',
               extent=(-1 * image1.shape[1] // 2,
                       image1.shape[1] // 2,
                       -1 * image1.shape[0] // 2,
                       image1.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.title(r'Reconstructed Image: $\tilde{\mathcal{B}}h(t, \theta)$')
    plt.imshow(filtered_back_projection1,
               cmap='gray',
               aspect='equal',
               extent=(-1 * filtered_back_projection1.shape[1] // 2,
                       filtered_back_projection1.shape[1] // 2,
                       -1 * filtered_back_projection1.shape[0] // 2,
                       filtered_back_projection1.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.subplot(1, 3, 3)
    plt.title('RRMSE={}\nAbsolute of Difference'.format(round(functions.rrmse(image1, filtered_back_projection1), 3)))
    plt.imshow(np.abs(image1 - filtered_back_projection1),
               cmap='gray',
               aspect='equal',
               extent=(-1 * filtered_back_projection1.shape[1] // 2,
                       filtered_back_projection1.shape[1] // 2,
                       -1 * filtered_back_projection1.shape[0] // 2,
                       filtered_back_projection1.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()
    plt.savefig(os.path.join(results_folder_path, 'Question 3b (ChestCT).png'))


    plt.figure(num='SheppLogan256')
    plt.suptitle('SheppLogan256', fontsize=26, fontweight='bold')

    plt.subplot(1, 3, 1)
    plt.title(r'Original Image: $f(x, y)$')
    plt.imshow(image2,
               cmap='gray',
               aspect='equal',
               extent=(-1 * image2.shape[1] // 2,
                       image2.shape[1] // 2,
                       -1 * image2.shape[0] // 2,
                       image2.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.title(r'Reconstructed Image: $\tilde{\mathcal{B}}h(t, \theta)$')
    plt.imshow(filtered_back_projection2,
               cmap='gray',
               aspect='equal',
               extent=(-1 * filtered_back_projection2.shape[1] // 2,
                       filtered_back_projection2.shape[1] // 2,
                       -1 * filtered_back_projection2.shape[0] // 2,
                       filtered_back_projection2.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.subplot(1, 3, 3)
    plt.title('RRMSE={}\nAbsolute of Difference'.format(round(functions.rrmse(image2, filtered_back_projection2), 3)))
    plt.imshow(np.abs(image2 - filtered_back_projection2),
               cmap='gray',
               aspect='equal',
               extent=(-1 * filtered_back_projection2.shape[1] // 2,
                       filtered_back_projection2.shape[1] // 2,
                       -1 * filtered_back_projection2.shape[0] // 2,
                       filtered_back_projection2.shape[0] // 2)
               )
    plt.xlabel(r'$- x \rightarrow$')
    plt.ylabel(r'$- y \rightarrow$')
    plt.colorbar()

    plt.savefig(os.path.join(results_folder_path, 'Question 3b (SheppLogan256).png'))
    plt.show()


# Building important folder locations
project_folder_path = os.path.abspath('..')
code_folder_path = os.path.join(project_folder_path, 'code')
data_folder_path = os.path.join(project_folder_path, 'data')
results_folder_path = os.path.join(project_folder_path, 'results')

# Reading image
image1 = np.asarray(cv2.imread(os.path.join(data_folder_path, 'ChestCT.png'), cv2.IMREAD_GRAYSCALE),
                   dtype=np.float) / 255
image2 = np.asarray(cv2.imread(os.path.join(data_folder_path, 'SheppLogan256.png'), cv2.IMREAD_GRAYSCALE),
                   dtype=np.float) / 255

partA()
partB()