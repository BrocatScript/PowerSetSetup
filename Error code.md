# Error Codes update.exe / Коды ошибок update.exe

The following table lists all error codes returned by `update.exe`, along with their descriptions in English and Russian.

В таблице ниже перечислены все коды ошибок, возвращаемые функцией `update.exe`, а также их описания на английском и русском языках.

| Code | English Description | Русское описание |
|------|---------------------|---------------------|
| `1x1001` | No administrator rights | Нет прав администратора |
| `1x1002` | Error during deletion | Ошибка при удалении |
| `1x1003` | Folder `{temp_dir}` no longer exists. | Папка `{temp_dir}` уже не существует. |
| `1x1004` | shutil.rmtree did not delete the folder completely. | Ошибка: shutil.rmtree не удалил папку полностью. |
| `1x1005` | Attempt `{attempt}`: shutil.rmtree error: `{e}` | Попытка `{attempt}`: shutil.rmtree ошибка: `{e}` |
| `1x1006` | Installation finished with error code `{process.returncode}`. | Установка завершилась с кодом ошибки `{process.returncode}`. |
| `1x1007` | Setup file not found in temporary folder. | Установочный файл не найден во временной папке. |
| `1x1008` | Temporary folder `{temp_dir}` does not exist. | Временная папка `{temp_dir}` не существует. |
| `1x1009` | Temporary folder already missing. | Временная папка уже отсутствует. |
| `1x1010` | rmdir did not delete the folder | rmdir не удалил папку |
| `1x1011` | rmdir failed | rmdir не сработал |
| `1x1012` | Failed to delete folder `{temp_dir}` after `{max_attempts}` attempts. | Не удалось удалить папку `{temp_dir}` после `{max_attempts}` попыток. |
| `1x1013` | Error: "download_url" missing in JSON | Ошибка: в JSON отсутствует "download_url" |
