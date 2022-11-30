import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import csv
import queue
import threading
import time

global urls_queue
urls_queue = []
lock = threading.Lock()

class Scraper (threading.Thread):

    

    def __init__(self) -> None:
        self.site_url = "https://exrx.net"
        self.base_url = "https://exrx.net/Lists/Directory"
        self.f = open("workouts.csv", "w")
        self.link_exercise_mapping = {}
        self.thread_exit_flag = 0

    def  getData(self):
        (exercises_urls, self.link_exercise_mapping) = self.getPages()
        for url in exercises_urls:
            urls_queue.append(url)

       
            name = "Thread" + str(0)
            t = threading.Thread(name=name,target=self.reader )
            t.start()
            name = "Thread" + str(1)
            t2 = threading.Thread(name=name,target=self.reader )
            t2.start()
            name = "Thread" + str(2)
            t3 = threading.Thread(name=name,target=self.reader )
            t3.start()
            name = "Thread" + str(3)
            t4 = threading.Thread(name=name,target=self.reader )
            t4.start()
            name = "Thread" + str(4)
            t5 = threading.Thread(name=name,target=self.reader )
            t5.start()
            t.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()

        self.f.close()
        

        
    def reader(self):
        print(f"----- Starting thread: {threading.currentThread().getName()}")
        while (len(urls_queue) != 0):
            print(f"---- item left in queue {len(urls_queue)}")
            try:
                lock.acquire()
                data =  urls_queue.pop()
                #process data
                self.createDataFromSingleWorkoutPage(self.f,data,link_exercise_mapping=self.link_exercise_mapping)
            except:
                #once no mor data is present
                print('No more data')
            lock.release()

    def getPages(self):
        html_text = requests.get(self.base_url).text
        base_page = BeautifulSoup(html_text, 'html.parser')

        muscle_group_pages = base_page.find_all('a')

        musclegroup_list_base_url = "https://exrx.net/Lists/"
        exlist = []
        for link in muscle_group_pages:
            link_string = link.get("href")
            if 'ExList' in link_string:
                if not link_string.startswith("https"):
                    link_string = musclegroup_list_base_url + link_string
                    exlist.append(link_string)
                    #print(f"{link_string}")

        # now get link to each individual exercise per muscle group
        print("------------- Getting Exercise Links ---------------")
        exercises_urls = set()
        link_exercise_mapping = {}
        for link in exlist:
            print(f"------------- parsing: {link}")
            html = requests.get(link).text
            dir_page = BeautifulSoup(html, 'html.parser')

            # find the ul elem 
            
            containers_list = dir_page.find('article').find_all('div', attrs={
                'class' : 'col-sm-6'})

            for container_div in containers_list:
                lists_elems = container_div.find_all('ul', recursive=False)
                for list in lists_elems:
                    li_elem =list.findChildren('li')
                    for li in li_elem:
                        # get the primary text for the first tag
                        res = [element for element in li if isinstance(element, NavigableString)]
                        #if  '<' not in first_tag and len(first_tag) > 0:
                        res = self.cleanNavigateableStringRes(res)
                        equipment_name = ""
                        if len(res) > 0:
                            equipment_name = res[0]
                            #print(f"tag: {res[0]} -----")

                            # now get the workout links under this tag
                            workout_links = li.find_all('a')

                            for link in workout_links:
                                url_string = link.get("href")
                                if url_string is not None and ('WeightExercises' in url_string or 'Stretches' in url_string or 'Plyometrics' in url_string):
                                    if (url_string.startswith("../../")):
                                        url_string = url_string[5:]
                                        url_string = self.site_url + url_string

                                exercises_urls.add(url_string)
                                link_exercise_mapping[url_string] = equipment_name
            
        return (exercises_urls, link_exercise_mapping)
        #end    
                  

                
           
            
    def createDataFromWorkoutsPages(self, exercises_urls, link_exercise_mapping):
        f = open("workouts.csv", "w")
        
        for url in exercises_urls:
            html = requests.get(url).text
            details_page = BeautifulSoup(html, 'html.parser')

            # get the w_workoutName
            name = details_page.find('h1', attrs={
                'class' : 'page-title'
            })
            # get the w_mainmusclegroup
            header_dir_elem = details_page.find('div', attrs= {
                'class': "row Breadcrumb-Container Add-Margin-Top"
            })

            header_links = header_dir_elem.find_all('a')
            main_muscle_group = ""
            for link in header_links:
                link_string = link.get("href")
                if 'ExList' in link_string:
                    main_muscle_group = link.text

            # get the w_minorMuscleGroup
            main_shell_elem = details_page.find('div', attrs= { 'id':'mainShell'})
            article_elem = main_shell_elem.find('article')
            minor_muscle_link = article_elem.find('a', attrs= {
                'href' : re.compile(r"Muscles")
            })

            # get the w_equiment
            equipment = link_exercise_mapping[url]

            # get w_description
            p_list = article_elem.find('div', attrs={ 'class':'col-sm-6'}).find_all('p', recursive=False)

            description = ""
            for p in p_list:
                res = [element for element in p if isinstance(element, NavigableString)]
                if len(res) > 0:
                    description = description + res[0].replace('\n', '').replace('\b','').strip() 
                   

            # get w_images
            vid_elem = article_elem.find('video', attrs={'id':'videoid'})
            writer = csv.writer(f, delimiter='|')
            data = [name.text, main_muscle_group, minor_muscle_link.text, equipment, description, "Basic", "https://www.rocketdogrescue.org/wp-content/uploads/2016/08/dog-working-out.jpg", False]
            writer.writerow(data)
            f.flush()
        
        f.close()

    def createDataFromSingleWorkoutPage(self, f, url,link_exercise_mapping):
        html = requests.get(url).text
        details_page = BeautifulSoup(html, 'html.parser')

        # get the w_workoutName
        name = details_page.find('h1', attrs={
            'class' : 'page-title'
        })
        # get the w_mainmusclegroup
        header_dir_elem = details_page.find('div', attrs= {
            'class': "row Breadcrumb-Container Add-Margin-Top"
        })

        header_links = header_dir_elem.find_all('a')
        main_muscle_group = ""
        for link in header_links:
            link_string = link.get("href")
            if 'ExList' in link_string:
                main_muscle_group = link.text

        # get the w_minorMuscleGroup
        main_shell_elem = details_page.find('div', attrs= { 'id':'mainShell'})
        article_elem = main_shell_elem.find('article')
        minor_muscle_link = article_elem.find('a', attrs= {
            'href' : re.compile(r"Muscles")
        })

        # get the w_equiment
        equipment = link_exercise_mapping[url]

        # get w_description
        p_list = article_elem.find('div', attrs={ 'class':'col-sm-6'}).find_all('p', recursive=False)

        description = ""
        for p in p_list:
            res = [element for element in p if isinstance(element, NavigableString)]
            if len(res) > 0:
                description = description + res[0].replace('\n', '').replace('\b','').strip() 
                

        # get w_images
        vid_elem = article_elem.find('video', attrs={'id':'videoid'})
        writer = csv.writer(f, delimiter='|')
        data = [name.text, main_muscle_group, minor_muscle_link.text, equipment, description, "Basic", "https://www.rocketdogrescue.org/wp-content/uploads/2016/08/dog-working-out.jpg", False]
        writer.writerow(data)
        f.flush()
    
       
                     
    def cleanNavigateableStringRes(self, results):
        """
            Checking an html tag for navigatble strings results in an array of inner text.
            This method will clean any whitespaces, newlines, or tabs that are captured in the results array - 
            leaving only valid text
        """
        new_results = []
        for item in results:
            new_string = item.replace('\n', '')
            new_string = new_string.replace('\b', '')
            new_string = new_string.strip()

            if any(c.isalpha() for c in new_string):
                new_results.append(new_string)  
            
        return new_results