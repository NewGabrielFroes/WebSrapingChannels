import undetected_chromedriver as uc

from selenium import webdriver

from bs4 import BeautifulSoup

from time import sleep


def main():
	channels = {
		'benfica_tv': 'https://www.livesoccertv.com/channels/benfica-tv/',
		'eleven_sports_5': 'https://www.livesoccertv.com/channels/eleven-sports-5-portugal/',
		'eleven_sports': 'https://www.livesoccertv.com/channels/eleven-sports-portugal/'
	}

	driver = config_selenium()

	print(get_channels_schedules_by_channels(channels, driver))

	driver.close()

def get_channels_schedules_by_channels(channels, driver):
	channels_schedules = {}

	for channel in channels:
		driver.get(channels[channel])

		site = BeautifulSoup(driver.page_source, 'html.parser')

		table = site.find('table', {'class': 'schedules'})

		channel_schedule = []

		for row in table.find_all('tr'):
			is_having_a_live_match = row.find('span', {'class': 'narrow'}).text != ''
			if is_having_a_live_match: continue
			
			time = row.find('td', {'class': 'timecell'}).text
			date = row.find('td', {'class': 'datecell'}).text
			teams = row.find('td', {'class': None}).text
			competition = row.find('td', {'class': 'compcell_right'}).text

			datetime = date.strip() + time.strip()
			datetime = datetime.replace(' ', '')
		
			competition = competition.strip()
			
			teams = teams.split('x')
			
			home_team = teams[0].strip()
			away_team = teams[1].strip()

			schedule = {
				'datetime': datetime,
				'home_team': home_team,
				'away_team': away_team,
				'competition': competition 
			}

			channel_schedule.append(schedule)


		channels_schedules[channel] = channel_schedule 

	return channels_schedules


def config_selenium():
	options = webdriver.ChromeOptions() 

	options.add_argument('--headless')

	driver = uc.Chrome(options=options)

	return driver


if __name__ == '__main__':
    main()		
