import argparse
from argparse import ArgumentParser, Namespace
from os import mkdir, path, listdir
from random import shuffle
from shutil import rmtree
from sys import exit

from PIL import Image
from PIL.Image import Image as ImageType
from PIL.ImageFile import ImageFile as ImageFileType

from term import r_print


def sv_parse_image(image: str) -> ImageFileType | None:
    if path.exists(image):
        return Image.open(image)
    else:
        return None


def sv_create_merge_dir() -> None:
    if not path.exists("sv"):
        mkdir("sv")
    else:
        rmtree("sv/", ignore_errors=True)
        mkdir("sv")


def sv_create_video_ffmpeg(directory: str, output: str) -> None:
    import ffmpeg

    glob = f"{directory}/*.jpg"

    try:
        ffmpeg.input(glob, pattern_type="glob", framerate=30).output(
            output, loglevel="quiet"
        ).run(overwrite_output=True)
    except Exception:
        r_print("[bold red]Error[/bold red]: FFMPEG Failed with error.")
        exit(1)

def sv_create_video_opencv(directory: str, output: str) -> None:
    import cv2
    from rich.progress import Progress

    images = sorted([img for img in listdir(
        directory) if img.endswith(".jpg")])

    try:
        if not images:
            r_print("[bold red]Error[/bold red]: No images found in the directory.")
            return

        frame = cv2.imread(path.join(directory, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(
            output, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

        with Progress() as progress:
            task = progress.add_task("Creating video...", total=len(images))
            for image in images:
                img = cv2.imread(path.join(directory, image))
                video.write(img)
                progress.advance(task)

        video.release()
    except Exception:
        r_print("[bold red]Error[/bold red]: OpenCV Failed with error.")
        exit(1)


def sv_parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="sort-image", description="Visualize sorting algorithms via images."
    )

    def valid_algorithm(value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(
                "Invalid input. Algorithm number must be an integer.")

        from sort import SVSort

        valid_algorithms = len(
            [algo.__name__ for algo in SVSort([]).algorithms])

        if value not in range(valid_algorithms):
            raise argparse.ArgumentTypeError(
                f"Invalid algorithm. Choose from {(valid_algorithms)}.")
        return value

    parser.add_argument("image", type=str, help="Path to the image")
    parser.add_argument("-s", "--split", type=int,
                        help="Size of splits (Default is 50)", required=False)
    parser.add_argument("-a", "--algorithm", type=valid_algorithm,
                        help="Sorting algorithm to use", required=False)
    parser.add_argument("-v", "--video-formatter", choices=[
                        "ffmpeg", "opencv"], required=False, help="Choose video processing tool: ffmpeg or opencv")

    args = parser.parse_args()

    return args


def sv_generate_array(size: int) -> list[int]:
    array = list(i for i in range(size))
    shuffle(array)

    return array


def sv_split_image(image: ImageFileType, split: int) -> list[ImageType]:
    split_images: list[ImageType] = []

    w, h = image.size
    w, h = w // split, h // split

    left = 0
    upper = 0
    right = split
    lower = split

    counter = 0

    for _ in range(h):
        for _ in range(w):
            img = image.crop((left, upper, right, lower))
            split_images.append(img)

            counter += 1

            left += split
            right += split

        left = 0
        upper += split
        right = split
        lower += split

    return split_images


def sv_merge_image(
    image: ImageFileType,
    images: list[ImageType],
    array: list[int],
    count: int,
    split: int,
) -> None:
    w, h = image.size
    w, h = w // split, h // split

    img = Image.new("RGB", image.size)

    left = 0
    upper = 0
    right = split
    lower = split

    counter = 0

    for _ in range(h):
        for _ in range(w):
            img.paste(images[array[counter]], (left, upper, right, lower))

            counter += 1

            left += split
            right += split

        left = 0
        upper += split
        right = split
        lower += split

    img.save(f"sv/{count:010}.jpg")
