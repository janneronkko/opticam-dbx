import argparse
import logging
import sys

import envparse
import pkg_resources

from . import opticam

_log = logging.getLogger('opticam')


def main():
    args = parse_args()
    if args.only_show_version:
        print(pkg_resources.get_distribution('opticam-dbx').version)
        return

    setup_logging()

    if args.env_file:
        envparse.env.read_envfile(args.env_file)

    downloader = opticam.AlarmVideoDownloader(
        envparse.env('DROPBOX_TOKEN'),
        args.dest,
        remove_downloaded=args.remove_downloaded,
    )

    _log.info(
        'Downloading new surveillance camera videos from Dropbox (opticam-dbx version %s)',
        pkg_resources.get_distribution('opticam-dbx').version,
    )
    downloader.download()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--env-file',
        '-e',
        help='Path to env file',
    )

    parser.add_argument(
        '--dest',
        default=envparse.env('VIDEO_ROOT_DIR', '.'),
        help='Destination directory',
    )

    parser.add_argument(
        '--remove-downloaded',
        help='Remove videos from Dropbox after download',
        default=False,
        action='store_true',
    )

    parser.add_argument(
        '--version',
        help='Show version and exit',
        dest='only_show_version',
        default=False,
        action='store_true',
    )

    return parser.parse_args()


def setup_logging():
    _log.propagate = False

    handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname) 4s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S%z',
    )
    handler.setFormatter(formatter)

    _log.addHandler(handler)

    _log.setLevel(logging.INFO)


if __name__ == '__main__':
    main()
