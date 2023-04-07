# Blackout Defender

This is a different approach to [DUAS](https://github.com/sujaldev/duas) (which I feel I've overcomplicated), in this
version a laptop will be used to detect power outages based on whether the laptop is on battery power or not. ~~Since
one already has to keep a laptop forever on for this, it'll be a good idea to use the laptop screen to display various
data about the server.~~ I'm ditching the TUI part because textual doesn't look as good in a virtual console (don't
know the exact name, the ones that open on `Ctrl+Alt+F1-F9`).

> **Note** If it isn't obvious, you have to keep the laptop plugged in, otherwise there's no way to tell if there's
> a power outage or not.

## Other dumb approaches

Checkout the other branches in this repo for other approaches, I find that the main branch is the simplest (doesn't
require installing anything on your proxmox server, if you ignore the TUI part).

## Systemd

Modify the `src/server/sample.service` according to your needs, don't forget to change the `/path/to/compiled/binary`
and `DE:AD:BE:EF` parameters on the `ExecStart` line. Enable and start the service on your laptop.

## Build

It'll be better to build each script on it's intended host, the server script on your laptop and the client script on
your proxmox server.

#### Setup

```bash
git clone https://github.com/sujaldev/blackout-defender
cd blackout-defender

# Setup a virtualenv if you wish (recommended)
viritualenv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt pyinstaller
```

#### Build client (on proxmox)

> **Note** Skip this step if you don't plan on using the TUI.

Your proxmox server may not have all the build tools required for this, if you wish to keep it that way, set up a debian
virtual machine and perform the build there.

```bash
cd src/client/
pyinstaller --onefile --name bd-client main.py
```

#### Build server (on laptop)

```bash
cd src/server/
pyinstaller --onefile --name bd-server main.py
```