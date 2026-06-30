---
title: Connect and Control Options
linkTitle: 3 - Connecting to Pi
description: Options for connecting to the Raspberry Pi in order to transmit desired data or set parameters.
weight: 100
---

<link rel="stylesheet" href="../style.css">

## Connecting to the Pi

We will be using SSH to connect your laptop to the Pi. You can do this either over wifi or ethernet. Before doing this, we need to get the IP address of the Pi and import your public SSH key onto the Pi. 

### Direct Control
This is the process to get the IP address of the Pi and import your public SSH key. 

{{% alert title="" color="info" %}}
If you use your laptop's mobile hotspot, you will be able to see the IP address of the PI but you still need to do direct control to import your SSH key. 
{{% /alert %}}

This method requires a monitor and keyboard, cannot be used to share files between a laptop and the Pi, and is more difficult to use. However, we need to use this, mainly to import your SSH key. This is also useful in case the network-config isn't working. Direct control allows you to edit the file that controls this. 

To access the Pi’s terminal directly you will need: 

- Raspberry Pi 5 
- Pi Power Supply (plugged into wall) 
- Monitor (plugged into wall) 
- HDMI to Micro-HDMI cable 
- Keyboard 
- Ethernet cable connected to a router (or ethernet port on the wall of the lab) or just connect the Pi to wifi

Simply connect the ethernet (or just use WiFi), micro-HDMI, keyboard, and power supply to the Raspberry Pi. When it boots, you will see the cloud-init running a bunch of things and the Pi’s Ubuntu Server terminal on the monitor. 

{{% alert title="" color="info" %}}
If the Pi get stuck on a boot page and keeps cycling through booting through USB-MSD, SD, and NVME, it can't find the boot files. You may have imaged the SD card for something that doesn't support the type of Pi you have so you'll have to reimage it. If you have a small light on your Pi, you may have a tiny button next to it which you can hold to power it off. 
{{% /alert %}}

#### Running Cloud-init
Power up the Pi and wait for cloud-init to run.

Within about a minute, your Pi should connect to whatever network interface(s)
are described in `network-config` and you should be able to find it on the
network. If you setup some sort of key-based authentication (such as by
importing a key from GitHub), it may take an extra couple of minutes for
this to be ready.

After the network setup is complete, you should be able to login over SSH.

In particular, please note that you need to have SSH agent forwarding working on your laptop.
You should have already done this under [ORCA Setup](/docs/radar/setupguide/2ORCAsetup) when you first made your SSH key. You can test that everything is working by running `ssh -T git@github.com`.

When you first login, cloud-init may not have finished running. To check the status, run:

```
cloud-init status --long
```

There are also logs in `/var/log/cloud-init-output.log`. 

To keep an eye on the entire process, you can run:

```
watch "cloud-init status --long && tail -n 10 /var/log/cloud-init-output.log"
```

Expect this process to take a few minutes to complete.

#### Initial Setup
When you are able to start running commands, run `./initial_setup.sh`. This will log to `/home/ubuntu/initial_setup_output.log`. It may take around 10 minutes to complete. It will automatically reboot your Pi at the end. If you don’t want this, feel free to comment out the last line. 
<!-- mcscuse me , what last line. where. how???? -->

After this process finishes running, run `ping 8.8.8.8` to test if it is connected to wifi/ethernet. If the Pi isn't connected, it will say "Network is unreachable". If the Pi is connected, it will start detecting bytes sent by the address. Hit `CTRL + C` to stop the pinging. 

{{% alert title="Not connecting to your wifi/ethernet?" color="info" %}}
If the Pi isn't connecting to the wifi, the network-config file might not be formatted properly. One issue that I ran into was using "wlp2s0b1:" under the "wifis:" section (I was connecting to a laptop's mobile hotspot). If you run `ip link` it will list the different formats that it is looking for. In my case, it was looking for "wlan0" for wifi or "eth0" for ethernet. 

Here is how to edit your network-config files without having to take the SD card out.

- Run `ls /etc/netplan/`. It should show a .yaml.
- Run `sudo nano /etc/netplan/FILENAME.yaml`. This allows you to open and edit the file. 
- Change whatever you need to, then hit `CTRL + X`, then `y`, then hit enter. This saves your edits.
- Run `sudo netplan apply` to apply these changes
- Try pinging 8.8.8.8 again to see if is connected now
- You may need to run `sudo reboot`
{{% /alert %}}

You can log in and run commands directly with the keyboard (no mouse inputs). There is no way to scroll up through this terminal however, so if you want to be able to read a long output from a command you must pipe it into a file (ex. `python run.py >> terminal_output.txt`), then read the text file using nano. 

### Importing Your SSH Key
You then need to add this SSH to the Pi. The simplest method is to first add the key to your GitHub account, then import it onto the Pi from there. If you don’t want to set up GitHub, you can add the key directly with a little extra work.

**With GitHub:** 
1. You should have already added the SSH key to your GitHub account. 
2. Run `ssh-import-id gh:<your-github-username>` on the Raspberry Pi with the direct control

If you haven't yet, do the following:

1. Create an account on GitHub and sign in. 
2. In GitHub, open settings and go to the SSH and GPG keys tab and add a new SSH key. 
3. Name this key whatever you want and paste the key into the correct field. 
4. Log into the Pi using the direct control method above. 
5. Run `ssh-import-id gh:<your-github-username>`. 

**Without GitHub:**

1. Log into the Pi using the direct control method above. 
2. Open the authorized keys file with `sudo nano ~/.ssh/authorized_keys`. 
3. Manually copy your key (starts with ssh-ed25519, ends with your email) into the file 
4. Hit Ctrl+X followed by Y, then Enter to save the changes. 

You should now have permission to SSH into the Pi from your laptop using one of the following methods (wifi or ethernet). 

Modify your `~/.ssh/config` file (use `nano ~/.ssh/config`) and add an entry like this enabling SSH agent forwarding (or don't, you likely already set up SSH agent forwarding on your laptop so I don't think you need to do this):

```
Host 192.168.11.137
    HostName 192.168.11.137
    User ubuntu
    ForwardAgent yes
```

Note that if your username or host IP address is different, you should adjust it accordingly.

{{% alert title="Remote host identification has changed" color="info" %}}
If you use the same static IP for multiple Pi's (which, presumably, you only
ever use one of at a time), you may encounter an error stating:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
```

This is because your computer thinks its connecting to a different Raspberry Pi.

You can manually add the fingerprint for the currently connected Pi like this:

```
ssh-keyscan -H 192.168.11.137 >> ~/.ssh/known_hosts
```

(This would be a bad idea to do at random for a remote computer. I'm assuming
here that you've just plugged in a new Pi right in front of you and you
know exactly why you're getting this error. You should only have to do this once
per new Pi.)
{{% /alert %}}

{{% alert title="" color="info" %}}
You might be able to just run `ssh ubuntu@<pi-ip-address>` on your Pi to SSH connect. The direct connect and internet connection should already exist since you needed them previously to import your GitHub key. You can get your Pi's IP address by running `hostname -I` or `ip a` (in my opinion, using `hostname -I` is easier cause you don't need to hunt for the ip info).
{{% /alert %}}

### SSH over Ethernet:

**This is the preferred method for connecting to and controlling the Pi** , and the only method that does not require the Pi to be connected to a router or Wi-Fi network. However, it does take a bit of setup the first time. 

For this method, you will need: 
   - Laptop connected to Wi-Fi 
   - Raspberry Pi 5 
   - Pi Power Supply (plugged into wall) 
   - Ethernet cable 
   - Ethernet to usb-c adapter (if your laptop doesn’t have an ethernet port) 

1. Plug the power supply into the Pi and plug one end of the ethernet cable into the Pi, and the other into your laptop. 
2. Connect your laptop to any Wi-Fi network. 
3. If your laptop's public SSH key is not already on the Pi, see the section above for how to add it. (Using direct connect)
4. If this is your first time setting up this method, you will now need to enable internet sharing on your laptop. If you have done this before, then skip this step. 

      - a. Windows: 
         - i. Open Control Panel and go to the Network section. 
         - ii. Find the Wi-Fi connection and right click on it, then go to Properties. 
         - iii. At the top, click on the Sharing tab. 
         - iv. Check “Allow other network users to connect...” 
         - v. In the dropdown, select “Ethernet2” (not the ethernet for WSL). 
         - vi. Apply the changes. 

      - b. Linux: 
         - i. Install Network Manager Command-line Interface (nmcli) with `sudo apt install network-manager` . 
         - ii. Find the connection name with `nmcli con show` . Find the entry with type ethernet, it should have a name like “Wired connection 1”. 
         - iii. Run `nmcli con modify “Wired connection 1” ipv4.method shared` . 

5. If you are on Linux, run `nmcli con up “Wired connection 1”` 
6. Find the Pi’s IP address on your local subnet. 
   - a. If you are on Windows, open PowerShell and run `arp -a`. You should see an interface for 192.168.137.1 and within that section should be an IP address that starts with 192.168.137 and ends with something other than .0 or .1 (ex. 192.168.137.27). 
   - b. If you are on Linux, then Pi #1 always has the IP 10.42.0.10, and Pi #2 always has the IP 10.42.0.20. If for some reason you cannot find the IP, confirm the subnet is 10.42.0 by running `ip a` . Under the enxc... section should say “state UP” and you should see “inet 10.42.0.1/24”. You can then scan the subnet to find the pi by running `nmap -sn 10.42.0.1/24` and looking for a device that’s not 10.42.0.1. You may need to restart the Pi and give it a minute to boot. 
7. Run `ssh ubuntu@<pi-ip-address>` to connect to the Pi. You can now run commands on the Pi, and transfer files to and from your laptop using SCP (will be explained below).

### SSH over Wi-Fi: 

This method is nice as it requires less cables and can be used for connecting multiple devices, **however you will have to use one of the other methods such as SSH over Ethernet initially to find the Pi’s internet IP address.** 

For this method, you will need: 
   - Laptop connected to Wi-Fi 
   - Raspberry Pi 5 
   - Pi Power Supply (plugged into wall) 
   - Ethernet cable connected to a router (or to the ethernet port on the wall of the lab) if not connecting the Pi to Wi-Fi 

1. Plug the ethernet and power cable into the Pi and turn it on. 
2. If you do not know what the Pi’s current IP address is, you must first use the Direct Control method above to get access to the terminal. When the Pi first boots, system information is printed to the terminal. In the bottom right corner of this message, you should see a section that says “IPv4 address for eth0: 128.138.189.xxx”. You can also find the IP address by running `ip a` and looking for the address under the `eth0` **This address may change each time the Pi is reconnected to the internet.** 
3. Connect your laptop to a wifi network. 
4. Check if you can find the Pi over the internet by running the command 
`ping -c 1 your.pi.ip.address`. On Windows, this must be done in PowerShell with admin privileges, not WSL. If it says 0 packets received, then either the IP address is incorrect, or you are not on the same network as the Pi. 
5. If your laptop's public SSH key is not already on the Pi, see the section above (Importing Your SSH Key section) for how to add it. 
6. Run `ssh ubuntu@your.pi.ip.address` to connect to the Pi. If you chose a different login username, replace ubuntu with that. You can now run commands on the Pi, and transfer files to and from your laptop using SCP (see below).

{{% alert title="" color="info" %}}
If you SSH into your pi from your laptop, you can type `exit` or `logout` to turn your powershell back to normal.
{{% /alert %}}


## Cloning the Repository onto the Pi

Run `git clone https://github.com/username/repositoryname` to add the uhd-radar github repository to the Pi. If you don't have the `https://` it won't work. Using SSH (the link that ends with .git) also won't work because your Pi doesn't have your laptop's private key. Don't give your Pi your private SSH key.

## Transferring files to and from the Pi:

The Raspberry Pi 5 unfortunately does not support data transfer (USB OTG) over its USB 3.0 ports, only the USB C port which we currently use for power. Fortunately, we can make use of the SSH connection to send files to and from the Pi using SCP and/or GitHub. 

If you have committed changes to the code and pushed them to GitHub, you can just checkout the correct branch and run `git pull` on the Pi to see them. However, if you are debugging or making small changes to a file that aren’t worthy of a commit, you can send files directly with SCP (secure copy protocol) by running the following command on your laptop. 

Send a single file with `scp <my-file-path> ubuntu@<pi-ip-address>:<pidirectory-path>` 

Example:
- Windows: `scp sdr\main.cpp ubuntu@192.168.137.10:~/uhd_radar/sdr/` 
- Windows: `scp .\Downloads\test.txt ubuntu@192.167.138.131:~/` 
    - This pushed from C:\Users\Name\Downloads and put it in /home/username

- Linux: `scp sdr/main.cpp ubuntu@10.42.0.10:~/uhd_radar/sdr/` 

{{% alert title="" color="info" %}}
The `"."` in windows and the `"~"` in ubuntu act the same way. They both make it start in the home directory so you don't have to type all of it out. The `"."` for windows puts you in `C:/Users/YourName` and the `"~"` for ubuntu puts you in `/home/AccountUsername`.
{{% /alert %}}

You can also send a whole folder with `scp -r <my-directory-path> ubuntu@<piip-address>:<pi-directory-path>` 

To send files from the Pi back to your laptop, reverse the two arguments ensuring the first is one or more files, or directory, and the second is a directory for where the file should go.

Example:
- Windows: `scp ubuntu@10.42.0.10:~/uhd_radar/data/20250716* ~/uhd_radar/data/` 
- Windows: `scp ubuntu@192.168.137.131:~/test2.txt .\Downloads`
    - This pulled from /home/username and put it in C:/Users/Name/Downloads

**If you push or pull a file that has the same name in the other device, the new file pushed/pulled will overwrite the old file.**

When using these commands, you are typing them on your laptop powershell. You are either pushing from your laptop to the Pi, or you are using your laptop to pull from the Pi. You can also push from the Pi but that's a different command. 

## Installing Miniconda
1. First go to Anaconda's [website](https://www.anaconda.com/download) and scroll to the bottom to download Miniconda. You will want the Linux 64-Bit ARM64 version.
2. Once the file is downloaded, you will want to use SCP to get the file onto the Pi. Make sure you have connected to the Pi using SSH. The command might look something like `scp .\Downloads\Miniconda3-latest-Linux-aarch64.sh ubuntu@192.168.137.131:~/`. 
3. Within the Raspberry Pi's terminal, run `bash location-to-file/Miniconda3-latest-Linux-aarch64.sh` and accept the default options in the installer (select yes when prompted about auto_activate_base, though we will change this later)
4. After Miniconda is installed, reboot the Raspberry Pi with `sudo reboot now`
5. To ensure it has been installed, run “conda list” and you should see a list of the installed dependencies printed out. 
6. We are now going to change one of the default settings with the command `conda config --set auto_activate_base false`