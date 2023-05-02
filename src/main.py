import traceback
from cls.Env import Env
from cls.Output import Output
from cls.TheNewYorkTimes import TheNewYorkTimes

def main():
    try:
        env = Env()
        output_folder, descriptive_mode = env.get_bot_config()
        searches = env.get_searches()

        ny = TheNewYorkTimes(descriptive_mode = descriptive_mode)
        
        for search in searches:
            search_phrase = search['SEARCH_PHRASE']
            months = search['MONTHS']
            sections = search['SECTIONS']

            print(' -> New Search:')
            print('Search Phrase:\t', search_phrase)
            print('Months:\t\t', months)
            print('Sections:\t', sections)

            ny.Search(search_phrase = search_phrase)
            ny.Sort()
            ny.FilterBySections(filter_list = sections)
            dict_news = ny.GetNews(months = months, search_phrase = search_phrase)
            ny.FilterBySections(filter_list = ['Any'])

            print(str(len(dict_news)) + ' news read')
            print('Saving news file')
            output = Output(out_folder = output_folder)
            output.save_news(dict_news, search_phrase, sections)
            
            print('Saving images')
            output.save_imgs(dict_news)

            print('Files saved\n')

    except Exception as e:
        print('main():', str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()