# fslack.py

fslack.py is tool to download and delete files off of Slack.
This is in response to <a href="https://www.ibuildings.nl/blog/2015/11/hidden-plain-sight-brute-forcing-slack-private-files">security problem</a>

### Requirements

* [Slack API Token] - Get it from https://api.slack.com/web and pass it via --token
* [Python] - The app is written in python3
* [requests] - web request library for python

### Installation Instructions

```sh
wget https://raw.githubusercontent.com/marek/fslack/master/fslack.py
chmod +x fslack.py
```

### Usage Instructions

get an api token from https://api.slack.com/web
```sh
fslack.py --download --all --out foo <token>
```

** Note: output folder must exit prior to calling the command


