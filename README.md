# 📶 Sort Image

Inspiration for this project is the following post from [Reddit](https://www.reddit.com/r/ProgrammerHumor/comments/cyrlvp/learn_sorting_algorithm_with_kronk/).

---

## 👷 Architecture

The flow of data is as follows: `PIL` is used for image manipulation, and either `ffmpeg` or `opencv` can be used to combine the generated images into a video.

!["Architecture"](./docs/images/architecture.jpg)

---

## ⚙️ Usage

- Install `ffmpeg` (If you want to use it instead of `opencv`).

```sh
sudo apt install ffmpeg
```

- Clone the repository:
```sh
git clone <https://github.com/surajkareppagol/sort-image>
cd sort-image
```

- Set up a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies:

```sh
pip install -r requirements_ffmpeg.txt
# OR
pip install -r requirements_opencv.txt
```

- Run the script:

```sh
python3 src/main.py <path_to_image>
```

---

## Additional Arguments
1. **Split Size**
Control the size of splits (default is `50`):
```sh
python3 src/main.py <path_to_image> -s 50
```

2. **Sorting Algorithm**
Select the sorting algorithm by index:
```sh
python3 src/main.py <path_to_image> -s 100 -a 2
```
Here -a 2 selects Insertion Sort. Available algorithms can be seen below.

3. **Video Formatter**
Choose between `ffmpeg` and `opencv` (default is `ffmpeg`):

```sh
python3 src/main.py <path_to_image> -v opencv
```

---

## 📶 Sorting Algorithms
The following algorithms are available:

0. `Bubble Sort`
1. `Selection Sort`
1. `Insertion Sort`
1. `Merge Sort`
1. `Quick Sort`
1. `Heap Sort`
 
Each algorithm creates a visually unique sorting video, making it easier to understand the sorting process.

---

## 📦 Dependencies
* Python 3.8+
* **`PIL`** (Pillow) for image manipulation
* **`ffmpeg`** or **`opencv`** for video creation

Install one of the following based on your preference:
* `requirements_ffmpeg.txt` (for `ffmpeg` support)
* `requirements_opencv.txt` (for `opencv` support)