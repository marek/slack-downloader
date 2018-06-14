# slack-downloader

`slack-downloader` is a tool to download/backup [Slack](https://slack.com) files on a local disk.

The program will download latest files uploaded on Slack, on a configured directory.
History of already downloaded files is mantained, in order to avoid duplicate downloads.

Files will be organized inside of a specified directory, with the following form:

```
<channel_name>/<date>-<filename>_by_<user/uploader>.<ext>
```

where `<date>` has the form `%Y%m%d_%H%M%S`.

This project is a fork of [marek/fslack](https://github.com/marek/fslack), used for a different purpose.

### Requirements

* `Slack API Token`: Get it from (https://api.slack.com/web)
* `Python`: The app is written in Python
* `python-requests`: web request library for Python

### Installation Instructions

1. Download the Python program:

   ```
   wget https://raw.githubusercontent.com/auino/slack-downloader/master/slack-downloader.py
   chmod +x slack-downloader.py
   ```

2. Open the `slack-downloader.py` script with a text editor and configure it using a [legacy token](https://api.slack.com/custom-integrations/legacy-tokens)
3. Optionally, you can add the program to your `crontab` to automatically check for new shared items on Slack:

   ```
   crontab -e
   ```

4. Now you have to append the following line (press `i` button to insert data):

   ```
   0 * * * * python /directory_path/slack-downloader.py
   ```

   where `/directory_path/` identifies the path of the directory containing the script, while `0 *` specifies the program has to be called every hour.
5. Hit `:q` to close, saving the file
6. Enjoy!

### Supporters ###

 * (https://github.com/nalt)[nalt] for the fix on file downloads

### Contacts ###

You can find me on Twitter as [@auino](https://twitter.com/auino).
