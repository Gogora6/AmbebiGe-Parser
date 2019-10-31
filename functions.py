import requests
import os
import csv
import threading


class SaitebiGe:
    def __init__(self, surname, lastname):
        self.url = f"https://www.ambebi.ge/api/search/?page=1&q={surname}+{lastname}"
        self.surname = surname
        self.lastname = lastname

    def get_url(self):
        r = requests.get(self.url)
        data = r.json()
        num_pages = data['pagination']['num_pages']
        print(num_pages)
        return num_pages

    def get_ids(self):
        ids = []
        num_page = self.get_url()
        for page in range(1, num_page + 1):
            url = f"https://www.ambebi.ge/api/search/?page={page}&q={self.surname}+{self.lastname}"
            r = requests.get(url)
            data = r.json()
            results = data['results']
            for result in results:
                ids.append(result['id'])
        return ids

    def get_info(self, id):
        info = requests.get(f"https://www.ambebi.ge/api/article/{id}/")
        data = info.json()
        try:
            title = data['meta_title']
            text = data['fulltext'].replace("&shy", "").replace(";", "").replace('<p>', "").replace("</p>",
                                                                                                    "").replace(
                "<strong>", "").replace("</strong>", "").replace("<ul>", "").replace("</ul>", "").replace("<li>",
                                                                                                          "").replace(
                "</li>", "")
            publish_date = data['publish_up']
        except:
            title = None
            publish_date = None
            text = None

        self.write_csv(id, title, text, publish_date)

    def create_dir(self):
        try:
            os.mkdir(f'{self.surname}_{self.lastname}')
        except OSError:
            pass

    def write_csv(self, id, title, text, publish_date):
        with open(f'{self.surname}_{self.lastname}/{id}', mode='a', encoding='utf-8-sig') as statement:
            biz_write = csv.writer(statement, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            biz_write.writerow([title, text, publish_date])

    def parse_site(self):
        self.create_dir()
        ids = self.get_ids()
        for id in ids:
            x = threading.Thread(target=self.get_info, args=(id,))
            x.start()
            x.join()
