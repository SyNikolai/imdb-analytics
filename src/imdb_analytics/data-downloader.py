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
        """ class method to download in chunks (stream) one file into the data_dir and return the path that it was saved to """
        dest = f"{self.data_dir}/{link.split('/')[-1]}"

