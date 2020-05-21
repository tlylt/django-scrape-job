from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

from scraping.models import Job

class Command(BaseCommand):
    help = "collect jobs"

    # define the logic of command
    def handle(self,*args,**options):
        # collect html
        html = urlopen("https://sg.indeed.com/jobs?q=web+developer+intern&l=Singapore&sort=date&start=20")
        
        # convert to soup
        soup = BeautifulSoup(html,'html.parser')

        # grab all postings
        postings = soup.find_all("div", class_="jobsearch-SerpJobCard unifiedRow row result")

        # Indeed address
        address = 'https://sg.indeed.com'
        for p in postings:
            item = p.find('a',class_="jobtitle turnstileLink")
            url = address+item['href']
            title = item['title']
            company = p.find('span',class_="company").text.lstrip()
            try:
                salary = p.find('span',class_="salaryText").text
            except AttributeError:
                salary = "Salary undisclosed"
            
            # check if url in db
            try:
                #save in db
                Job.objects.create(url=url,title=title,company=company,compensation=salary)
                print(f'{title} added')
            except:
                print(f'{title} already exists')
        self.stdout.write('job complete')
        
    
    