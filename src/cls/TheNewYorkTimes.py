from cls.DOM import DOM
from cls.Browser import Browser
from dateutil.parser import parse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TheNewYorkTimes:
    def __init__(self, descriptive_mode = 0):
        self.__descriptive_mode = descriptive_mode

        interaction_wait = 1
        typing_wait = 0.2
        goto_wait = 2
        
        self.__b = Browser(
            interaction_wait = interaction_wait,
            typing_wait = typing_wait,
            goto_wait = goto_wait
        )

        self.__b.goto('https://www.nytimes.com/')
    
        self.Say('Clicking Reject Cookies options')
        self.__b.click_button(1, text='Reject')
        
    def Say(self, text):
        if(self.__descriptive_mode):
            print('\t' + text)

    def Search(self, search_phrase):
        # Faster implementation (easier to detect)
        # self.Say('Using GET params to get to the right page')
        # self.__b.goto("https://www.nytimes.com/search?query=" + search_phrase.replace(' ','+'))

        self.Say('Clicking on Search button')
        self.__b.click_element('[data-test-id="search-button"]')

        self.Say('Typing sentence')
        for char in search_phrase:
            self.__b.input_text('[data-testid="search-input"]', char)

        self.Say('Clicking on Go button')
        self.__b.click_element('[data-test-id="search-submit"]')

    def Sort(self, by='newest'):
        options = ['best', 'newest', 'oldest']

        if(by not in options):
            by = 'newest'
        
        self.Say('Clicking sort options')
        self.__b.click_element('[data-testid="SearchForm-sortBy"]')

        self.Say('Choosing ' + by + ' option')
        self.__b.click_element('[value="' + by + '"]')

        self.Say('Choosing somewhere else for the options to disappear')
        self.__b.click_element('[data-testid="SearchForm-status"]')

    def FilterBySections(self, filter_list):
        if(filter_list == ['Any']):
            self.Say('Clicking section options')
            self.__b.click_element('[data-testid="search-multiselect-button"]')

            try:
                self.Say('Clicking Any filter')
                self.__b.click_element('[value^="any"]')
            except: 
                self.Say('Option Any not found')
            
            self.Say('Choosing somewhere else for the options to disappear')
            self.__b.click_element('[data-testid="SearchForm-status"]')

        elif(len(filter_list) > 0):
            self.Say('Clicking section options')
            self.__b.click_element('[data-testid="search-multiselect-button"]')

            elements_list = self.__b.find_elements('[data-testid="multi-select-dropdown-list"]')
            
            if(len(elements_list) > 0):
                e = elements_list[0]
                d = DOM(e)

                options_list = []

                for li in d.get_tag_contents('li'):
                    d2 = DOM(html=li)
                    options_list.append(d2.get_tag_contents('span')[0].split('<')[0])

                filter_list = list(set(options_list) & set(filter_list))

                for filter in filter_list:
                    try:
                        self.Say('Clicking ' + filter + ' filter')
                        self.__b.click_element('[value^="' + filter + '"]')
                    except: 
                        self.Say('Option ' + filter + ' not found')


                self.Say('Choosing somewhere else for the options to disappear')
                self.__b.click_element('[data-testid="SearchForm-status"]')
            else:
                self.Say('No dropdown options')
        else:
            self.Say('Didn\'t choose a section to filter')
       
    def GetNews(self, months, search_phrase):
        self.Say('Starting to read news')
        if(months < 1):
            months = 1        
        months = months - 1

        today = datetime.now().date()
        try:
            limit = today.replace(day=1) - relativedelta(months=months)
        except ValueError:
            limit = datetime(1950,1,1).date()
        
        self.Say('Limit date set to ' + str(limit))
        
        date = today
        
        elements_list = None

        last_list_size = 0

        self.Say('Clicking Show More until the time criteria is met')
        while(date >= limit):
            elements_list = self.__b.find_elements('[data-testid="search-bodega-result"]')

            if(len(elements_list) == last_list_size):                
                self.Say('No more news found')
                break
            
            # for e in elements_list:
            #optimization - avoids reading same news again
            for i in range(last_list_size, len(elements_list)):
                e = elements_list[i]
                d = DOM(e)
                
                dt_str = d.get_tag_contents('span')[0]
                # Just now
                if('h ago' in dt_str):
                    h = dt_str.split('h')[0]
                    date = (datetime.now() - timedelta(hours = int(h))).date()
                elif('m ago' in dt_str):
                    m = dt_str.split('m')[0]
                    date = (datetime.now() - timedelta(minutes = int(m))).date()
                elif('Just now' in dt_str):
                    datetime.now().date()
                else:
                    date = parse(dt_str).date()
            
            self.Say('Clicking Show More')
            self.__b.click_element('[data-testid="search-show-more-button"]')

            last_list_size = len(elements_list)

        self.Say('Reading all news')
        dict_news = []

        for e in elements_list:
            d = DOM(e)
            
            dt_str = d.get_tag_contents('span')[0]
            if('h ago' in dt_str):
                h = dt_str.split('h')[0]
                date = (datetime.now() - timedelta(hours = int(h))).date()
            elif('m ago' in dt_str):
                m = dt_str.split('m')[0]
                date = (datetime.now() - timedelta(minutes = int(m))).date()
            elif('Just now' in dt_str):
                datetime.now().date()
            else:
                date = parse(dt_str).date()
            
            if(date < limit):
                break

            title = d.get_tag_contents('h4')[0]
            paragraphs = d.get_tag_contents('p')
            category = paragraphs[0]
            description = paragraphs[1] if len(paragraphs) >= 2 else ''
            author = paragraphs[2][3:] if len(paragraphs) >= 3 else 'Unknown'

            img = d.get_tags('img')
            if(len(img) > 0):
                img_path = str(img[0]).split('src="')[1].split('"')[0]
                img_name = img_path.split('/')[-1].split('?')[0]
            else:
                img_name = ''
                img_path = ''

            #visual check
            # self.Say('date:\t\t' + str(date))
            # self.Say('title:\t\t' + title)
            # self.Say('author:\t\t' + author)
            # self.Say('count:\t\t' + str(title.lower().count(search_phrase.lower())))
            # self.Say('$:\t\t' + str('$' in title))
            # self.Say('USD:\t\t' + str('USD' in title))
            # self.Say('dollar:\t\t' + str('dollar' in title))
            # self.Say('money:\t\t' + str(('$' in title) or ('USD' in title) or ('dollar' in title)))
            # self.Say('img_name:\t' + img_name)
            # self.Say('img_path:\t' + img_path + '\n')
        
            dict_news.append({
                'title': title,
                'date': date,
                'description': description,
                'img_name': img_name,
                'author': author,
                'count': title.lower().count(search_phrase.lower()),
                'money': ('$' in title) or ('USD' in title) or ('dollar' in title),
                'img_path': img_path
            })
        
        self.Say('Finished reading news')
        
        return dict_news