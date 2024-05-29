import asyncio
from pyppeteer import launch
import csv


async def scrape_indeed():
    browser = await launch(headless=False)
    page = await browser.newPage()


    await page.goto('https://www.indeed.com')


    await page.waitForSelector('#text-input-what')
    await page.waitForSelector('#text-input-where')

    #clear the form value to an empty string
    await page.evaluate('''() => {
    document.querySelector('#text-input-what').value = ''
}''')
    
    await page.type('#text-input-what', 'Lobbyist')

    await page.evaluate('''() => {
    document.querySelector('#text-input-where').value = ''
}''')
    await page.type('#text-input-where', 'USA')


    await page.click('button[type="submit"]')


    await page.waitForNavigation()


    job_listings = await page.querySelectorAll('.resultContent')
    all_jobs = []
    for job in job_listings:
        # Extract the job title
        title_element = await job.querySelector('h2.jobTitle span[title]')
        title = await page.evaluate('(element) => element.textContent', title_element)
        #print("this is the title: ", title)


        # Extract the company name
        company_element = await job.querySelector('div.company_location [data-testid="company-name"]')
        company = await page.evaluate('(element) => element.textContent', company_element)


        # Extract the location
        location_element = await job.querySelector('div.company_location [data-testid="text-location"]')
        location = await page.evaluate('(element) => element.textContent', location_element)

        new_job = {'title': title, 'company': company, 'location': location}
        print({'title': title, 'company': company, 'location': location})
        all_jobs.append(new_job)

    with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Location'])
        for job in all_jobs: 
            writer.writerow([job['title'], job['company'], job['location']])

    await browser.close()
            
"""
This function will take a number n and click through all pages up to n
"""
async def numPagesSearch(n):
    pass


    


# Run the coroutine
if __name__ == '__main__':
    asyncio.run(scrape_indeed())
