# Imports

import amazon_tracker_configs as conf
import time
from selenium.webdriver.common.keys import Keys

# Classes

class AmazonAPI:
    
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        self.currency = currency
        self.price_filters = f"&rh=p36%3A{filters['min']}00-{filters['max']}00"
        
        
        options = conf.get_chromdriver_options()
        conf.set_ignore_certificate_error(options)
        conf.set_incognito_mode(options)
        
        self.driver = conf.get_chrome_driver(options)
        
        
    def get_product_links(self):
        self.driver.get(self.base_url)
        time.sleep(2)
        
        search_box = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        
        self.driver.get(f'{self.driver.current_url}{self.price_filters}')
        time.sleep(2)
        
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        
        links = []
        try :
            
            results = result_list[0].find_elements_by_xpath('//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            links = [link.get_attribute('href') for link in results]
            return links
        
        except Exception as exp :
            
            print("Sorry no  search results")
            print(exp)
            return links
        
       
        
    def get_products_info(self,links):
        asins = self.get_asins(links)
        
        products = []
        
        for asin in asins:
            product = self.get_single_product_info(asin)
            
            
    def get_single_product_info(self, asin):
        
        print(f"Getting Info for Product ID: {asin}")
        
        product_shortened_url = self.shorten_url(asin)
        
        self.driver.get(f'{product_shortened_url}?language=en_GB')
        time.sleep(2)
        
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        
        
    
    def get_title(self):
        
        try :
            
            return self.driver.find_element_by_id('productTitle').text
        
        except Exception as exp:
            
            print(exp)
            print(f'Error cannot get title for this product')
            return None
        
    def get_seller(self):
        
        try :
            
            return self.driver.find_element_by_id('bylineinfo').text
        
        except Exception as exp:
            
            print(exp)
            print(f"error cannot get seller for this item")
            return None
        
        
    def get_price(self):
    
        pass
    
    
    def shorten_url(self, asin):
        
        return self.base_url + 'dp/' + asin
        
        
        
        
    def get_asins(self, links):
        return [self.get_asin(link) for link in links]
        
    
    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref/')]
        
        
    
    
    def run(self):    
        print("Starting Tracker....")
        print(f"Searching Amazon for {self.search_term}")
        time.sleep(1)
        
        product_links = self.get_product_links()
        if not product_links :
            print("No links Found")
            return
        
        print(f'found : {len(product_links)}')
        print(f'Getting Products Information...')
        
        products_info = self.get_products_info(product_links )
        
        self.driver.quit()

class ReportGenerator:
    
    def __init__(self):
        pass 





# Static Functions


if __name__ == '__main__':
    print("Initialising......")
    amazon = AmazonAPI(conf.ITEM_NAME, conf.FILTERS, conf.BASE_URL, conf.CURRENCY)
    
    amazon.run()