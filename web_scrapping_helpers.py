from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from app.models import Tournament, Bout, Fencer
from app.database import SessionLocal
import time 
import warnings
import datetime
warnings.filterwarnings('ignore')

class WebScrapper:

    def __init__(self, weapon, age, comp_type, gender, team=False):
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service = self.service)
        self.weapon = weapon
        self.age_cat = age
        self.comp_type = comp_type
        self.gender = gender 
        self.team = team
        
    def open_competions(self):
        self.driver.get('https://fie.org/competitions')

    def filters(self):
        #event: 1 == epee, 2 == foil, 3 == sabre
        weapon_button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][1]/label[{self.weapon}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(weapon_button).click(weapon_button).perform()

        team_button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][2]/label[{2 if self.team == True else 1}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(team_button).click(team_button).perform()

        #1==women 2 == men
        gender_button = self.driver.find_element_by_xpath(f"//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='checkbox-row Search-options Search-options--open']/div[@class='indicators'][3]/label[{self.gender}]/i")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(gender_button).click(gender_button).perform()

        #JO == Olympics, CHM == world championships, GP == Grand Prix, A == World Cup, SA == Sattelite, CHZ == Zonal Championships, OF == Official, NF == Non Official
        type_button = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='select-row Search-options Search-options--advanced Search-options--open']/select[@id='competitionType']")
        select = Select(type_button)
        select.select_by_value(self.comp_type)

        #Cadet === c, Junior == j, Senior== s, Vets == v
        age_button = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='sub-row']/div[@class='select-row Search-options Search-options--advanced Search-options--open']/select[@id='ageCategory']")
        select = Select(age_button)
        self.driver.implicitly_wait(10)
        select.select_by_value(self.age_cat)



    def parse_tableue(self):

        size = ['small', 'medium', 'medium', 'big', 'big', 'big']
        rnd = ['64', '32', '16', '8', '4', '2']
        nums = ["2", "1", "0"]*2
        bouts = []
        for i, s, r in zip(nums, size, rnd):
            win = self.driver.find_elements_by_xpath(f"//div[@class='Tableau-elimination Tableau-elimination--{r} Tableau-elimination--{s} Tableau-elimination--visible-{i}']/div[@class='Tableau-round']/div[@class='Tableau-fencers']/div[@class='Tableau-fencer']")
            self.driver.implicitly_wait(10)
            lose = self.driver.find_elements_by_xpath(f"//div[@class='Tableau-elimination Tableau-elimination--{r} Tableau-elimination--{s} Tableau-elimination--visible-{i}']/div[@class='Tableau-round']/div[@class='Tableau-fencers']/div[@class='Tableau-fencer Tableau-fencer--defeated']")
            self.driver.implicitly_wait(10)
            for w_f, l_f in zip(win, lose):
                bouts.append((w_f.text, l_f.text))
            if int(i) == 0:
                for i in range(3): 
                    next_button = self.driver.find_elements_by_xpath("//div[@class='Tableau-container']/div[@class='Tableau-directionSquare Tableau-directionSquare--next']/div[@class='Tableau-direction Tableau-direction--next Tableau-direction--square']")
                    self.driver.implicitly_wait(10)
                    ActionChains(self.driver).move_to_element(next_button[1]).click(next_button[1]).perform()
        return bouts


    def get_links(self):
        #fetches the href of every row in the competitions table
        links_1 = self.driver.find_elements_by_xpath("//section[@class='athletes-rankings-table results-competitions-table']/section[@class='statistics-table']/div[@class='container small']/div[@class='row']/div[@class='col-xs-12 js-competitions-grid']/div[@class='table-parent']/table[@class='table']/a[@class='Table-row Table-row--hover CompetitionsTable-row CompetitionsTable-row--borderBottom']")
        self.driver.implicitly_wait(10)
        results_2 = self.driver.find_elements_by_xpath("//div[@class='row']/div[@class='col-xs-12 js-competitions-grid']/div[@class='table-parent']/table[@class='table']/a[@class='Table-row Table-row--hover CompetitionsTable-row CompetitionsTable-row--borderBottom CompetitionsTable-row--even']/td[8]")
        self.driver.implicitly_wait(10)
        links_2 = self.driver.find_elements_by_xpath("//section[@class='athletes-rankings-table results-competitions-table']/section[@class='statistics-table']/div[@class='container small']/div[@class='row']/div[@class='col-xs-12 js-competitions-grid']/div[@class='table-parent']/table[@class='table']/a[@class='Table-row Table-row--hover CompetitionsTable-row CompetitionsTable-row--borderBottom CompetitionsTable-row--even']")
        self.driver.implicitly_wait(10)
        results_1 = self.driver.find_elements_by_xpath("//div[@class='row']/div[@class='col-xs-12 js-competitions-grid']/div[@class='table-parent']/table[@class='table']/a[@class='Table-row Table-row--hover CompetitionsTable-row CompetitionsTable-row--borderBottom']/td[8]")
        self.driver.implicitly_wait(10)
        results_1.extend(results_2)
        results = [result.text for result in results_1]
        links_1.extend(links_2)
        hrefs = [link.get_attribute('href') for link, res in zip(links_1, results) if res == 'Results']
        return hrefs

    def tournament_metadata(self):
        month_to_num = {
            'Jan':1, 
            'Feb':2,
            'Mar':3,
            'Apr':4,
            'May':5,
            'Jun':6,
            'Jul':7,
            'Aug':8,
            'Sep':9,
            'Oct':10,
            'Nov':11,
            'Dec':12,
            }
        date = self.driver.find_element_by_xpath("//span[@class='CompetitionHero-date']")
        self.driver.implicitly_wait(10)
        city = self.driver.find_element_by_xpath("//div[@class='Overview-section']/div[@class='Overview-group'][1]/div[@class='Table-country Overview-country Overview-label--dark']/span[@class='Overview-country-name']")
        self.driver.implicitly_wait(10)
        country = self.driver.find_element_by_xpath("//div[@class='Overview-section']/div[@class='Overview-group'][2]/div[@class='Table-country Overview-country Overview-label--dark']/span[@class='Overview-country-name']")
        self.driver.implicitly_wait(10)
        country = country.text.split(' ')[0]
        city = city.text
        date = date.text
        date = date.split(' ')
        date = datetime.date(int(date[-1]), month_to_num[date[1]], int(date[0]))

        return date, country, city

    def to_tableue(self):
        results = self.driver.find_element_by_xpath("//div[@id='results']/div[@class='Tabs-nav-link js-tabs-nav-link']")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(results).click(results).perform()
        #navigate to round of 64 tableu
        tab_items =self.driver.find_elements_by_xpath("//div[@class='Subtabs-nav-items Subtabs-nav-items--centered']/div[@class='Subtabs-nav-item js-subtabs-nav-item']")
        self.driver.implicitly_wait(10)
        tab_labels = [tab_item.text for tab_item in tab_items]
        if 'Tableau' in tab_labels:
            ind = tab_labels.index('Tableau')
            button = tab_items[ind]
            ActionChains(self.driver).move_to_element(button).click(button).perform()
            success = True
        else: success = False
        return success

    def populate_db(self, bouts, date, country, city):
        tournament = Tournament(country=country, city=city, date=date)
        fencers = []
        with SessionLocal as session, session.begin():
            for bout in bouts[:32]:
                
                rnd = 64
                fencer_1, fencer_2 = bout
                fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
                name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
                first_names_1 = []
                last_names_1 = []
                first_names_2 = []
                last_names_2 = []
                for name in name_1:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_1 = ' '.join(first_names_1)
                last_name_1 = ' '.join(last_names_1)

                for name in name_2:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_2 = ' '.join(first_names_2)
                last_name_2 = ' '.join(last_names_2)
                print(first_name_1, last_name_1, first_name_2, last_name_2)
                country_1, country_2 = fencer_1[1], fencer_2[1]
                score_1, score_2 = fencer_1[2], fencer_2[2]
                f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name=last_name_1).first()
                if not f1:
                    f1 = Fencer(first_name = first_name_1, last_name = last_name_1, country = country_1)
                    session.add(f1)
                f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name=last_name_2).first()
                if not f2:
                    f2 = Fencer(first_name = first_name_2, last_name = last_name_2, country = country_2)
                    session.add(f2)
                fencers.extend([f1, f2])
                local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
                session.add(local_bout)
                local_bout.fencers.extend([f1, f2])
                tournament.bouts.append(local_bout)        

            for bout in bouts[32:48]:
                
                rnd = 32
                fencer_1, fencer_2 = bout
                fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
                name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
                first_names_1 = []
                last_names_1 = []
                first_names_2 = []
                last_names_2 = []
                for name in name_1:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_1 = ' '.join(first_names_1)
                last_name_1 = ' '.join(last_names_1)

                for name in name_2:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)

                first_name_2 = ' '.join(first_names_2)
                last_name_2 = ' '.join(last_names_2)
                country_1, country_2 = fencer_1[1], fencer_2[1]
                score_1, score_2 = fencer_1[2], fencer_2[2]
                f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name = last_name_1).first()         
                f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name = last_name_2).first()           
                fencers.extend([f1, f2])
                local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
                session.add(local_bout)
                local_bout.fencers.extend([f1, f2])
                tournament.bouts.append(local_bout)

            for bout in bouts[48:56]:
                
                rnd=16
                fencer_1, fencer_2 = bout
                fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
                name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
                first_names_1 = []
                last_names_1 = []
                first_names_2 = []
                last_names_2 = []
                for name in name_1:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_1 = ' '.join(first_names_1)
                last_name_1 = ' '.join(last_names_1)

                for name in name_2:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_2 = ' '.join(first_names_2)
                last_name_2 = ' '.join(last_names_2)

                country_1, country_2 = fencer_1[1], fencer_2[1]
                score_1, score_2 = fencer_1[2], fencer_2[2]
                f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name = last_name_1).first()         
                f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name = last_name_2).first()           
                fencers.extend([f1, f2])
                local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
                session.add(local_bout)
                local_bout.fencers.extend([f1, f2])
                tournament.bouts.append(local_bout)

            for bout in bouts[56:60]:
                rnd = 8
                fencer_1, fencer_2 = bout
                fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
                name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
                first_names_1 = []
                last_names_1 = []
                first_names_2 = []
                last_names_2 = []
                for name in name_1:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_1 = ' '.join(first_names_1)
                last_name_1 = ' '.join(last_names_1)

                for name in name_2:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_2 = ' '.join(first_names_2)
                last_name_2 = ' '.join(last_names_2)
                country_1, country_2 = fencer_1[1], fencer_2[1]
                score_1, score_2 = fencer_1[2], fencer_2[2]
                f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name = last_name_1).first()         
                f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name = last_name_2).first()           
                fencers.extend([f1, f2])
                session.add(f1)
                session.add(f2)
                local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
                session.add(local_bout)
                local_bout.fencers.extend([f1, f2])
                tournament.bouts.append(local_bout)

            for bout in bouts[60:62]:
                
                rnd = 4
                fencer_1, fencer_2 = bout
                fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
                name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
                first_names_1 = []
                last_names_1 = []
                first_names_2 = []
                last_names_2 = []
                for name in name_1:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_1 = ' '.join(first_names_1)
                last_name_1 = ' '.join(last_names_1)

                for name in name_2:
                    if name.isupper():
                        name = ''.join([name[0], name[1:].lower()])
                        last_names_1.append(name)
                    else: first_names_1.append(name)
                first_name_2 = ' '.join(first_names_2)
                last_name_2 = ' '.join(last_names_2)
                country_1, country_2 = fencer_1[1], fencer_2[1]
                score_1, score_2 = fencer_1[2], fencer_2[2]
                f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name = last_name_1).first()         
                f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name = last_name_2).first()           
                fencers.extend([f1, f2])
                session.add(f1)
                session.add(f2)
                local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
                session.add(local_bout)
                local_bout.fencers.extend([f1, f2])
                tournament.bouts.append(local_bout) 

            rnd = 2
            fencer_1, fencer_2 = bouts[-1]
            fencer_1, fencer_2 = fencer_1.split('\n'), fencer_2.split('\n')
            name_1, name_2 = fencer_1[0].split(' '), fencer_2[0].split(' ')
            first_names_1 = []
            last_names_1 = []
            first_names_2 = []
            last_names_2 = []
            for name in name_1:
                if name.isupper():
                    name = ''.join([name[0], name[1:].lower()])
                    last_names_1.append(name)
                else: first_names_1.append(name)
            first_name_1 = ' '.join(first_names_1)
            last_name_1 = ' '.join(last_names_1)

            for name in name_2:
                if name.isupper():
                    name = ''.join([name[0], name[1:].lower()])
                    last_names_1.append(name)
                else: first_names_1.append(name)
            first_name_2 = ' '.join(first_names_2)
            last_name_2 = ' '.join(last_names_2)
            country_1, country_2 = fencer_1[1], fencer_2[1]
            score_1, score_2 = fencer_1[2], fencer_2[2]
            f1 = session.query(Fencer).filter_by(first_name = first_name_1).filter_by(last_name = last_name_1).first()         
            f2 = session.query(Fencer).filter_by(first_name = first_name_2).filter_by(last_name = last_name_2).first()           
            fencers.extend([f1, f2])
            session.add(f1)
            session.add(f2)
            local_bout = Bout(fencer_1_score= score_1, fencer_2_score=score_2, rnd = rnd)
            session.add(local_bout)
            local_bout.fencers.extend([f1, f2])
            tournament.bouts.append(local_bout) 
            tournament.fencers.extend(fencers)


    def search(self):
        submit = self.driver.find_element_by_xpath("//div[@class='row']/div[@class='col-xs-12'][2]/form[@class='js-comp-form-search']/div[@class='filter-wrapper']/div[@class='top-row']/div[@class='row']/div[@class='col-xs-12 col-md-8']/div[@class='search-row']/div[@class='check-container']/input")
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(submit).click(submit).perform()
        time.sleep(4)

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