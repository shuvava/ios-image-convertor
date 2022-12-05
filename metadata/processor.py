# encoding: utf-8
import os.path
from datetime import datetime
from pathlib import Path
from logging import getLogger
from shutil import copy2
from typing import List, Dict

import pyheif
from PIL import Image

from metadata import get_metadata
from metadata.model import Photo

log = getLogger(__name__)


def process_file(file: Path, dest_path: str, photo: Photo, cnt: int):
    suffix = file.suffix.lower()
    if suffix == '.heic':
        heif_file = pyheif.read(file)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(f'{dest_path}/{photo.build_name(cnt)}.jpg', "JPEG")
    else:
        copy2(file, f'{dest_path}/{photo.build_name(cnt)}{file.suffix}')


def process_images(in_dir: str, out_dir: str, max_date: str):
    photos: List[Photo] = []
    counter: Dict[str, int] = {}
    unprocessed_path = os.path.join(out_dir, 'unprocessed')
    log.info('reading files metadata')
    for path in Path(in_dir).rglob('*.*'):
        try:
            photo = get_metadata(path)
            if photo is not None:
                photos.append(photo)
        except Exception as error:
            log.error(f'file {path} was not processed {error}')
            Path(os.path.join(out_dir, 'unprocessed')).mkdir(parents=True, exist_ok=True)
            dest = os.path.join(out_dir, 'unprocessed', path.name)
            copy2(path, dest)
    log.info(f'soring data ({len(photos)} items)')
    photos.sort(key=lambda x: x.order)
    log.info('moving files')
    for photo in photos:
        if photo.date > max_date:
            log.warning(f'photo date is incorrect {photo} (max allowed date {max_date})')
            key = f'{photo.city}'
        else:
            key = f'{photo.date}_{photo.city}'
        cnt = counter.get(key, 0)
        origin_path = os.path.join(in_dir, photo.file_name)
        if photo.date > max_date:
            path = out_dir
        else:
            path = os.path.join(out_dir, photo.dir_name())
        if cnt == 0:
            Path(path).mkdir(parents=True, exist_ok=True)
        file = Path(origin_path)
        process_file(file, path, photo, cnt)
        cnt += 1
        counter[key] = cnt
