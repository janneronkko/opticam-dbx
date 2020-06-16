import argparse
import logging
import os
import subprocess
import sys

import envparse
import pkg_resources

from . import opticam

_log = logging.getLogger('opticam')


def main():
    args = parse_args()

    os.umask(int(args.umask, 8))

    setup_logging()

    if args.env_file:
        envparse.env.read_envfile(args.env_file)

    args.main(args)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--env-file',
        '-e',
        help='Path to env file',
    )

    parser.add_argument(
        '--umask',
        help='Set umask (default %(default)s)',
        default='0o022',
    )

    def print_help(args): # pylint: disable=unused-argument
        print('No command given')
        print()
        parser.print_help()
        sys.exit(1)

    parser.set_defaults(main=print_help)

    subparsers = parser.add_subparsers(title='Command')
    configure_show_version(subparsers.add_parser('version', help='Show version'))
    configure_download(subparsers.add_parser('download', help='Download videos from Dropbox'))
    configure_transcode_video(subparsers.add_parser('transcode', help='Transcode AVIs to mp4'))

    return parser.parse_args()


def configure_show_version(parser):
    parser.set_defaults(main=show_version_main)


def show_version_main(args): # pylint: disable=unused-argument
    print(pkg_resources.get_distribution('opticam-dbx').version)


def configure_download(parser):
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
        '--transcode',
        help='Transcode downloaded videos to mp4 format',
        default=False,
        action='store_true',
    )

    parser.set_defaults(main=download_main)


def download_main(args):
    downloader = opticam.AlarmVideoDownloader(
        envparse.env('DROPBOX_TOKEN'),
        args.dest,
        remove_downloaded=args.remove_downloaded,
    )

    _log.info(
        'Downloading new surveillance camera videos from Dropbox (opticam-dbx version %s)',
        pkg_resources.get_distribution('opticam-dbx').version,
    )
    downloader.download(
        after_download=transcode_avi_to_mp4 if args.transcode else None,
    )


def configure_transcode_video(parser):
    parser.add_argument(
        'video',
        help='Video to transcode',
        nargs='+',
    )

    parser.set_defaults(main=transcode_video_main)


def transcode_video_main(args):
    for source_video in args.video:
        transcode_avi_to_mp4(source_video)


def transcode_avi_to_mp4(path_to_avi):
    dest_file_path = '{}.mp4'.format(os.path.splitext(path_to_avi)[0])

    if os.path.isfile(dest_file_path) and os.stat(path_to_avi).st_mtime < os.stat(dest_file_path).st_mtime:
        _log.info(
            'Not transcoding %s to %s as the source is older than destination',
            path_to_avi,
            dest_file_path,
        )
        return

    _log.info(
        'Transcoding %s to %s',
        path_to_avi,
        dest_file_path,
    )

    subprocess.run(
        ('ffmpeg', '-y', '-i', path_to_avi, dest_file_path),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


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
