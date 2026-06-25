---
title: SSH
linktitle: Basics of SSH
description: If you already know how SSH works you don't need to read this. The goal is to gain a basic understanding of what SSH is. 
weight: 10
---
<!-- HAVE SOMEONE FACT CHECK THIS BECAUSE OTHERWISE ITS THE BLIND LEADING THE BLIND :fear: -->

SSH stands for secure shell. This is another way to connect to other cloud services or devices without needing to login each time. SSH is being used here with GitHub and the Raspberry Pi. You can clone a repository using SSH and you can connect to your Raspberry Pi's terminal from your laptop using SSH.

Whenever you generate a key on your laptop, it creates both a public and private version. The public version is what you give to things like GitHub or the Raspberry Pi. The private key is what you keep on your laptop and don't share with anyone. 

Whenever you try to connect to something, like GitHub with the SSH key, something happens where the public and private key are compared and verified. Then GitHub is like cool, you're you, and allows you to clone repositories. 

To connect to your Raspberry Pi's terminal from your laptop, you first give it the public key. After it is connected to the wifi, it is able to copy it from GitHub. Further details are in the setting up your Raspberry Pi page. Then when you try to connect to the Raspberry Pi, the two keys are compared. After verification, you then can access the Pi's terminal. If verification fails, you can't access the terminal. 

<!-- HAVE ROWAN TEST, after he makes a ssh key, can he connect to the Pi? or then after it gets the public key can it connect -->

{{% pageinfo %}}
Back to [ORCA setup](/docs/radar/setupguide/ORCAsetup) or continue to [Raspberry Pi setup](/docs/radar/setupguide/RaspPi).

{{% /pageinfo %}}