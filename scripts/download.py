#!/usr/bin/python
# This script allows to download the data (currently 2015-2025) from marine cadastre

from argparse import ArgumentParser
import subprocess
import calendar
from pathlib import Path
from tqdm import tqdm

def download_year(year: int, output_dir: Path | None = None):
    year_dir = Path(str(year)) 
    year_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Download data for {year=}")
    for month in tqdm(range(1,13), desc="months", total=12):
        _, max_month = calendar.monthrange(year, month)
        for day in tqdm(range(1, max_month+1), desc="days", total=max_month, leave=False):
            filename = f"AIS_{year}_{month:02}_{day:02}.zip"

            output_filename = year_dir/ filename

            if not Path(output_filename).exists():
                directory_prefix = year_dir
                if output_dir:
                    directory_prefix = Path(output_dir) / year_dir
                subprocess.run(["wget", f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}/{filename}", "--directory-prefix", directory_prefix, "-o", "download.log"])


def run(from_year, to_year, output_dir):
    for year in range(from_year, to_year + 1):
        download_year(year, output_dir)


if __name__ == "__main__":
    parser = ArgumentParser(
            description="Download data from marine cadastre"
    )
    parser.add_argument("--output-dir",
            type=str,
            default=None,
            help="The output directory for the data"
    )
    parser.add_argument("--from-year",
            type=int,
            default=2015,
            help="Download data from this year (default: 2015)"
    )
    parser.add_argument("--to-year",
            type=int,
            default=2024,
            help="Download data until this year (default: 2024)"
    )

    args, unknown = parser.parse_known_args()
   
    run(args.from_year, args.to_year, args.output_dir)
