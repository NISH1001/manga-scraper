#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import datetime
from exception import MangaError

def remove_newline(text):
    return re.sub(r'\n+', '', text)


"""
MangaScraper
    - accepts space separated manga name

attributes:
    - url : http://www.mangapanda.com/
    - latest_chapters : list for latest chapters with no date info
    - latest_chapters_time : list for latest chapters with date info

methods:
manganame_dashed():
    -function to return dashed names for space separated

scrap():
    - scraps the mangapanda from div element of latestchapters
    - faster because of scrapping from this 'latestchapters' div
    - contains no date info

scrap_with_time():
    - scraps the mangapanda from the table of all chapters
    - slower due to all chapter from first to lastest
    - contains date info too
"""
class MangaScraper(object):

    ''' accept manga name'''
    def __init__(self, manga_name):
        self.manga_name = self.manganame_dashed(manga_name.strip())
        self.url = "http://www.mangapanda.com/"
        self.chapters = []
        self.latest_chapters = []
        self.latest_chapters_time = [] # is actually a list of tuple -> (chapter full name, dateinfo)

    ''' convertes spaces to dash'''
    def manganame_dashed(self, manga):
        name = manga.lower()
        spaces_removed = re.sub(r'(\s+)|(:\s*)+', '-', name)
        return spaces_removed

    ''' scrap from latestchapters div'''
    def scrap(self):
        # get the response
        response = requests.get(self.url + self.manga_name)
        try:
            if response.status_code != 200:
                raise MangaError("oh shit. \nEither manga is invalid(not available) or your internet is retarded :D")

            else:
                # root extractor
                extractor = BeautifulSoup(response.content, "html.parser")

                # get this div
                div_latest = extractor.find("div", {'id' : 'latestchapters'})

                # find all the chapter list
                latest_list = div_latest.find_all(['li'])

                self.latest_chapters = [ remove_newline(x.get_text()) for x in latest_list if x ]
                return self.latest_chapters

        except MangaError as merr:
            merr.display()
            return ''

    """ scraps the chapters with date info"""
    def scrap_with_time(self):
        response = requests.get(self.url + self.manga_name)
        try:
            if response.status_code != 200:
                raise MangaError("oh shit. \nEither manga is invalid(not available) or your internet is retarded :D")

            else:
                extractor = BeautifulSoup(response.content, "html.parser")
                table = extractor.find("table", {'id' : 'listing'} )
                rows = table.find_all('tr')[-5:]
                rows = rows[::-1]

                for row in rows:
                    data = [ remove_newline(td.get_text()) for td in row.find_all('td') if td]
                    """
                    for td in row.find_all('td'):
                        print(td.get_text())
                    """
                    self.latest_chapters_time.append(tuple(data))
                return self.latest_chapters_time

        except MangaError as merr:
            merr.display()
            return ''

    def display(self, with_time=False):
        print(re.sub(r'[-]+', ' ', self.manga_name), " : latest chapters")
        print("-"*80)

        if not with_time:
            for chapter in self.latest_chapters:
                print(chapter)

        else:
            # latest_chapters_time is tuple -> (chapter full name, dateinfo)
            for chapter in self.latest_chapters_time:
                chapter_full = chapter[0]
                chapter_name = ''.join( re.split(r':', chapter_full)[-1:] )
                chapter_num = ''.join(re.findall(r'\d+\s+', chapter_full))

                #format_string = "mm/md/YYYY"
                date_str = chapter[1]
                date_list = date_str.split('/')

                # year, month, day
                dt = datetime.date(int(date_list[2]), int(date_list[0]), int(date_list[1]))
                humanize = dt.strftime("%A %B %d, %Y")
                print("{:5s} : {:50s} {}".format(chapter_num, chapter_name, humanize))


def main():
    name = input("Enter the manga name(spaces separated): ")
    manga = MangaScraper(name)
    chapters = manga.scrap_with_time()
    chapters = manga.scrap()
    if chapters:
        manga.display(with_time=False)



if __name__=="__main__":
    main()




