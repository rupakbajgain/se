import logging
from pathlib import Path
from typing import Dict, Iterator, Union
from ...page import Page

from langchain_core.documents import Document

from langchain_community.document_loaders.base import BaseLoader

#copied blindly
class HTMLLoader(BaseLoader):
    """Load `HTML` files and parse them with `beautiful soup`."""

    def __init__(
        self,
        url: str,
        file_path: str,
        open_encoding: Union[str, None] = None,
        bs_kwargs: Union[dict, None] = None,
        get_text_separator: str = "",
    ) -> None:
        """initialize with path, and optionally, file encoding to use, and any kwargs
        to pass to the BeautifulSoup object.

        Args:
            url: The url of source.
            open_encoding: The encoding to use when opening the file.
            bs_kwargs: Any kwargs to pass to the BeautifulSoup object.
            get_text_separator: The separator to use when calling get_text on the soup.
        """
        try:
            import bs4  # noqa:F401
        except ImportError:
            raise ImportError(
                "beautifulsoup4 package not found, please install it with "
                "`pip install beautifulsoup4`"
            )

        self.url = url
        self.file_path = file_path
        self.open_encoding = open_encoding
        if bs_kwargs is None:
            bs_kwargs = {"features": "lxml"}
        self.bs_kwargs = bs_kwargs
        self.get_text_separator = get_text_separator

    def lazy_load(self) -> Iterator[Document]:
        """Load HTML document into document objects."""
        from bs4 import BeautifulSoup

        p=Page(self.url)
        glinks = p.get_filtered_links(filter=False)#custom filter
        
        soup = p.get_soup()

        for i in soup.find_all('a'):
            h=i.get('href')
            if h:
                if h in glinks:
                    i.string = f'[{i.string}]({h})'
                else:
                    i.string = ''#no text if bad link

        text = soup.get_text(self.get_text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        #add title to text
        text = f"#{title}\n\n" + text

        metadata: Dict[str, Union[str, None]] = {
            "source": str(self.file_path),
            "title": title,
        }
        yield Document(page_content=text, metadata=metadata)
