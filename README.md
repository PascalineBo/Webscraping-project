# Web Scraping progam
This code's purpose is to scrape (http://books.toscrape.com)

## Requisits: 

Install Python : download **[Python 3.10](https://www.python.org/downloads/)** 

## Program's set up:
  <ol>
  <li>import the repository's files:

`git clone https://github.com/PascalineBo/Webscraping-project.git`</li>
  
  <li> navigate to the folder:
    
- `cd Webscraping-project` </li>
<li> create your virtual environment folder:

- `mkdir .venv`
- `pip install pipenv`
</li>
<li> then install packages requirements:

- `pipenv install beautifulsoup4`
- `pipenv install bs4`
- `pipenv install certifi`
- `pipenv install charset-normalizer`
- `pipenv install idna`
- `pipenv install requests`
- `pipenv install soupsieve`
- `pipenv install urllib3`
    </li>
<li> activate your virtual environment in your terminal:
    
- `pipenv shell`
    </li>
<li> run the script:
  
- `python main.py`
- answer the question: key in `Data`or `Pics`
- the file main.py allows you to run the script; 
  
  the file projet2g.py contains the code necessary to srape data into csv files; 
  
  the file projet2image.py contains the code necessary to scrape pictures from the website;
</li>
  <li>see all the data you scraped in csv output files in your folder or 
  the scraped pictures in categories' directories</li>
(Note: program's run time superates 20 minutes) 
  </ol>
