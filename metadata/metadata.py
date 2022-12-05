# encoding: utf-8
import os
import platform
from datetime import datetime
from io import BytesIO
from logging import getLogger
from pathlib import Path
from typing import Optional

import ffmpeg
import pyheif

from geo import to_dec_deg, get_city
from metadata.model import Photo
from exifread import process_file

log = getLogger(__name__)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(os.path.getctime(path_to_file))
    else:
        stat = os.stat(path_to_file)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return datetime.fromtimestamp(stat.st_mtime)


def get_heif_metadata(file_name: str, file:Path) -> Photo:
    """extract metadata from HEIF image"""
    heif_file = pyheif.read(file)
    for metadata in heif_file.metadata:
        file_stream = BytesIO(metadata['data'][6:])
        tags = process_file(file_stream, details=False)
        if not tags:
            continue
        long = tags.get('GPS GPSLongitude', None)
        long_ref = tags.get('GPS GPSLongitudeRef', '')
        lat = tags.get('GPS GPSLatitude', None)
        lat_ref = tags.get('GPS GPSLatitudeRef', '')
        str_dt = str(tags['Image DateTime'])
        gps_date = str(tags.get('GPS GPSDate', ''))
        if gps_date == '':
            # dt = datetime.strptime(str_dt, '%Y:%m:%d %H:%M:%S')
            gps_date = str_dt.split(' ')[0]
        longitude = to_dec_deg(long_ref, long)
        latitude = to_dec_deg(lat_ref, lat)
        city = get_city(latitude, longitude)
        # for k, v in tags.items():
        #     print(f'"{k}" :::: {v}')
        return Photo(file_name, city, gps_date, str_dt)
    raise ValueError('No EXIF information found')


def get_jpg_metadata(file_name: str, file: Path) -> Photo:
    """extract metadata from JPG image"""
    with open(file, 'rb') as img_file:
        tags = process_file(img_file)
        if not tags:
            raise ValueError('No EXIF information found')
    long = tags.get('GPS GPSLongitude', None)
    long_ref = tags.get('GPS GPSLongitudeRef', '')
    lat = tags.get('GPS GPSLatitude', None)
    lat_ref = tags.get('GPS GPSLatitudeRef', '')
    str_dt = str(tags.get('Image DateTime', ''))
    if str_dt != '':
        dt = str_dt.split(" ")[0]
    else:
        _dt = creation_date(file)
        dt = _dt.strftime("%Y:%m:%d")
        str_dt = _dt.strftime("%Y:%m:%d %H:%M:%S")
    longitude = to_dec_deg(long_ref, long)
    latitude = to_dec_deg(lat_ref, lat)
    city = get_city(latitude, longitude)
    return Photo(file_name, city, dt, str_dt)


def get_png_metadata(file_name: str, file: Path) -> Photo:
    """extract metadata from PNG image"""
    with open(file, 'rb') as img_file:
        tags = process_file(img_file)
        if not tags:
            raise ValueError('No EXIF information found')
    str_dt = str(tags['EXIF DateTimeOriginal'])
    dt = str_dt.split(" ")[0]

    return Photo(file_name, '', dt, str_dt)


def get_mov_metadata(file_name: str, path: Path) -> Photo:
    # file creation date looks more accurate for test data set
    # probe = ffmpeg.probe(str(path))
    # tags = probe['streams']
    # for tag in tags:
    #     if 'tags' not in tag:
    #         continue
    #     tag = tag['tags']
    #     if 'creation_time' in tag:
    #         dt = datetime.strptime(tag['creation_time'], '%Y-%m-%dT%H:%M:%S.%f%z')
    #         return Photo(file_name, '', dt.strftime("%Y:%m:%d"), dt.strftime("%Y:%m:%d %H:%M:%S"))
    _dt = creation_date(path)
    return Photo(file_name, '', _dt.strftime("%Y:%m:%d"), _dt.strftime("%Y:%m:%d %H:%M:%S"))


def get_metadata(file: Path) -> Optional[Photo]:
    suffix = file.suffix.lower()
    if suffix == '.heic':
        return get_heif_metadata(str(file.name), file)
    elif suffix == '.png':
        return get_png_metadata(str(file.name), file)
    elif suffix in {'.jpeg', '.jpg'}:
        return get_jpg_metadata(str(file.name), file)
    elif suffix in {'.mov', '.avi', '.mp4'}:
        return get_mov_metadata(str(file.name), file)
    else:
        log.info(f'got unexpected file type: {file.suffix}')
        return None
