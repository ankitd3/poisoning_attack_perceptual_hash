# Hash Poisoning Attack and Steganography Attack with mitigation using MD5 Hash

## Abstract

Our project detects a hash poisoning attack, in which the poison image having the same hash of the innocent image is uploaded and causes a denial of service to the legitimate users trying to upload, but because it has the same hash as that of poison image, the system compares the hash with the hash table and deletes the innocent image.
We aim to mitigate with the help of a counter associated with every hash which maps the hash collisions. If the count increases beyond threshold, system reviews the incoming image while removing the hash entry from the database. In the second phase, we take into consideration the poison images modified using steganography methods that transfers unwanted malicious files along with the image uploads. 
We use the message authentication mechanism incorporating the use of MD5 hash which is sent along with the image and is verified at the server side.

#### Use Case (Reference [link](https://towardsdatascience.com/black-box-attacks-on-perceptual-image-hashes-with-gans-cc1be11f277))
A system that allows users to submit photos to a database of images to ban. 
A human reviews the image to ensure it is an image that deserves banning (and that the image is say, not the Coca-Cola logo). If approved, this hash gets added to the database and is checked against whenever a new image is uploaded. If this new image’s hash collides with the banned hash, the image is prevented from being uploaded.

![Block](https://i.imgur.com/7HcvZQ3.png?1)

## Usage

1. Run the (Server side) - "app.py" (For phase 1 use case) and "app_steg.py" for steganography check (Not simultaneously)
2. Run test.py alog with app.py
3. Change the IP Address to your IP address in both app.py and app_steg.py for access to clients in your network
