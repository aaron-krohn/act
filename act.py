#!/usr/bin/env python3

import os
import sys
import logging
import argparse

from PIL import Image, ImageMath
import numpy as np


def autocrop(infile, outfile, threshold=245, below=False, extra=0):
    """The assumption is that scanned images have a picture component and a uniformly
       colored area that is not the picture. Perhaps it's the underside of the scanner
       bed lid.

       By determining the average color of each row and column, we should be able to
       make a good guess about where the corner of the photo is.

       It is assumed that the photos are placed in the corner of the scan bed, and as
       such, only two sides of the image will need cropped.
    """

    logging.info('Opening image %s', infile)
    with Image.open(infile) as im:

        im_data = im.getdata()
        im_width = im.size[0]
        im_height = im.size[1]

    logging.info('Processing image')
    idata = np.array(im_data).reshape(im_height, im_width, 3)
    logging.debug('Loaded image with dimensions %s', idata.shape)

    for hidx, hpx in enumerate(idata.mean(axis=(1,2))):
        if hpx > threshold:
            break

    for widx, wpx in enumerate(idata.mean(axis=(0,2))):
        if wpx > threshold:
            break

    logging.debug('Cropping to size %s, %s', (widx - extra), (hidx - extra))

    # Maybe silly, but this way, the file isn't open while doing calculations
    with Image.open(infile) as im:
        try:
            cropped = im.crop((0, 0, (widx - extra), (hidx - extra)))
        except ValueError:
            logging.error('Crop failed, skipping image')
            return False

    logging.info('Writing cropped image to %s', outfile)
    cropped.save(outfile)

    return True


def init_args():

    parser = argparse.ArgumentParser(
            prog='ACT - AutoCropping Tool',
            description='Automatically crops scanned images. Analyzes the image by rows and columns, and if the average pixel value is above the threshold, crop the remaining image. The default assumes a white area to be cropped, as if the image were scanned. If the opposite is true, and the portion to be cropped is dark, use the --below flag and modify the threshold to be near zero. Currently, this tool only supports images starting at the top left corner (0,0), and cropping occurs to the right of, and below the image. In a future version, this may be fixed to support cropping on all sides of the image.',
            epilog=''
            )

    parser.add_argument(
            '-f', '--filename',
            required=True,
            dest='filename',
            help='Location of the image to crop',
            action='store'
            )
    parser.add_argument(
            '-t', '--threshold',
            required=False,
            default=245.0,
            type=float,
            dest='threshold',
            help='Columns and rows above the threshold value will be cropped. A value near the max of 255 indicates a light background to be cropped, while a value near the minimum of 0 indicates a dark background. By default, values above the threshold are cropped. If a dark background needs cropped, include the --below flag and set the threshold close to zero.',
            action='store'
            )
    parser.add_argument(
            '-e', '--extra',
            required=False,
            default=0,
            type=int,
            dest='extra_pixels',
            help='Crops an additional number of pixels. Useful, for example, if photo edge is visible.',
            action='store'
            )
    parser.add_argument(
            '-b', '--below',
            required=False,
            default=True,
            dest='below',
            help='Crop when pixel values are below the threshold.',
            action='store_true'
            )
    parser.add_argument(
            '-i', '--in-place',
            required=False,
            dest='overwrite',
            help='Overwrite the source file',
            action='store_true'
            )
    parser.add_argument(
            '-o', '--outfile',
            required=False,
            dest='outfile',
            help='Name of the cropped image. If not specified, and --in-place flag is omitted, the output filename has \'_cropped\' added to it and is placed in the same directory as the source file.',
            action='store'
            )
    parser.add_argument(
            '-l', '--log-level',
            required=False,
            default='INFO',
            dest='log_level',
            choices=['INFO','DEBUG','ERROR','WARNING','CRITICAL','NOTSET'],
            help='Sets python log level.',
            action='store'
            )

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    if (sys.version_info[0] == '3' and int(sys.version[1]) < 7) or int(sys.version_info[0]) < 3:
        logging.error('Requires Python 3.7 or greater to support numpy.mean() axis argument')
        sys.exit(1)

    conf = init_args()

    logging.basicConfig(level=getattr(logging, conf.log_level), format='%(asctime)s\t- %(levelname)s - %(message)s')

    logging.debug('ARGS: %s', sys.argv)

    filename = os.path.realpath(conf.filename)

    if conf.overwrite is True and conf.outfile is None:
        outfile = conf.filename
    elif conf.outfile:
        outfile = os.path.realpath(conf.outfile)
    else:
        ffpath, ext = os.path.splitext(os.path.realpath(filename))
        outdir, fn = os.path.split(ffpath)
        newfile = f'{fn}_cropped{ext}'

        outfile = os.path.join(outdir, newfile)

    autocrop(infile=filename, outfile=outfile, threshold=conf.threshold, below=conf.below, extra=conf.extra_pixels)

