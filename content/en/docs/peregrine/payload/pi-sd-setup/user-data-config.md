---
title: Customizing user-data
#description: 
#weight: 10
---

The default user-data we start from is as shown below. You will likely need to
tweak many of these settings. Descriptions and tips for the most important
sections are below.

Note that this is one of two key configuration files. You can read about
[network-config here]({{< ref "pi-internet" >}}).

## Starting point user-data file

{{< readfile file="/static/cloud-init/user-data" code="true" lang="yaml" >}}

## Password-less shutdown

```
system_info:
  default_user:
    name: ubuntu # Allow the default user to shutdown or reboot the system without entering a password (used by our automated scripts)
    sudo: "ALL=(ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown"
```

One of the features supported by the uav_radar_logger utility is to automatically
cleanly shutdown the system if the measured battery voltage drops below a
threshold. To facilitate this, the default user must be able to shutdown the
system without needing additional authentication. This gives permission for the
`ubuntu` user to call `sudo shutdown` or `sudo reboot` without entering a password.

## Password authentication

```
# On first boot, set the (default) ubuntu user's password to "cryosphere"
chpasswd:
  expire: false
  list:
  - ubuntu:$6$rounds=4096$aQ7tu0.beL3WAL32$fKxKYvZpY7EMCoxAU1heRomA3v8WvgbqBhhz08QwOtQdlP/DJOP2BThqZFoRW8d2a9PaIKK9BC9NHs1qNnkya1

# Enable password authentication with the SSH daemon
ssh_pwauth: true
```

This sets up a default password for the `ubuntu` user. You should change this to
something else (or disable password authentication completely, if you prefer).

Passwords are stored in a hashed format. You can generate password hashes using
this utility:

```
mkpasswd --method=SHA-512 --rounds=4096
```

## Timezone

```
# Set a default timezone
timezone: Etc/UTC
```

You could set this to other time zones (i.e. `America/Los_Angeles"), but really
it would make everyone's life easier if you just set your clock to UTC.

## Add SSH keys through GitHub

```
## On first boot, use ssh-import-id to give the specific users SSH access to
## the default user
ssh_import_id:
- gh:thomasteisberg
- gh:albroome
- gh:dfxmay
```

You can very conveniently enable key-based authentication for specific GitHub
user names. If your username is in here and you have a public key setup with GitHub,
this public key will be imported and you will be able to SSH into your Pi
with no additional setup. You might want to remove us from your list, though. :)

## Files

Arbitrary files can be written to the system with cloud-init. Some of these are
important.

### initial_setup.sh

```
- path: /home/ubuntu/initial_setup.sh
  content: |
    #!/bin/bash
    exec > >(tee -a "initial_setup_output.log") 2>&1
    # Miniconda Setup
    wget --progress=bar:force:noscroll "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh" -O $HOME/miniconda.sh
    bash $HOME/miniconda.sh -b -p $HOME/miniconda
    cd $HOME
    source .profile
    source miniconda/etc/profile.d/conda.sh
    conda init bash
    # Setup logger environment
    git clone git@github.com:thomasteisberg/uav_radar_logger.git
    # Clone uhd_radar repo
    git clone git@github.com:radioglaciology/uhd_radar.git
    cd uhd_radar
    #git checkout thomas/dask # Uncomment if you want to check out a specific branch other than main
    conda env create -n uhd -f environment.yaml
    conda activate uhd
    python /home/ubuntu/miniconda/envs/uhd/lib/uhd/utils/uhd_images_downloader.py
    systemctl --user enable radar.service
    systemctl --user enable logger.service
    ifconfig
    sudo reboot
  append: true
```

The `initial_setup.sh` script grabs copies of our code and sets up the radar and
logging services. This script is intended to be manually run the first time you
SSH into the system. This enables you to use
[SSH agent forwarding](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/using-ssh-agent-forwarding)
to provide any needed GitHub authentication to get the code.

This is also where you would customize the repositories to check out (if, for
example, you've forked our code) and where you can pick a branch to automatically
checkout.

### Radar and Logger services

```
- path: /etc/systemd/user/radar.service
  content: |
    [Unit]
    Description=Service to run the radar code on startup

    [Service]
    Type=simple
    WorkingDirectory=/home/ubuntu/uhd_radar/
    ExecStart=/home/ubuntu/uhd_radar/manager/radar_service.sh

    Restart=always
    RestartSec=10

    KillSignal=SIGINT

    [Install]
    WantedBy=default.target
- path: /etc/systemd/user/logger.service
  content: |
    [Unit]
    Description=Service to log data from I2C sensors and automatically shutdown below a voltage threshold

    [Service]
    Type=simple
    WorkingDirectory=/home/ubuntu/uav_radar_logger/
    ExecStart=/home/ubuntu/uav_radar_logger/logger_service.sh

    Restart=always
    RestartSec=60

    KillSignal=SIGINT

    [Install]
    WantedBy=default.target
```

Two systemd services are used to manage everything. One run the radar code in
its default button-controlled setup. The other runs basic logging of I2C-connected
sensors and handles automatic low-battery shutdown.

## Run commands

```
runcmd:
- chown -R ubuntu:ubuntu /home/ubuntu
- chmod +x /home/ubuntu/initial_setup.sh
- wget -O /etc/udev/rules.d/uhd-usrp.rules https://raw.githubusercontent.com/EttusResearch/uhd/master/host/utils/uhd-usrp.rules
- usermod -a -G i2c ubuntu
- usermod -a -G dialout ubuntu
- usermod -a -G tty ubuntu
- apt remove -y modemmanager
- systemctl stop serial-getty@ttyS0.service && systemctl disable serial-getty@ttyS0.service
- i2cdetect -y 1
- echo "dtoverlay=i2c-rtc,pcf8523" >> /boot/firmware/config.txt
- loginctl enable-linger ubuntu
- mkdir /media/ssd
- echo "/dev/sda2  /media/ssd  exfat  defaults,nofail,uid=1000,gid=1000  0  2" | tee -a /etc/fstab
```

Some final setup is done by running arbitrary commands. These are run as the root
user.

One aspect of this you may wish to customize are the last two lines, which add
settings to automatically mount an ExFAT-formatted SSD plugged into the Pi. This
can be (optionally) used as a storage location for radar data.

## Testing changes

You may want to test your changes before using them on your Pi. Options for doing
that are [described here](https://cloudinit.readthedocs.io/en/latest/howto/predeploy_testing.html).
Note that the `initial_setup.sh` script downloads miniconda for the `aarch64`
architecture, which probably won't work on your computer. If you want to test that
part, you'll need to change this.