"""Image processing calculations for Local Entropy for event detected images"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import csv
import argparse

# Function to convert rgb to grayscale image
def rgb2gray(rgb):
    # If rgb = (1,0,0), (0,1,0) or (0,0,1)
    return np.dot(rgb[...,:3], [255*0.2989, 255*0.5870, 255*0.1140])
    # If rgb = (255,0,0), (0,255,0) or (0,0,255)
    # return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


# Function to calculate entropy
def entropy(signal):

    # Returns entropy of a signal - signal must be a 1-D numpy array
    lensig = signal.size
    symset = list(set(signal))
    propab = [np.size(signal[signal == i]) / (1.0 * lensig) for i in symset]
    ent = np.sum([p * np.log2(1.0 / p) for p in propab])
    return ent


# Main function
def main():
    
    print("\n*** Starting Entropy Calculation ***")
    print("\n")

    entropy_dict = {}
    
    for image_path in os.listdir(args.imagePath):
        image = os.path.join(args.imagePath, image_path)
        im_frame = mpimg.imread(image)
        gray = rgb2gray(im_frame)

        N = 5
        S = gray.shape
        E = np.array(gray)
        for row in range(S[0]):
                for col in range(S[1]):
                        Lx=np.max([0,col-N])
                        Ux=np.min([S[1],col+N])
                        Ly=np.max([0,row-N])
                        Uy=np.min([S[0],row+N])
                        region=gray[Ly:Uy,Lx:Ux].flatten()
                        E[row,col]=entropy(region)
        entropy_sum = E.sum()

        entropy_dict[image_path] = entropy_sum
        
        if args.saveImg:
            # Save the entropy images
            full_path_img = os.path.join(args.outputPath, f'LocalEntropy_img_{image_path}')
            plt.imsave(full_path_img, E, cmap='viridis')

        if args.savePlot:
            # Save the entropy figures
            fig, (ax0) = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
            ax0.imshow(E, cmap='viridis')
            ax0.set_title("Local entropy Image, Entropy=" + str(round(entropy_sum, 3)), fontsize=10)
            plt.colorbar(ax0.imshow(E, cmap='viridis'), ax=ax0, fraction=0.046, pad=0.04)
            full_path_fig = os.path.join(args.outputPath, f'LocalEntropy_fig_{image_path}')
            fig.savefig(full_path_fig, bbox_inches="tight")
            plt.close(fig)

    if args.saveEntropyData:
        # Save csv with local entropy values of each image
        full_csv_path = os.path.join(args.outputPath, f'LocalEntropy_data_{os.path.basename(os.path.normpath(args.outputPath))}.csv')

        with open(full_csv_path, 'w', newline='') as csv_file:
            csv_file.write('File Name, Local Entropy\n')
            for key,val in entropy_dict.items():
                csv_file.write(f'{key},{val}\n')

    print("\n*** Entropy Calculation Ended***")

if __name__ == "__main__":
    # Get command line args
    parser = argparse.ArgumentParser(
        description="Entropy Calculation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image_path", dest="imagePath", type=str,
        help="Path where the image to be processed are")
    parser.add_argument("--output_path", dest="outputPath", type=str,
        help="Path where the image after processing is to be saved to")
    parser.add_argument("--save_img", dest="saveImg", action='store_true',
        help="Save image without plot information")
    parser.add_argument("--exclude_plot", dest="savePlot", action='store_false',
        help="Save image with plot information")
    parser.add_argument("--save_entropy_data", dest="saveEntropyData", action='store_true',
        help="Save entropy data for each image in a CSV")
    args = parser.parse_args()

    main()