import os
import argparse
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class Slogger:

    @staticmethod
    def url_encode(urls):
        new_urls = []
        for url in urls:
            url_split = url.split("/")
            new_urls.append(url_split[0]+"//"+url_split[2]+"/"+urllib.parse.quote("/".join(url_split[3:])))

        return new_urls

    def __init__(self, url_file):

        #read the file and setup the urls
        self.urls = [url.strip() for url in open(url_file).readlines()]
        self.new_urls = self.url_encode(self.urls)
        '''
        for url in self.new_urls:
            print (url)
        #print(self.new_urls)
        '''

    @staticmethod
    def fetch_size(url):

        site = urllib.request.urlopen(url)
        meta = site.info()

        #print("Thread : {}".format(threading.current_thread().name))
        print("{} : {} => {:.2f}MB ({} bytes) \n".format(threading.current_thread().name, url, int(meta['Content-Length'])/(1024*1024), int(meta['Content-Length'])))
        return int(meta['Content-Length'])

    @staticmethod
    def print_relative_size(size_bytes):

        if int(size_bytes/(1024*1024*1024)) >0:
            print("Total Size : {:.2f} GB ({} bytes)".format(size_bytes/(1024*1024*1024), size_bytes))
            return "{:.2f} GB".format(size_bytes/(1024*1024*1024))

        elif int(size_bytes/(1024*1024)) >0:
            print("Total Size : {:.2f} MB ({} bytes)".format(size_bytes/(1024*1024), size_bytes))
            return "{:.2f} MB".format(size_bytes/(1024*1024))

        elif int(size_bytes/(1024)) >0:
            print("Total Size : {:.2f} KB ({} bytes)".format(size_bytes/(1024), size_bytes))
            return "{:.2f} KB".format(size_bytes/(1024))

        else:
            print("Total Size : {} B ({} bytes)".format(size_bytes))
            return "{} B".format(size_bytes)


    def cal_total_size(self):

        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(self.fetch_size, url) for url in self.new_urls]

            cumulative =0
            for future in as_completed(futures):
                cumulative += future.result()
            #print("Cumulative Size : {}\n".format(cumulative))
            return cumulative


    def fetch_urls(self, url):
        ''' Save the urls to the disk'''

        req = urllib.request.urlopen(url)
        filename = os.path.basename(url)

        print("Thread : {}".format(threading.current_thread().name))
        print("STARTED : {filename}\n".format(filename=filename))

        with open(os.path.join(self.output_dir, filename), 'wb') as file_handler:

            while True:
                chunk = req.read(1024)
                if not chunk:
                    break
                #print(sys.getsizeof(chunk))
                file_handler.write(chunk)
        return 'DONE : {filename}'.format(filename=filename)


    def download_urls(self):

        # Create temp and output paths based on where the executable is located
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = os.path.join(self.base_dir, "output")

        if os.path.exists(self.output_dir)==False:
            os.mkdir(self.output_dir)
            
        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(self.fetch_urls, url) for url in self.new_urls]
            for future in as_completed(futures):
                print(future.result())

    def go(self):

        #Check for the entire size of downloads and check with user
        total_size_bytes = self.cal_total_size()
        total_size = self.print_relative_size(total_size_bytes)

        option =''
        while option not in ('Y', 'N'):
            option = input(total_size+" of Data required. Do you want to continue ? [Y/N]: ")

            if option not in ('Y', 'N'):
                print("Incorrect option! Choose 'Y' or 'N'")

        #Don't proceed to donload if user opts out
        if option == 'N':
            print('Got it! Exiting ...')
            exit()

        print("Proceed to Download ....")
        #Proceed ahead to download the urls

        self.download_urls()

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--urls", required=True, help=" File containing urls list")
    args = vars(ap.parse_args())

    slogg = Slogger(args["urls"])
    slogg.go()
