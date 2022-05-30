import re
import time
import logging

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class Course:
    def __init__(self):
        self._link = None
        self._title = None
        self._category = None
        self._image_url = None
        self._difficulty = None
        self._description = None
        self._estimated_time = None

    def to_dict(self):
        return {
            'link': self.link,
            'title': self.title,
            'category': self.category,
            'image_url': self.image_url,
            'difficulty': self.difficulty,
            'description': self.description,
            'estimated_time': self.estimated_time
        }

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, dirty_url):
        pattern = r'url\(\"([^\"\;]+)'
        match = re.search(pattern, dirty_url)
        if match is not None:
            self._image_url = match.group(1)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, input_text):
        match = re.search(r'(Facile|Moyenne|Difficile)', input_text)
        if match is not None:
            self._difficulty = match.group(1)

    @property
    def estimated_time(self):
        return self._estimated_time

    @estimated_time.setter
    def estimated_time(self, input_text):
        match = re.search(r'(.*heures?)$', input_text)
        if match is not None:
            self._estimated_time = match.group(1)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, dirty_category):
        if dirty_category.endswith(' - COURS'):
            self._category = dirty_category.split(' - ')[0]


def get_all_courses(courses):
    page_courses = []
    for course in courses:
        new_course = Course()
        new_course.link = course.find_element(By.TAG_NAME, 'a').get_attribute('href')
        new_course.title = course.find_element(By.TAG_NAME, 'h6').text
        new_course.description = course.find_element(By.TAG_NAME, 'p').text
        new_course.image_url = course.find_element(By.TAG_NAME, 'figure').get_attribute('style')
        for element in course.find_elements(By.TAG_NAME, 'span'):
            new_course.difficulty = element.text
            new_course.estimated_time = element.text
            new_course.category = element.text
        page_courses.append(new_course.to_dict())
    return page_courses

def configure_browser():
    # Virtual browser configuration
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    return webdriver.Firefox(options=opts)

def extract_pagination(browser):
    css_selector = 'ul[class^=main-header-2-main-header] > li > button'
    elements = browser.find_elements(By.CSS_SELECTOR, css_selector)
    indexes = list(map(lambda x: x.text, elements))
    return [int(index) for index in indexes if index]

def extract(page_number):
    url = f'https://openclassrooms.com/fr/search?type=course&page={page_number}'
    browser = configure_browser()
    browser.get(url)

    # Wait for the javascript to generate the DOM we are interested in
    css_selector = 'ul[class^=main-header-2-main-header] > .MuiPaper-root'
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        return [], []

    courses = browser.find_elements(By.CSS_SELECTOR, css_selector)
    pagination = extract_pagination(browser)
    return get_all_courses(courses), pagination


if __name__ == '__main__':
    pass
