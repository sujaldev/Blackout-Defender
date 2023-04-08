# Blackout Defender

This is a different approach to [DUAS](https://github.com/sujaldev/duas) (which I feel I've overcomplicated), in this
version a laptop will be used to detect power outages based on whether the laptop is on battery power or not. ~~Since
one already has to keep a laptop forever on for this, it'll be a good idea to use the laptop screen to display various
data about the server.~~ I'm ditching the TUI part because textual doesn't look as good in a virtual console (don't
know the exact name, the ones that open on `Ctrl+Alt+F1-F9`).

> **Note** If it isn't obvious, you have to keep the laptop plugged in, otherwise there's no way to tell if there's
> a power outage or not.

## Other dumb approaches

Checkout the other branches in this repo for other approaches, I find that the main branch is the simplest.

## Build

Build the script on the same machine you intend to run it on (or a similar VM).

#### Setup

```bash
git clone https://github.com/sujaldev/blackout-defender
cd blackout-defender

# Setup a virtualenv if you wish (recommended)
viritualenv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt pyinstaller

cd src/
```

#### Build (on laptop)

```bash
pyinstaller --onefile --name bd-server main.py
```