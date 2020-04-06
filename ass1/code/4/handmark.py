from matplotlib import pyplot as plt
import os
import csv

data_folder_path = os.path.abspath(os.path.join('..', 'data', 'leaf'))
csvs_folder_path = os.path.abspath(os.path.join(data_folder_path, 'csv'))
images_folder_path = os.path.abspath(os.path.join(data_folder_path, 'data'))

if not os.path.isdir:
    os.mkdir(csvs_folder_path)

def onclick(event):
    global x_idxes, y_idxes
    global h1

    x_idx, y_idx = event.xdata, event.ydata

    if x_idx == None or y_idx == None:
        return

    x_idxes.append(x_idx)
    y_idxes.append(y_idx)

    print(x_idx, y_idx)
    print(len(x_idxes), len(y_idxes))

    hl.set_xdata(x_idxes)
    hl.set_ydata(y_idxes)

    plt.draw()

for image_file_name in os.listdir(images_folder_path):
    image_file_path = os.path.join(images_folder_path, image_file_name)
    image_number = image_file_name.split(sep='.')[0]
    image = plt.imread(image_file_path)

    x_idxes = []
    y_idxes = []

    fig = plt.figure(figsize=(20, 20), num=image_file_path)
    plt.imshow(image)
    hl, = plt.plot([], [], 'ro-')
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    fig.canvas.mpl_disconnect(cid)

    with open(os.path.join(csvs_folder_path, 'Points {}.csv'.format(image_number)), 'w', newline='') as file:
        csv_file = csv.writer(file)
        for i in range(len(x_idxes)):
            csv_file.writerow([round(x_idxes[i], 3), round(y_idxes[i], 3)])