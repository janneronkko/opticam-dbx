import datetime
import logging
import os

import dropbox

_log = logging.getLogger('opticam')


class AlarmVideoDownloader(object):
    def __init__(self, auth_token, dest_root_dir, remove_downloaded):
        super().__init__()

        self.dbx = dropbox.Dropbox(auth_token)
        self.dest_root_dir = dest_root_dir
        self.remove_downloaded = remove_downloaded

    def download(self):
        for file in self._get_alarm_video_files():
            self._download_file(file)

            if self.remove_downloaded:
                _log.info(f'Removing file {file.path_lower} from Dropbox')
                self.dbx.files_delete(file.path_lower)

    def _download_file(self, file):
        recording_time = datetime.datetime.strptime(file.name, 'MDalarm_%Y%m%d_%H%M%S.avi')

        dest_path = os.path.join(
            self.dest_root_dir,
            '{}.avi'.format(recording_time.strftime('%Y-%m-%d %H-%M-%S')),
        )
        dest_path = os.path.abspath(dest_path)

        if os.path.isfile(dest_path):
            existing_file_size = os.stat(dest_path).st_size
            if existing_file_size == file.size:
                _log.info(f'Skipping already downloaded file {dest_path}')
                return

            assert existing_file_size < file.size, \
                f'File {file.path_lower} is smaller than existing file {dest_path}'

            _log.info(f'Removing existing partially downloaded file {dest_path}')
            os.remove(dest_path)

        elif os.path.exists(dest_path):
            raise AssertionError('File {dest_path} exists but is not a file')

        _log.info(f'Downloading file {file.name} into {dest_path}')
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        self.dbx.files_download_to_file(dest_path, file.path_lower)

    def _get_alarm_video_files(self):
        files_list_result = self.dbx.files_list_folder(
            '/apps/ipcamera',
            include_media_info=True,
        )

        yield from (
            entry
            for entry in files_list_result.entries
            if entry.name.endswith('.avi')
        )
