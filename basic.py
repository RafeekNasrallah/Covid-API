import requests
import json
import pycountry_convert as pc
from operator import itemgetter
from itertools import groupby
import operator



class Retriever:
    main_url = 'https://api.covid19api.com/summary'
    country_url = 'https://api.covid19api.com/live/country/%s/status/confirmed'
    country_url_covered = 'https://api.covid19api.com/live/country/%s/status/covered'
    confirmed_dayone = 'https://api.covid19api.com/dayone/country/%s'
    all = 'https://api.covid19api.com/all'


    def update(self):
        resp = requests.get(self.main_url)
        if resp.status_code != 200:
            print('Global Cases GET Request could not be retrieved')
        else:
            self.glob_dict = resp.json()
            self.countries_list = self.glob_dict['Countries']
            self.countries_dict = {}
            for country_dict in self.countries_list:
                self.countries_dict[country_dict['Country']] = country_dict


    def __init__(self):
        self.update()

    
    def dict_global(self):
        return self.glob_dict['Global']


    def dict_country(self, country):
        if country in self.countries_dict:
            return self.countries_dict[country]
        else:
            print('Country %s not valid' % country)
    
    def dict_country_detail(self, country):
        resp = requests.get(self.country_url % country)
        if resp.status_code != 200:
            print('The country is probably invalid')
        else:
            return resp.json()


    def get_allcountries(self): # return list of all country names in small letter!
        return list(map(lambda string : string.lower(), self.countries_dict.keys()))


    def all_countries(self):
        resp = requests.get(self.all)
        json = resp.json()
        first = json[0]['CountryCode']
        last10daysAll = []
        last10daysSpecific = []
        for i in json:
            if i['CountryCode'] == first:
                try:

                    code = pc.country_alpha2_to_continent_code(i['CountryCode'])
                    last10daysSpecific.append((code,i['Confirmed']))
                except:
                    pass
            else:
                last10daysSpecific = last10daysSpecific[-10:]
                if (len(last10daysSpecific) != 0):
                    last10daysAll.append(last10daysSpecific)
                last10daysSpecific.clear()
                first = i['CountryCode']
                try:
                    code = pc.country_alpha2_to_continent_code(i['CountryCode'])
                    last10daysSpecific.append((code,i['Confirmed']))
                except:
                    pass
        print(json)



    def get_sinceDayone(self,country):
        resp = requests.get(self.confirmed_dayone % country)
        json = resp.json()
        dates = []
        cases = []
        for i in json:
            dates.append((i['Date'])[:10])
            cases.append(i['Confirmed'])
        return (dates,cases)



    def countrycode_cases(self): #returns list of tuples (Countrycode,totalcases)
        dictlist = list(self.countries_dict.values())
        info = []
        print(dictlist)
        for n in dictlist:
            info.append((n['CountryCode'],n['TotalConfirmed']))
        continents = []
        for i in info:
            code,confirmed = i
            try:
                continents.append((pc.country_alpha2_to_continent_code(code),confirmed))
            except:
                pass
        x = [(x,sum(map(itemgetter(1),y))) for x,y in groupby(continents, itemgetter(0))]

if __name__ == '__main__':
    ret = Retriever()
    #ret.get_summary_countriesandcases()
    ret.all_countries()
