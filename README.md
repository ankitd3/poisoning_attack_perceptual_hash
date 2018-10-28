# Hash Poisoning Attack and Steganography Attack with mitigation using MD5 Hash

### Use Case (Reference [link](https://towardsdatascience.com/black-box-attacks-on-perceptual-image-hashes-with-gans-cc1be11f277))
A system that allows users to submit photos to a database of images to ban. 
A human reviews the image to ensure it is an image that deserves banning (and that the image is say, not the Coca-Cola logo). If approved, this hash gets added to the database and is checked against whenever a new image is uploaded. If this new image’s hash collides with the banned hash, the image is prevented from being uploaded.

![Block](https://i.imgur.com/7HcvZQ3.png?1)

## Usage

1. Run the (Server side) - "app.py" (For phase 1 use case) and "app_steg.py" for steganography check (Not simultaneously)
2. Run test.py alog with app.py
3. Change the IP Address to your IP address in both app.py and app_steg.py for access to clients in your network
