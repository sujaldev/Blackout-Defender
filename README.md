# Blackout Defender

This is a different approach to [DUAS](https://github.com/sujaldev/duas) (which I feel I've overcomplicated), in this
version a laptop will be used to detect power outages based on whether the laptop is on battery power or not. Since one
already has to keep a laptop forever on for this, it'll be a good idea to use the laptop screen to display various data
about the server.

> **Note** If it isn't obvious, you have to keep the laptop plugged in, otherwise there's no way to tell if there's
> a power outage or not.

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
