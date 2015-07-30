# manga-scraper
Just a casual manga scraper to get latest chapters info

## What does it do
This is just a simple tool to get the info of latest chapters.  
The data is directly scraped from [MangaPanda].  
Basically, you just have to provide the manga names. If the name has multiple words, be sure to input space separated ones.  

## Ok! I want to use it. But how?
#### Clone this repo first

```bash
git clone https://github.com/NISH1001/manga-scrapper.git
```

#### Dependencies
I have used **python3**. So you should have to use pip for python3 ie **pip3**.
You need python's **requests** and **BeautifulSoup** modules

```bash
sudo apt-get install python3-pip
```

```bash
sudo apt-get install python3-requests
```

```bash
sudo pip3 install beautifulsoup4
```

## Usage
Just hit the following command in your terminal and just enter the manga name after that.  
```bash
python3 mangascraper.py
```

[MangaPanda]:http://mangapanda.com/
