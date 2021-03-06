from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from app.database import SessionLocal
import time 
import warnings
import datetime
import uuid
from dataclasses import dataclass
warnings.filterwarnings('ignore')

class FIEPage:

    def __init__(self, weapon=None, age=None, comp_type=None, gender=None, team=False):
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service = self.service)
        self.weapon = weapon
        self.weapon_dict={
            'epee':1,
            'foil':2,
            'sabre':3 
            }
        self.age_cat = age
        self.comp_type = comp_type
        self.gender = gender 
        self.team = team
        self.results_xpath = '/html/body/div[4]/div/div/div[1]/div/div[3]/div'
        self.pools_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[1]/div/div[1]/div/span'
        self.prelim_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[1]/div/div[3]/div/span'
        self.tableu_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[1]/div/div[4]/div/span'
    def open_competions(self):
        self.driver.get('https://fie.org/competitions')
        return self
    def previous(self, prev=True):
        index = 1 if prev else 2
        button = self.driver.find_element_by_xpath(f"/html/body/section[1]/div/div/div[1]/form/label[{index}]")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self 

    def select_weapon(self, weapon=None):
        if weapon is None:
            weapon = self.weapon     
        index = self.weapon_dict[weapon.lower()]
        button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][1]/label[{index}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    def select_event_type(self, team=False):
        index = 2 if team else 1
        button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][2]/label[{index}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self 
    def select_gender(self, gender=None):
        if gender is None:
            gender = self.gender
        index = 2 if gender.lower() == 'm' else 1
        button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][3]/label[{index}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self 
    def comp_category(self, comp_type=None):
        if comp_type is None:
            comp_type = self.comp_type
        button = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='select-row Search-options Search-options--advanced Search-options--open']/select[@id='competitionType']")
        select = Select(button)
        self.driver.implicitly_wait(10)
        select.select_by_value(comp_type)
        return self

    def age_group(self, age_cat=None):
        if age_cat is None:
            age_cat = self.age_cat
        button = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='select-row Search-options Search-options--advanced Search-options--open']/select[@id='ageCategory']")
        select = Select(button)
        self.driver.implicitly_wait(10)
        select.select_by_value(age_cat)
        return self
    def search(self):
        search_xpath = "/html/body/section[1]/div/div/div[2]/form/div/div[1]/div/div[1]/div/div[2]/input"
        button = self.driver.find_element_by_xpath(search_xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self

    def dates(self):
        #TODO: Implement Date Picker Method
        pass
    def to_results(self):
        button = self.driver.find_element_by_xpath(self.results_xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    def to_tableu(self):
        button = self.driver.find_element_by_xpath(self.tableu_xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    def to_pools(self):
        button = self.driver.find_element_by_xpath(self.pools_xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    def to_prelims(self):
        button = self.driver.find_element_by_xpath(self.prelim_xpath)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    def next_round_prelim(self, option=False):
        if not option:
            button_path = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[4]/div[2]/div/div[2]/div[5]/div'
        else:
            button_path = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[4]/div[2]/div/div[2]/div[4]/div'
        
        button = self.driver.find_element_by_xpath(button_path)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self
    
    def next_round_de(self):
        button_path = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[5]/div[2]/div/div[2]/div[8]/div'
        button = self.driver.find_element_by_xpath(button_path)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self

    def get_pool_names(self):
        path = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div'
        bouts = self.driver.find_elements_by_xpath(path)
        return [fencer.get_property('title') for fencer in bouts]

    def next_page_tournaments(self):
        path = '/html/body/section[2]/section/div/div/div[1]/div/div/ul/li/a'
        button = self.driver.find_elements_by_xpath(path)
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button[-1]).click(button[-1]).perform()
        return self
    
    def get_prelim_data(self):
        bout_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[4]/div[2]/div/div[2]/div/div'
        bouts = self.driver.find_elements_by_xpath(bout_xpath)
        bout_data = [bout.text.split('\n') for bout in bouts]
        return [tuple(bout) for bout in bout_data if len(bout) == 6]

    def get_pools_data(self):
        pool_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div'
        pool = self.driver.find_elements_by_xpath(pool_xpath)
        pool_data = [element.text.split('\n') for element in pool]
        return pool_data[2:]

    def get_de_data(self):
        de_xpath = '/html/body/div[4]/div/div/div[2]/div[3]/div/div/div[5]/div[2]/div/div[2]/div/div'
        de = self.driver.find_elements_by_xpath(de_xpath)
        de_data = [elem.text.split('\n') for elem in de]
        return [elem for elem in de_data if len(elem) == 6]


    def next_page(self):
        button_path = '/html/body/section[2]/section/div/div/div[1]/div/div/ul/li[7]/a'
        button = self.driver.find_element_by_xpath(button_path)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self

    def prev_page(self):
        button_path = '/html/body/section[2]/section/div/div/div[1]/div/div/ul/li[1]/a'
        button = self.driver.find_element_by_xpath(button_path)
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        return self

    def close_window(self):
        self.driver.close()
        self.driver.implicitly_wait(10)


    # def parse_tableue(self):

    #     size = ['small', 'medium', 'medium', 'big', 'big', 'big']
    #     rnd = ['64', '32', '16', '8', '4', '2']
    #     nums = ["2", "1", "0"]*2
    #     bouts = []
    #     for i, s, r in zip(nums, size, rnd):
    #         win = self.driver.find_elements_by_xpath(f"//div[@class='Tableau-elimination Tableau-elimination--{r} Tableau-elimination--{s} Tableau-elimination--visible-{i}']/div[@class='Tableau-round']/div[@class='Tableau-fencers']/div[@class='Tableau-fencer']")
    #         self.driver.implicitly_wait(10)
    #         lose = self.driver.find_elements_by_xpath(f"//div[@class='Tableau-elimination Tableau-elimination--{r} Tableau-elimination--{s} Tableau-elimination--visible-{i}']/div[@class='Tableau-round']/div[@class='Tableau-fencers']/div[@class='Tableau-fencer Tableau-fencer--defeated']")
    #         self.driver.implicitly_wait(10)
    #         for w_f, l_f in zip(win, lose):
    #             bouts.append((w_f.text, l_f.text))
    #         if int(i) == 0:
    #             for i in range(3): 
    #                 next_button = self.driver.find_elements_by_xpath("//div[@class='Tableau-container']/div[@class='Tableau-directionSquare Tableau-directionSquare--next']/div[@class='Tableau-direction Tableau-direction--next Tableau-direction--square']")
    #                 self.driver.implicitly_wait(10)
    #                 ActionChains(self.driver).move_to_element(next_button[1]).click(next_button[1]).perform()
    #     return bouts


    def get_competitions(self):
        #Well posed if filters are specified enough otherwise will return None's for dropdown tournament      
        competitions = self.driver.find_elements_by_xpath(f"/html/body/section[2]/section/div/div/div[1]/div/table/a")
        metadata = [(comp.text.split('\n'), comp.get_attribute('href')) for comp in competitions]
        return metadata

    # def to_tableue(self):
    #     results = self.driver.find_element_by_xpath("//div[@id='results']/div[@class='Tabs-nav-link js-tabs-nav-link']")
    #     self.driver.implicitly_wait(10)
    #     ActionChains(self.driver).move_to_element(results).click(results).perform()
    #     #navigate to round of 64 tableu
    #     tab_items =self.driver.find_elements_by_xpath("//div[@class='Subtabs-nav-items Subtabs-nav-items--centered']/div[@class='Subtabs-nav-item js-subtabs-nav-item']")
    #     self.driver.implicitly_wait(10)
    #     tab_labels = [tab_item.text for tab_item in tab_items]
    #     if 'Tableau' in tab_labels:
    #         ind = tab_labels.index('Tableau')
    #         button = tab_items[ind]
    #         ActionChains(self.driver).move_to_element(button).click(button).perform()
    #         success = True
    #     else: success = False
    #     return success



    def search(self):
        submit = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='top-row']/div[@class='row']/div[@class='col-xs-12 col-md-8']/div[@class='search-row']/div[@class='check-container']/input")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(submit).click(submit).perform()
        time.sleep(4)

    def open_window(self, link):
        self.driver.execute_script(f'''window.open("{link}", '_blank')''')
        main_window, new_window = self.driver.window_handles
        self.driver.switch_to.window(new_window)
        return new_window

    def scrape(self):
        self.open_competions()
        consecutive_fails = 0
        self.filters()
        time.sleep(4)
        self.search()
        while consecutive_fails < 5:
            hrefs = self.get_links()
            for link in hrefs:
                #open link 
                self.driver.execute_script(f'''window.open("{link}", '_blank')''')
                main_window, new_window = self.driver.window_handles
                self.driver.switch_to.window(new_window)
                meta = self.tournament_metadata()
                success = self.to_tableue()
                if success == True:
                    consecutive_fails = 0
                    bouts = self.parse_tableue()
                    self.populate_db(bouts, *meta)

                else: consecutive_fails += 1

                self.driver.close()
                self.driver.switch_to.window(main_window)
            next_button = self.driver.find_element_by_xpath("//div[@class='table-parent']/div[@class='text-center']/ul[@class='pager']/li[7]/a")
            self.driver.implicitly_wait(10)
            ActionChains(self.driver).move_to_element(next_button).click(next_button).perform()




def parse_metadata(metadata):
    metadata = metadata.split('\n')
    return metadata


def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]


def parse_pool(pool, pool_name, conn):
    pool = pool[2:]
    for elem in pool:
        if not elem.isnumeric():
            break 
        last_elem = elem
    
    pool_size = int(last_elem)
    def chunker(seq, size):
        for pos in range(0, len(seq), size):
            yield seq[pos:pos + size]
    bouts = {}
    for name, elem in zip(pool_name, chunker(pool[pool_size+4:], pool_size + 6)):
        country = elem[1]
        first_name, last_name = parse_name(name)
        fencer_id = check_and_add(first_name, last_name, country,  conn)
        bouts[fencer_id] = elem[3:3+pool_size-1] 
        #bouts[''.join([first_name.upper(), ' ', last_name.upper()])] = elem[3:3+pool_size-1]
    return bouts, pool_size
    
def parse_name(name):
    split_names = name.split(' ')
    print(split_names)
    last_name = []
    first_name = []
    for name in split_names:
        if name.isupper():
            last_name.append(name)
        else:
            first_name.append(name)
    first_name = ' '.join(first_name).upper()
    last_name = ' '.join(last_name)
    return first_name, last_name

def check_and_add(first_name, last_name, country, conn):
        f1 = conn.execute("SELECT f.id FROM fencers f WHERE f.first_name = ? AND f.last_name = ? AND f.country = ?", (first_name.upper(), last_name.upper(), country.upper())).fetchall()
        if len(f1) != 0:
            fencer_id = f1[0]['id']
        else:
            cur =  conn.cursor()
            cur.execute("insert into fencers (first_name, last_name, country) values (?, ?, ?)", (first_name, last_name, country))
            id = conn.execute("select f.id from fencers f where f.first_name = ? and f.last_name = ? and f.country = ?", (first_name.upper(), last_name.upper(), country.upper())).fetchall()
            fencer_id = id[0]['id']
            cur.close()
        return fencer_id

        


def pool_to_db(pool_bouts, tournament_id, conn):
    #When creating fencer objects in pools initially none will have ids so 
    #need to check if they exist in the db and then add id to object
    for i, (fencer_id, fencer_bouts) in enumerate(pool_bouts.items()):
        if i == len(pool_bouts): break
        #Check and add inserts into db if not there
        # and returns fencer object with id
        # f1 = session.query(Fencer).filter_by(first_name=fencer.first_name, last_name=fencer.last_name, country=fencer.country).first()
        for j, b in enumerate(fencer_bouts[i:], start = i+1):
            op_id = list(pool_bouts.keys())[j] 
            # f2 = session.query(Fencer).filter_by(first_name=op.first_name, last_name=op.last_name, country=op.country).first()
            op_bout = pool_bouts[op_id][i]
            fencer_res, fencer_score = b.split('/')
            op_res, op_score = op_bout.split('/')
            if fencer_res == 'V':
                f_win_id = fencer_id
                f_win_score = fencer_score
                f_lose_id = op_id
                f_lose_score = op_score 
            else:
                f_win_id = op_id
                f_win_score = op_score
                f_lose_id = fencer_id 
                f_lose_score = fencer_score
            
            cursor = conn.cursor()
            bout_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO bouts (id, win_score, lose_score, round) VALUES (?, ?, ?, ?)", (bout_id, f_win_score, f_lose_score, 'P'))
            cursor.execute("INSERT INTO winners (fencer_id, bout_id) VALUES (?, ?)", (f_win_id, bout_id))
            cursor.execute("INSERT INTO losers (fencer_id, bout_id) VALUES (?, ?)", (f_lose_id, bout_id))
            cursor.execute("INSERT INTO tournaments_to_bouts (tournament_id, bout_id) VALUES (?, ?)", (tournament_id, bout_id))
            cursor.close()
            #local_bout = Bout(fencer_w_score = f_win_score, fencer_l_score = f_lose_score, round = 'P')
            # session.add(local_bout)
            # local_bout.fencer_win = f_win
            # local_bout.fencer_lose = f_lose
            # tournament.bouts.append(local_bout)
            # tournament.fencers.extend([f_win, f_lose])

            
def round_to_db(bouts, rnd, tournament_id, conn):
    round_bouts = []
    for bout in bouts:
        f1_name, f1_country, f1_score, f2_name, f2_country, f2_score = bout
        f1_first_name, f1_last_name = parse_name(f1_name)
        f2_first_name, f2_last_name = parse_name(f2_name)
        f1_id = check_and_add(f1_first_name, f1_last_name, f1_country, conn)
        f2_id = check_and_add(f2_first_name, f2_last_name, f2_country, conn)


        # f1 = session.query(Fencer).filter_by(first_name=f1_first_name, last_name=f1_last_name, country=f1_country).first() 
        # f2 = session.query(Fencer).filter_by(first_name=f2_first_name, last_name=f2_last_name, country=f2_country).first() 
        if int(f1_score) > int(f2_score): 
            win_fencer_id = f1_id
            win_score = f1_score
            lose_fencer_id = f2_id
            lose_score = f2_score
        else:
            win_fencer_id = f2_id
            win_score = f2_score 
            lose_fencer_id = f1_id
            lose_score = f1_score
        curs = conn.cursor()
        bout_id = str(uuid.uuid4())
        curs.execute("INSERT INTO bouts  (id, win_score, lose_score, round) VALUES (?, ?, ?, ?)", (bout_id, win_score, lose_score, rnd))
        curs.execute("INSERT INTO winners (fencer_id, bout_id) VALUES (?, ?)", (win_fencer_id, bout_id))
        curs.execute("INSERT INTO losers (fencer_id, bout_id) VALUES (?, ?)", (lose_fencer_id, bout_id))
        curs.execute("INSERT INTO tournaments_to_bouts (tournament_id, bout_id) VALUES (?, ?)", (tournament_id, bout_id))
        curs.close()
    return round_bouts


def tournament_to_db(tourn_data, conn):
    country = tourn_data[2][1:3]
    city = tourn_data[1]
    bouts = []
    s_day, s_month, s_year = tourn_data[3].split(' ')[1].split('-')
    e_day, e_month, e_year = tourn_data[4].split(' ')[1].split('-')
    start_date = datetime.date(year=int(s_year), month=int(s_month), day=int(s_day)) 
    end_date = datetime.date(year=int(e_year), month=int(e_month), day=int(e_day))
    curs = conn.cursor()
    curs.execute("INSERT INTO tournaments (country, city, start_date, end_date) VALUES (?, ?, ?, ?)", (country, city, start_date, end_date))
    res = curs.execute("SELECT t.id FROM tournaments t WHERE t.country = ? AND t.city = ? AND t.start_date = ? AND t.end_date = ?", (country, city, start_date, end_date)).fetchall()
    tournament_id = res[0]['id']
    curs.close()
    return tournament_id 

@dataclass(init=False, unsafe_hash=True)
class Fencer:
    id: int = None
    first_name: str
    last_name: str
    country: str

@dataclass(init=False)
class Bout:
    id: int = None
    win_score: int
    lose_score: int
    win_fencer: Fencer
    lose_fencer: Fencer
    rnd: str

@dataclass(init=False)
class Tournament:
    id: int = None
    country: str
    city: str
    start_date: datetime
    end_date: datetime

