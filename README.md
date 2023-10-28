# Autocrop

This script was written to crop the whitespace from images scanned by a device whose drivers or software lack built-in cropping.

The image is analyzed by row and column, and by taking the average pixel value for each, the cropping occurs where the first row and column drop below the threshold.

Given the quick-and-dirty nature of this script, and that it was written for scanned images, it makes a few assumptions that cause limitations, which are described below.

# Example

```
python3 ac.py --filename /media/assets/scan0006.jpg --threshold 252 --extra 12
```

The above will autocrop an image above the threshold of 252, and remove an additional 12 pixels.

# Usage

```
$ ./act.py --help
usage: ACT - AutoCropping Tool [-h] -f FILENAME [-t THRESHOLD] [-e EXTRA_PIXELS] [-b] [-i] [-o OUTFILE] [-l {INFO,DEBUG,ERROR,WARNING,CRITICAL,NOTSET}]

Automatically crops scanned images. Analyzes the image by rows and columns, and if the average pixel value is above the threshold, crop the remaining image. The default assumes a white area to be cropped, as if the image were scanned.
If the opposite is true, and the portion to be cropped is dark, use the --below flag and modify the threshold to be near zero. Currently, this tool only supports images starting at the top left corner (0,0), and cropping occurs to the
right of, and below the image. In a future version, this may be fixed to support cropping on all sides of the image.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Location of the image to crop
  -t THRESHOLD, --threshold THRESHOLD
                        Columns and rows above the threshold value will be cropped. A value near the max of 255 indicates a light background to be cropped, while a value near the minimum of 0 indicates a dark background. By default,
                        values above the threshold are cropped. If a dark background needs cropped, include the --below flag and set the threshold close to zero.
  -e EXTRA_PIXELS, --extra EXTRA_PIXELS
                        Crops an additional number of pixels. Useful, for example, if photo edge is visible.
  -b, --below           Crop when pixel values are below the threshold.
  -i, --in-place        Overwrite the source file
  -o OUTFILE, --outfile OUTFILE
                        Name of the cropped image. If not specified, and --in-place flag is omitted, the output filename has '_cropped' added to it and is placed in the same directory as the source file.
  -l {INFO,DEBUG,ERROR,WARNING,CRITICAL,NOTSET}, --log-level {INFO,DEBUG,ERROR,WARNING,CRITICAL,NOTSET}
                        Sets python log level.
```

# Limitations

The script assumes the image starts in the top right corner. Only the right side and bottom of the image are cropped.

Search for empty rows and columns (i.e. below threshold) stops when the first one of each is found. A better way of doing this would ensure there are no other significant rows or columns after the initial drop below threshold. However, this is more difficult than it seems because there are often dark edges on a scanner, which would result in the image not begin cropped using this method.

These problems might be solved in a future update, in a galaxy far, far away.
