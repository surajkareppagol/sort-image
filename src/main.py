from shutil import rmtree

from rich.progress import Progress

import util
from sort import SVSort
from term import r_print, status


def main() -> None:
    args = util.sv_parse_args()

    directory = "sv"

    # Get image
    image = util.sv_parse_image(args.image)

    if image is None:
        r_print("[bold red]Error[/bold red]: Invalid image file.")
        exit(1)

    # Get split size
    split = int(args.split) if args.split else 50

    # Algorithm
    algorithm = int(args.algorithm) if args.algorithm else 0

    # Video Formatter
    formatter = args.video_formatter

    w, h = image.size
    splits = (w // split) * (h // split)

    util.sv_create_merge_dir()

    # Process Image
    with status("Splitting image into pieces...", spinner="dots9"):
        images = util.sv_split_image(image, split)

    with Progress() as progress:
        task = progress.add_task(
            f"Generating {splits} images...", total=splits)

        array = util.sv_generate_array(splits)
        sorter = SVSort(array)
        sort = sorter.sort(algorithm)

        for index, iteration in enumerate(sort()):
            util.sv_merge_image(image, images, iteration, index, split)
            progress.update(task, advance=1)

    video = [algo.__name__ for algo in sorter.algorithms][algorithm] + ".mp4"

    if formatter == "opencv":
        util.sv_create_video_opencv(directory, video)
    else:
        with status("Creating video with ffmpeg...", spinner="dots9"):
            util.sv_create_video_ffmpeg(directory, video)

    rmtree(directory, ignore_errors=True)

    r_print("🚀 Video generated.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        rmtree("sv/", ignore_errors=True)
        r_print("[bold red]Error[/bold red]: Interrupted.")
        exit(1)
    except Exception as exception:
        rmtree("sv/", ignore_errors=True)
        r_print("[bold red]Error[/bold red]: Exception occurred.")
        r_print(exception)
        exit(1)
