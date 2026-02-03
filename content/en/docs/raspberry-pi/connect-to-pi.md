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



