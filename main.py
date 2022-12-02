from selenium import webdriver
from bs4 import BeautifulSoup
import time

result = {}

def openLinkedinAndLogin(email,password,profileURL):
    driver = webdriver.Chrome()

    driver.get("https://linkedin.com/uas/login")

    time.sleep(5)

    username = driver.find_element('id',"username")

    username.send_keys(email) #Entering email

    pword = driver.find_element('id',"password")

    pword.send_keys(password)	#Entering password

    driver.find_element('xpath',"//button[@type='submit']").click()

    profile_url = profileURL #Entering a profile URL to scrape

    driver.get("https://www.linkedin.com/in/abhinavvsinhaa/")
    time.sleep(10)
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        
        time.sleep(5)
        end = time.time()

        if round(end - start) > 20:
            break

    src = driver.page_source
    
    # Using BeautifulSoup
    soup = BeautifulSoup(src, 'html.parser')
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()
    
    
    location_loc = intro.find_all("span", {'class': 'text-body-small'})
    location = location_loc[1].get_text().strip()
    result.name = name
    result.works = works_at
    result.location = location

    experience = soup.find("section", {"id": "experience-section"}).find('ul')
    li_tags = experience.find('div')
    a_tags = li_tags.find("a")
    job_title = a_tags.find("h3").get_text().strip()
    
    result.jobTitle = job_title
    
    company_name = a_tags.find_all("p")[1].get_text().strip()
    result.companyName = company_name
    
    joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()
    
    employment_duration = a_tags.find_all("h4")[1].find_all(
        "span")[1].get_text().strip()

    result.employment = joining_date + ", " + employment_duration

    jobs = driver.find_element('xpath',"//a[@data-link-to='jobs']/span")
    
    jobs.click()

    job_src = driver.page_source
    
    soup = BeautifulSoup(job_src, 'html.parser') 
    jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
    job_titles = []
    
    for title in jobs_html:
        job_titles.append(title.text.strip())
    
    result.jobTitles = job_titles

    company_name_html = soup.find_all(
    'div', {'class': 'job-card-container__company-name'})
    company_names = []
    
    for name in company_name_html:
        company_names.append(name.text.strip())
    
    result.companyNames = company_names

    return result