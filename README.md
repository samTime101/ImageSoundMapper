# IMAGE SOUND MAPPER

![Author](https://img.shields.io/badge/author-samip--regmi-blue)

---

## IMAGE TO SOUND

Following is the algorithm I used to convert image to sound:

### 1. RESIZE
* Resizes the source image to specified image size

### 2. GRAYSCALE
* Converts the resized image to grayscale whose pixel value can be mapped from `0-255`

### 3. PIXEL TO FREQUENCY
* Each pixel from `0-255` is mapped to frequency from `200-1000` using linear mapping

### 4. AUDIO FILE IS SAVED
* Those mapped frequencies are saved in each `0.01` second of the audio file, holding `441` samples each  
* with total frequency data being size of resized image  
* **default: 50 x 50 = 2500**

---

## SOUND TO IMAGE

### 1. AUDIO CHUNK DETECTION
* As duration per frequency is known, we extract all the chunks of data.  
* Each chunk holds `441` samples, in total `2500` chunks.

### 2. CHUNKS TO FREQUENCY
* We then use **librosa** to find the frequency of each chunk

### 3. FREQUENCY TO PIXEL
* Using linear mapping we convert the frequencies back to pixels

### 4. PIXEL TO IMAGE
* Finally, all the pixel data is saved back into the image

---

[> Demo](https://github.com/user-attachments/assets/e2eb8ffb-ca62-479e-a699-af40396a8966)


## CLONING

* clone the repo using `git clone <remote-url>` u can use **ssh** or **https**
* after cloning install required dependencies using `pip install -r requirements.txt`
* add and correct the required paths in **main.py**
* run the program using `python3 main.py`