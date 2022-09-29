"""

    EpicWarScraper
    
    Класс, реализущий веб скрапер

"""

from bs4 import BeautifulSoup
import requests
import time

class EpicWarScraper:

    _base_url = 'https://www.epicwar.com/maps/'

    def __init__(self, store, sleep=.0):
        self.store = store
        self.session = requests.Session()
        self.sleep = sleep

    def parse_page(self, url, timeout = 5):
        page = self.session.get(url, timeout=timeout)
        return BeautifulSoup(page.text, 'lxml')

    def test(self):
        test_page = self._base_url + '1/'
        parsed_page = self.parse_page(test_page)
        data = self.extract_data(parsed_page)
        data['id'] = 1
        self.store.create_cursor()
        self.store.add_map(data)
        self.store.close_cursor()

    def start(self):

        self.store.create_cursor()

        last_id = self.store.get_last_id() 
        last_map_id = self.get_last_map_id()
        
        if last_id == last_map_id:
            print('All maps are already in db')
            return

        for i in range(last_map_id - last_id):
            mid = i + 1 + last_id
            if not self.store.is_exists(mid):        
                parsed_page = self.parse_page('{}{}/'.format(self._base_url, mid))
                data = self.extract_data(parsed_page)
                if data is not None:
                    data['id'] = mid
                    self.store.add_map(data)
                    print('map', mid, 'was added to db')
                time.sleep(self.sleep)
            else:
                print('map', mid, 'is already in db')
             
        self.store.close_cursor()


    def extract_data(self, tree):

        obj = {}

        cl_listentry = tree.find_all('td', {'class': 'listentry'})
        
        if len(cl_listentry) < 2 or len(cl_listentry) > 3:
            return None

        obj['name'] = cl_listentry[1].a.b.text

        obj['author'] = cl_listentry[1].find_all('b')[1]
        for a in obj['author'].find_all('a'):
            a.decompose()
        obj['author'] = obj['author'].text[:60]

        r_list = repr(cl_listentry[2]).split('\n')

        for el in r_list:
            if el.find('Category') > 0:
                obj['category'] = el[17:-5]
            elif el.find('Tileset') > 0:
                obj['tileset'] = el[16:-5]
            elif el.find('Dimensions') > 0:
                obj['dims'] = el[19:-5]
            elif el.find('Playable Area:') > 0:
                obj['area'] = el[22:-5]
            elif el.find('Recommended Players:') > 0: 
                sl = BeautifulSoup(el, 'lxml')
                for a in sl.find_all('a'):
                    a.decompose()
                if sl.br is not None:
                    sl.br.decompose()
                sl.b.decompose()
                obj['players'] = sl.text[:35]
            elif el.find('Size') > 0:
                obj['size'] = el[13:-8]
            elif el.find('Submitted') > 0:
                obj['sub'] = el[18:-5]
            elif el.find('Rating') > 0:
                obj['good'] = el[el.find('f">')+3: el.find('Go')-1]
                obj['bad'] = el[el.find('3">')+3: el.find('Ba')-1]
            elif el.find('Downloads') > 0:
                obj['downloads'] = el[18:-5]
            
        return obj
    
    
    def get_last_map_id(self):
        parsed_page = self.parse_page(self._base_url+'/')   
        last_map_link = parsed_page.find_all('table')[-2].find_all('tr')[1].a.attrs['href']   
        last_map_id = last_map_link.split('/')
        return int(last_map_id[-2])
        