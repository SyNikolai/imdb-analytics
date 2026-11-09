import os

import requests


class IMDbDownloader:
    """ Class to find and download the .tsv.gz file links on the IMDB dataset page """

    def __init__(self, url: str="https://datasets.imdbws.com/", data_dir: str="data", chunk_size: int = 1024^2) -> None:
        self.url = url
        self.data_dir = data_dir
        self.chunk_size = chunk_size # defaulted to 1 MB
        self.session = requests.Session() # establish a connection for each instance of the downloader class

    def find_links(self) -> list[str]:
        """ class method to find and return as a list of strings the links corresponding to .tsv.gz files """
        page = self.session.get(self.url, timeout=30)
        page.raise_for_status()

        links = []
        for piece in page.text.split('href="')[1:]:
            link = piece.split('"')[0]
            if link.endswith(".tsv.gz") and link not in links:
                links.append(link)
        return links

    def download(self, link: str) -> str:
        """ class method to download in chunks (stream) one file into the data_dir and return the path that it was saved to as a string """
        dest = f"{self.data_dir}/{link.split('/')[-1]}"
        print(f"Downloading {dest}")

        with self.session.get(link, stream=True, timeout=60) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            done = 0

            with open(dest, "wb") as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    f.write(chunk)
                    done+= len(chunk)
                    self._show_progress(done, total)
        print()
        return dest

    @staticmethod
    def _show_progress(done: int, total: int) -> None:
        """ private class method to show porgress while downloading the files """
        if total:
            print(f"\r {done / 1e6:,.0f} / {total / 1e6:,.0f} MB ({done / total:.0%})", end="", flush=True)
        else:
            print(f"\r {done / 1e6:,.0f} MB", end="", flush=True)
    
    def run(self) -> list[str]:
        """ class method to run the download process and complete the task of saving the relebvant data; returns the list of all saved paths """
        os.makedirs(self.data_dir, exist_ok=True)
        links = self.find_links()

        if not links:
            raise SystemExit(f"No .tsv.gz links found in {self.url}")

        paths = [self.download(link) for link in links]
        print(f"Done: {len(paths)} files in {self.data_dir}/")

        return paths

def main() -> None:
    IMDbDownloader().run()


if __name__ == "__main__":
    main()