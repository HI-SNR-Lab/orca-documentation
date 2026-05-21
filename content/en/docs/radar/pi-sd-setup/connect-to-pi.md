---
title: Connecting to the Raspberry Pi
#description: 
weight: 10
---

By default, the cloud-init script sets up a static IP of `192.168.11.137`, but
you could choose to configure this to something different for each payload box.

Our usual way of connecting is by plugging an ethernet cable into the Pi and
connecting it to a laptop. You can read about
[all the networking options here]({{< ref "pi-internet" >}}).

## SSH agent forwarding

If you need to authenticate to GitHub to download code, the recommended way is
using [SSH agent forwarding](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/using-ssh-agent-forwarding).

To summarize the above link, you should make sure you have
[an SSH key setup with your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys).

Test this by running `ssh -T git@github.com`.

{{% alert title="Setup an SSH Key" color="info" %}}

If you do not already have an SSH key, you can create one as follows: 

1. In your terminal (PowerShell on Windows) run `ssh-keygen -t ed25519 -C “your@email.com”` and accept the default location.  
2. Create a memorable password. When you type the password, no text will appear in the terminal but the password is being logged.  
3. We now need to copy the public key you just created. When the key was generated, a message should have been printed that says something like Your public key has been saved in `/home/<username>/.ssh/id_ed25519.pub`.  
4. To view the contents of this public key file, run  `cat <path-from-above>/.ssh/id_ed25519.pub` and copy the full key that is printed to the terminal.

You then need to add this SSH to the Pi. The simplest method is to first add the key to your GitHub account, then import it onto the Pi from there. If you don’t want to set up GitHub, you can add the key directly with a little extra work. 

**GitHub:** 
1. Create an account on GitHub and sign in. 
2. In GitHub, open settings and go to the SSH and GPG keys tab and add a new SSH key. 
3. Name this key whatever you want and paste the key into the correct field. 
4. Log into the Pi using the direct control method above. 
5. Run `ssh-import-id gh:<your-github-username>`.

**Without GitHub:**
1. Log into the Pi using the direct control method above. 
2. Open the authorized keys file with `sudo nano ~/.ssh/authorized_keys`. 
3. Manually copy your key (starts with ssh-ed25519, ends with a comment) into the file 
4. Hit Ctrl+X followed by Y, then Enter to save the changes. 

{{% /alert %}}

You should now have permission to SSH into the Pi from your laptop using one of the following methods. 

Then modify your `~/.ssh/config` file to have an entry like this enabling
SSH agent forwarding:

```
Host 192.168.11.137
    HostName 192.168.11.137
    User ubuntu
    ForwardAgent yes
```


## SSH'ing to your Pi

Connect to the Raspberry Pi over SSH:

```
ssh ubuntu@192.168.11.137
```


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

You can test that your SSH agent forwarding is working by running
`ssh -T git@github.com` again while SSH'd into your Pi.

## Types of Control

There are three potential ways to control the Raspberry Pi; direct control, ethernet, or WiFi.

### Direct Control

This method requires a monitor and keyboard, cannot be used to share files between a laptop and the Pi, and is more difficult to use. **I would only recommend this method if it were needed while setting up an SSH connection from your laptop, or you are unable to use the alternate methods.**

To access the Pi’s terminal directly you will need: 
1. Raspberry Pi 5 
2. Pi Power Supply (plugged into wall) 
3. Monitor (plugged into wall) 
4. HDMI to Micro-HDMI cable 
5. Keyboard 
6. Ethernet cable connected to a router (or ethernet port on the wall of the lab)

Connect the ethernet (or just use WiFi), micro-HDMI, keyboard, and power supply to the Raspberry Pi. When it boots, you will see the Pi’s Ubuntu Server terminal on the monitor and can log in and run commands directly with the keyboard (no mouse inputs). There is no way to scroll up through this terminal however, so if you want to be able to read a long output from a command you must pipe it into a file (ex. python run.py >> terminal_output.txt), then read the text file using nano. 

### SSH over Ethernet

**This is the preferred method for connecting to and controlling the Pi**, and the only method that does not require the Pi to be connected to a router or Wi-Fi network. However, it does take a bit of setup the first time.

For this method, you will need: 
1. Laptop connected to Wi-Fi 
2. Raspberry Pi 5 
3. Pi Power Supply (plugged into wall) 
4. Ethernet cable 
5. Ethernet to usb-c adapter (if your laptop doesn’t have an ethernet port) 

{{% alert title="Common Mac Problem" %}}

Keep in mind that, especially if you are on a network with a firewall and you are using a more recent MacBook, due to how Mac routes Wi-Fi, the Raspberry Pi's internet connection will either be difficult or impossible. SSH via Ethernet is most likely to work on a Windows or Linux machines. If you are using a Mac on university Wi-Fi, and can ping the Raspberry Pi but the Pi cannot connect to the network, you will likely need to either use a different network on your computer, contact your university's IT department, or use a different Control Type.

{{% /alert %}}

**Process**
1. Plug the power supply into the Pi and plug one end of the ethernet cable into the Pi, and the other into your laptop. 
2. Connect your laptop to any Wi-Fi network. 
3. If your laptop's public SSH key is not already on the Pi, see the section above for how to add it. 
4. If this is your first time setting up this method, you will now need to enable internet sharing on your laptop. If you have done this before, then skip this step.
   
     **Windows:**
      1. Open Control Panel and go to the Network section. 
      2. Find the Wi-Fi connection and right click on it, then go to Properties. 
      3. At the top, click on the Sharing tab. 
      4. Check “Allow other network users to connect...” 
      5. In the dropdown, select “Ethernet2” (not the ethernet for WSL). 
      6. Apply the changes.
         
     **Linux:** 
      1. Install Network Manager Command-line Interface (nmcli) with `sudo apt install network-manager`. 
      2. Find the connection name with `nmcli con show`. Find the entry with type ethernet, it should have a name like “Wired connection 1”. 
      3. Run `nmcli con modify “Wired connection 1” ipv4.method shared`. 
1. If you are on Linux, run `nmcli con up “Wired connection 1”` 
2. Find the Pi’s IP address on your local subnet. 
    - **Windows**: Open PowerShell and run `arp -a`. You should see an interface for 192.168.137.1 and within that section should be an IP address that starts with 192.168.137 and ends with something other than .0   or .1 (ex. 192.168.137.27).  
    - **Linux**: If for some reason you cannot find the IP, confirm the subnet is 10.42.0 by running `ip a`. Look at the section labeled `enxc` and make sure it says “state UP”. You should see labeled something like `inet 10.42.0.1/24`. You can then scan the subnet to find the pi by running `nmap -sn 10.42.0.1/24` and looking for a device that’s not 10.42.0.1. You may need to restart the Pi and give it a minute to boot. 

1. Run `ssh ubuntu@<pi-ip-address>` to connect to the Pi. You can now run commands on the Pi, and transfer files to and from your laptop using SCP (see below).

### SSH over Wi-Fi

This method is nice as it requires less cables and can be used for connecting multiple devices, **however you will have to use one of the other methods such as SSH over Ethernet initially to find the Pi’s internet IP address.** 

For this method, you will need: 
1. Laptop connected to Wi-Fi 
2. Raspberry Pi 5 
3. Pi Power Supply (plugged into wall) 
4. Ethernet cable connected to a router (or to the ethernet port on the wall of the lab) if not connecting the Pi to Wi-Fi

**Process**
1. Plug the ethernet and power cable into the Pi and turn it on.
2. If you do not know what the Pi’s current IP address is, you must first use the Direct Control method above to get access to the terminal. When the Pi first boots, system information is printed to the terminal. In the bottom right corner of this message, you should see a section that says “IPv4 address for eth0: 128.138.189.xxx”. You can also find the IP address by running `ip a` and looking for the address under the eth0 section. This address may change each time the Pi is reconnected to the internet. 
3. Connect your laptop to the UCB Wireless network. 
4. Check if you can find the Pi over the internet by running the command `ping -c 1 128.138.189.xxx` (where xxx is replaced by the Pi’s IP). On Windows, this must be done in PowerShell, not WSL. If it says 0 packets received, then either the IP address is incorrect, or you are not on the same network as the Pi. 
5. If your laptop's public SSH key is not already on the Pi, see the section above for how to add it. 
6. Run `ssh ubuntu@128.138.189.xxx` to connect to the Pi. You can now run commands on the Pi, and transfer files to and from your laptop using SCP (see above).


## Transferring files to and from the Pi

The Raspberry Pi 5 unfortunately does not support data transfer (USB OTG) over its USB 3.0 ports. Fortunately, we can make use of the SSH connection to send files to and from the Pi using SCP and/or GitHub. 

If you have committed changes to the code and pushed them to GitHub, you can just checkout the correct branch and run `git pull` on the Pi to see them. However, if you are debugging or making small changes to a file that aren’t worthy of a commit, you can send files directly with SCP by running the following command on your laptop. 

Send a single file with `scp <my-file-path> ubuntu@<pi-ip-address>:<pi-directory-path>`. 
* Windows: `scp sdr/main.cpp ubuntu@192.168.137.10:~/uhd_radar/sdr/`
* Linux: `scp sdr/main.cpp ubuntu@10.42.0.10:~/uhd_radar/sdr/`

You can also send a whole folder with `scp -r <my-directory-path> ubuntu@<pi-ip-address>:<pi-directory-path>`. 

To send files from the Pi back to your laptop, reverse the two arguments ensuring the first is one or more files, or directory, and the second is a directory for where the file should go.  

ex. `scp ubuntu@10.42.0.10:~/uhd_radar/data/20250716* ~/uhd_radar/data/`. 

# Indoor Testing

While indoors, make sure **not** to transmit any signals with the antenna. Only transmit into the spectrum analyzer or in a loopback configuration to the SDR. 

**Before doing any testing in a loopback configuration, use the spectrum analyzer to confirm that the transmitted power is less than the maximum input power the SDR can handle.** 

When connecting any SMA cable, make sure to hold the cable and connection point still while you connect it so that the cable **does not spin** as you tighten the nut, as this can cause damage to the pin. Tighten the nut using the SMA torque wrench (the wrench will bend when the proper tightness is reached). 

## Spectrum Analyzer:
To test the program with the spectrum analyzer, you will need the following equipment: 
* b205mini SDR 
* USB 3.0 Micro B cable (connecting SDR to Pi) 
* Raspberry Pi 5 
* Raspberry Pi 5 Power Supply (USB C) 
* Ethernet cable (connecting Pi to Laptop) 
* Ethernet to USB C adapter (if your laptop doesn't have ethernet) 
* 30 dB inline attenuator 
* 2 SMA male-male cables 
* SMA female-female adapter (or replace one of the male-male cables with a male-female cable) 
* SMA torque wrench 
* SMA female to N-Type male adapter (probably plugged into the spectrum analyzer RF Input port already) 
* Spectrum Analyzer (Rigol DSA832-TG) 
* 50 Ohm Load (Found in the Calibration Kit F604MS) 

**Process**
1. Ensure the blue ESD mat is properly grounded, and there are no food or drinks nearby. 
2. Carefully take the 50 Ohm Load out of the calibration kit box. Be very careful while handling this piece of equipment.  
3. Connect 50 Ohm Load to the “RX2” port on the SDR, ensuring that the load does not spin while the nut is being tightened. Tighten it using the torque wrench. 
4. Connect this cable to the SMA female-female adapter. 
5. Connect the SMA female-female adapter to the “IN” port on the 30 dB attenuator. 
6. Connect the other SMA cable to the “OUT” port on the 30 dB attenuator.  
7. Connect this SMA cable to the SMA female to N-Type adapter. 
8. Connect the SMA female to N-Type adapter to the “RF Input” port on the spectrum analyzer if it is not already connected. Take special care that the adapter does not spin while connecting it to this port. 
9. Turn on the spectrum analyzer.
10. Set the Spectrum Analyzer's frequency to the chirps' configured center frequency. 
11. Set the span of the spectrum analyzer to a bandwidth that allows you to see your full chirp in detail. 
12. Configure your spectrum analyzer to see the maximum value when sampled. 
13. Follow the steps in the sections above to connect your laptop to the Pi and get all the code ready to run on the Pi. 
14. Plug the USB 3.0 Micro B cable into one of the blue USB ports on the Pi and plug the other end into the SDR. 
15. Follow the Running the Code section below on how to run the program. 
16. When the code is running, you should see the transmissions appear on the spectrum analyzer. To see the peak transmitted power, press “Peak”. Ensure that this value is less than the SDR’s max input power before doing any loopback or outdoor testing. 
17. Since the SDR is not receiving any samples, you will see receiver errors printed to `uhd_stdout.log`, and `rx_samps.bin` will be empty.

## Loopback Configuration: 

To get any actual data from the SDR, we must both transmit and receive signals by connecting the SDR to itself in a loopback configuration. 

**Before running the program in this configuration, make sure that you have tested your current code and config settings with the spectrum analyzer method above, and that the peak power is less than the SDR’s max input power (-15 dBm)!** 

**When connecting the b205mini to itself, you should always use a 30 dBm attenuator!**

1. Follow the steps in the Spectrum Analyzer section above to set up the hardware and test it with the spectrum analyzer. Confirm that the program works and the peak power is less than -15dBm. 
2. Stop all transmissions, and do not transmit again until everything has been reconnected. You can unplug the SDR from the Pi to ensure this cannot happen. 
3. Disconnect the SMA cable from the adapter on the spectrum analyzer. 
4. Carefully disconnect the 50 Ohm Load and place it back in the box. 
5. Connect the SMA cable to the “RX2” port on the SDR. 
6. Plug the SDR back into the Pi if you disconnected it previously. 
7. Follow the Running the Code section below to run the program.

# Running the Code: 
Now that you’re connected to the Pi and have hardware set up, you can run the code with the following commands: 

1. `cd uhd_radar/` 
2. `conda activate uhd`
3. Check your config settings are set correctly with `nano config/<your-file>.yaml` 
4. With the b205mini make sure the following values in the RF0 (not RF1) section are set: tx_gain should not exceed ~80 dB (max possible is 89.8 dB), rx_gain should not exceed 76 dB, tx_ant should be set to “TX/RX”, rx_ant should be set to “RX2” and transmit should be set to true. 
5. run `make hardware-test` 
6. run `python run.py config/<your-file>.yaml` 
7. If you have num_pulses set to -1, then you must stop the program with Ctrl+C. 
8. To view the output data, transfer it to a laptop (see above), ensure the PLOT section has been copied to the config file (it can be found in any of our previous outdoor tests, or the synthetic-config.yaml) and update the parameters in that section. 
9. Plot the output with `python postprocessing/plot_samples.py data/<timestamp>_config.yaml` 


