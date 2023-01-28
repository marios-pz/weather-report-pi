from bs4 import BeautifulSoup
from time import sleep
from requests import get as get_html
from colorama import init, Fore
import json

# Initialize colorama
init(autoreset=True)

class Weather_Forecast:

    def __init__(self):

        self.website = "https://weather.com/weather/today/l/"

        self.cities = {
            "Athens": "5892dfe2c539df7d42cdbd8f9cfda434f21f6c2a63cec329fa598d4e5aa3d584",
            "Thessaloniki": "4f7940e96197643c80e3c64a7d0ccb4fb6eff7bced4158152da995da08f40053",
            "Patra": "a8c1d5fa8f854f3e5c626109483f1542b6eb8f29924330ccc44ffc07e3050bd7",
            "Iwannina": "7a5351e10b7d52f667e9f0a0b71140bd176ef6cd09edf748f7e28a607baeb3e8"
        }

        # Status
        self.current_status = {

            "Athens": {
                "current_temperature": '',
                "weather": [],
                "temperatures": []
            },

            "Thessaloniki": {
                "current_temperature": '',
                "weather": [],
                "temperatures": []
            },

            "Patra": {
                "current_temperature": '',
                "weather": [],
                "temperatures": []
            },

            "Iwannina": {
                "current_temperature": '',
                "weather": [],
                "temperatures": []
            },
        }

    def get_percentages(self, div_block, city, day_wave = ["Morning", "Noon", "Afternoon", "Night"],  weather_status = "" , percs = []):
        """
            The output should look like  'Morning whether not found' or  'Chance of Raining in the Morning' , %percentage
        """
        for d_index, perc in enumerate(div_block.find_all("div", {"class": "Column--precip--2ck8J"})):
            local_span = perc.span

            # if the percentage was not found, then it was hidden by a child <span>
            for span_child in local_span.find_all("span"):
                weather_status = span_child.string
                span_child.decompose() # Purge span

            if weather_status != "":
                percs.append([weather_status + " in the " + str(day_wave[d_index]) , local_span.string])
            else:
                percs.append(str(day_wave[d_index]) + " weather not found.")
        
        return percs 


    def get_temperatures(self, div_block):
        """
            Gets the temperatures inside the div block
        """
        return [
            temp.span.string[:3] 
            for temp in (
                div_block.find_all("div", {"class": "Column--temp--5hqI_"})
            )
        ]

    def print_weather(self, data, city_name):
        """
            Printing the scrapped data in a fancy way
        """
        city = data[city_name]

        print(f"""     
    {city_name} Currently: {Fore.YELLOW + city['current_temperature'] + Fore.WHITE}

        Morning: {Fore.YELLOW + city['temperatures'][0] + Fore.WHITE}

        Noon: {Fore.YELLOW + city['temperatures'][1] + Fore.WHITE}

        Afternoon: {Fore.YELLOW + city['temperatures'][2] + Fore.WHITE}

        Night: {Fore.YELLOW + city['temperatures'][3] + Fore.WHITE}        
        """)

    def write_data(self):
        """ 
            Cause why not? since I made a dict 
        """
        with open('handmade_api.json', 'w') as f:
            json.dump(self.current_status, f, indent=4)

    def get_data(self):
        """

            Browses through each city and scraps essential data

        """
        for city_name, hash_key in self.cities.items():

            page = get_html(self.website + hash_key)

            # Make soup
            soup = BeautifulSoup(page.content,'html.parser')

            # Gets the main temperature from the top dev block
            curr_temperature = soup.find("div", {"class": "CurrentConditions--primary--2SVPh"})
            self.current_status[city_name]['current_temperature'] = curr_temperature.span.string

            # Take "Today's Forecast block"
            main_block = soup.find("div", {"id": "WxuTodayWeatherCard-main-486ce56c-74e0-4152-bd76-7aea8e98520a"})

            temperatures = self.get_temperatures(main_block)

            percentages = self.get_percentages(main_block, city_name)

            # Save data to dictionary
            self.current_status[city_name]['weather'] = percentages
            self.current_status[city_name]['temperatures'] = temperatures

            self.print_weather(self.current_status, city_name)
    
    def update(self):
        """
            Self explanatory
        """
        self.get_data()
        self.write_data()

w = Weather_Forecast()
if __name__ == "__main__":
    w.update()
