import argparse
import requests
import warnings
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfReader, PdfMerger


# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Silence the warnings
warnings.filterwarnings("ignore")

#counter for infinite reccursion
n=1

#function to check if a pdf is empty or not
def is_pdf_empty(file_path):
    file_size = os.path.getsize(file_path)
    return file_size == 0

#function to create a pie chart using matplotlib and saving or appending it to the passed pdf
def pie_chart(file_categories, pie_chart_file, recursion_level):
    #plotting
    labels = []
    sizes = []
    for category, files in file_categories.items():
        labels.append(category)
        sizes.append(len(files))

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})

    ax.set_title(f"Recursion Level {recursion_level}")

    plt.tight_layout()
    #saving the plot to the pdf
    if is_pdf_empty(pie_chart_file):
        with PdfPages(pie_chart_file, 'a') as pdf:
            pdf.savefig(fig, bbox_inches='tight')
    else:
        temp_file = 'temp_plot.pdf'
        plt.savefig(temp_file, bbox_inches='tight')
        plt.close()

        # Merge the temporary PDF file with the existing PDF file
        merger = PdfMerger()
        merger.append(PdfReader(pie_chart_file, 'rb'))
        merger.append(PdfReader(temp_file, 'rb'))
        merger.write(pie_chart_file)
        merger.close()

        # Remove the temporary PDF file
        os.remove(temp_file)



class CrawlStatistics:
    def __init__(self):
        # Start time of the crawling process
        self.start_time = time.time()
        # Total number of pages crawled
        self.pages_crawled = 0
        # Total response time of all the crawled pages
        self.total_response_time = 0
        # Total number of errors encountered during crawling
        self.error_count = 0

    def increment_pages_crawled(self):
        """
        Increment the count of crawled pages.
        """
        self.pages_crawled += 1

    def add_response_time(self, response_time):
        """
        Add the response time of a crawled page to the total response time.
        
        Parameters:
        - response_time: Response time of a crawled page in seconds.
        """
        self.total_response_time += response_time

    def increment_error_count(self):
        """
        Increment the count of encountered errors during crawling.
        """
        self.error_count += 1

    def get_average_response_time(self):
        """
        Calculate the average response time of crawled pages.

        Returns:
        - Average response time in seconds.
        """
        if self.pages_crawled > 0:
            return self.total_response_time / self.pages_crawled
        else:
            return 0

    def get_elapsed_time(self):
        """
        Get the elapsed time of the crawling process.

        Returns:
        - Elapsed time in seconds.
        """
        return time.time() - self.start_time

    def get_error_rate(self):
        """
        Calculate the error rate of crawled pages.

        Returns:
        - Error rate as a percentage.
        """
        if self.pages_crawled > 0:
            return self.error_count / self.pages_crawled * 100
        else:
            return 0



def find_unique_links(url):
    #open the webpage using the request library
    response = requests.get(url, verify=False)
    response_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'  #sometimes some alphabets are not decoded, so used it
    #beautiful soup for parsing the html content of the page
    soup = BeautifulSoup(response.content.decode('utf-8', errors='replace'), 'html.parser')

    # Get the base domain of the website
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc

    unique_links = set()
    internal_links = set()
    external_links= set()
    
    #finding the elements with different tags 
    elements = soup.find_all(['a', 'img', 'script', 'link'])

    for element in elements:
        href = element.get('href')
        src = element.get('src')

        if href:
            absolute_href = urljoin(url, href)
            unique_links.add(absolute_href)
            parsed_link = urlparse(absolute_href)
            if parsed_link.netloc == base_domain:
                internal_links.add(absolute_href)

        if src:
            absolute_src = urljoin(url, src)
            unique_links.add(absolute_src)
            parsed_link = urlparse(absolute_src)
            if parsed_link.netloc == base_domain:
                internal_links.add(absolute_src)
            else:
                external_links.add(absolute_src)

    return unique_links, internal_links, external_links, response_time


def recursive_crawling(internal_links_passed, depth, depth_threshold, output_file, crawl_stats, plot_pie_chart, pie_chart_file, include_internal, include_external):
    categories = {
        'html': 'Html',
        'htm': 'Html',
        'css': 'Css',
        'jpg': 'Jpg',
        'jpeg': 'Jpg',
        'png': 'Png',
        'gif': 'Gif',
        'js': 'Js',
        'pdf': 'Pdf',
        'doc': 'Doc',
        'docx': 'Doc',
        'xls': 'Excel',
        'xlsx': 'Excel',
        'ppt': 'PowerPoint',
        'pptx': 'PowerPoint',
        'txt': 'Text',
        'zip': 'Zip',
        'rar': 'Zip',
        'xml': 'Xml',
        'ico': 'Ico',
        'json': 'Json'
    }

    file_categories = {
        'miscellaneous': set()
    }
    

    internal_links = set()
    all_links = set()
    external_links= set()

    for link in internal_links_passed:
        crawled_all, crawled_internal, crawled_external, response_time = find_unique_links(link)
        internal_links.update(crawled_internal)
        all_links.update(crawled_all)
        external_links.update(crawled_external)
        crawl_stats.increment_pages_crawled()
        crawl_stats.add_response_time(response_time)

    
    for file_link in all_links:
        file_extension = file_link.split('.')[-1].lower()
        category = categories.get(file_extension, 'miscellaneous')
        if category not in file_categories:
            file_categories[category] = set()
        file_categories[category].add(file_link)


    output = []
    if include_internal:
        output.append("--- Internal Links ---")
        for link in internal_links:
            output.append(link)

    if include_external:
        output.append("--- External Links ---")
        for link in external_links:
            output.append(link)
   
    output.append(f"Recursion level: {depth_threshold + 1 - depth}")
    output.append(f"Total files found: {len(all_links)}")

    for category, files in file_categories.items():
        output.append(f"{category}: {len(files)}")
        for file in files:
            output.append(file)

    output_string = '\n\n'.join(output)

    if output_file is None:
        print(output_string)
    else:
        output_file.write(output_string)
        output_file.write('\n\n')
        
    if plot_pie_chart:
        pie_chart(file_categories, pie_chart_file, depth_threshold + 1 - depth)

 
    if depth > 1 and len(internal_links) > 0:
        recursive_crawling(internal_links, depth - 1, depth_threshold, output_file, crawl_stats, plot_pie_chart, pie_chart_file, include_internal, include_external)

def infinite_recursive_crawling(internal_links_passed, output_file, crawl_stats, plot_pie_chart, pie_chart_file, include_internal, include_external):
    global n
    categories = {
        'html': 'Html',
        'htm': 'Html',
        'css': 'Css',
        'jpg': 'Jpg',
        'jpeg': 'Jpg',
        'png': 'Png',
        'gif': 'Gif',
        'js': 'Js',
        'pdf': 'Pdf',
        'doc': 'Doc',
        'docx': 'Doc',
        'xls': 'Excel',
        'xlsx': 'Excel',
        'ppt': 'PowerPoint',
        'pptx': 'PowerPoint',
        'txt': 'Text',
        'zip': 'Zip',
        'rar': 'Zip',
        'xml': 'Xml',
        'ico': 'Ico',
        'json': 'Json'
    }

    file_categories = {
        'miscellaneous': set()
    }

    internal_links = set()
    all_links = set()
    external_links=set()

    for link in internal_links_passed:
        crawled_all, crawled_internal, crawled_external, response_time = find_unique_links(link)
        internal_links.update(crawled_internal)
        all_links.update(crawled_all)
        external_links.update(crawled_external)
        crawl_stats.increment_pages_crawled()
        crawl_stats.add_response_time(response_time)

    
    for file_link in all_links:
        file_extension = file_link.split('.')[-1].lower()
        category = categories.get(file_extension, 'miscellaneous')
        if category not in file_categories:
            file_categories[category] = set()
        file_categories[category].add(file_link)


    output = []
       
    if include_internal:
        output.append("--- Internal Links ---")
        for link in internal_links:
            output.append(link)

    if include_external:
        output.append("--- External Links ---")
        for link in external_links:
            output.append(link)

    output.append(f"Recursion level: {n}")
    output.append(f"Total files found: {len(all_links)}")
 

    for category, files in file_categories.items():
        output.append(f"{category}: {len(files)}")
        for file in files:
            output.append(file)

    output_string = '\n\n'.join(output)

    if plot_pie_chart:
        pie_chart(file_categories, pie_chart_file, n)
    
    n=n+1

    if output_file is None:
        print(output_string)
        print('\n')
    else:
        output_file.write(output_string)
        output_file.write('\n\n')

    if  len(internal_links) == 0 or internal_links == internal_links_passed:
        return None
    else:
        infinite_recursive_crawling(internal_links, output_file, crawl_stats, plot_pie_chart, pie_chart_file,include_internal, include_external)


def main():
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-u', '--url', help='URL to crawl', required=True)
    parser.add_argument('-t', '--threshold', type=int, help='Recursion threshold')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot pie charts')
    parser.add_argument('-i', '--include-internal', action='store_true', help='Include internal links')
    parser.add_argument('-e', '--include-external', action='store_true', help='Include external links')
    parser.add_argument('-pc', '--pie-chart', help='PDF file to save pie charts')


    args = parser.parse_args()

    if args.url is None:
        parser.error('Error: URL is required.')
        return

    initial_links = set([args.url])
    
    output_file = None
    if args.output:
        output_file = open(args.output, 'w')
        print('Output file:', args.output)
    else:
        print('Output file: Standard Output')

    crawl_stats = CrawlStatistics()


    if args.threshold is None:
        infinite_recursive_crawling(initial_links,output_file, crawl_stats, args.plot, args.pie_chart, args.include_internal, args.include_external)
    else:
        depth_threshold = args.threshold

        if depth_threshold <= 0:
            print('Error: Invalid threshold. Threshold must be greater than 0.')
            return
        
        recursive_crawling(initial_links, depth_threshold, depth_threshold, output_file, crawl_stats, args.plot, args.pie_chart, args.include_internal, args.include_external)


    if output_file is not None:
        output_file.close()
    
    print("\n")
    print("--- Crawl Statistics ---")
    print(f"Pages Crawled: {crawl_stats.pages_crawled}")
    print(f"Average Response Time: {crawl_stats.get_average_response_time():.2f} seconds")
    print(f"Elapsed Time: {crawl_stats.get_elapsed_time():.2f} seconds")
    print(f"Error Rate: {crawl_stats.get_error_rate():.2f}%")

if __name__ == '__main__':
    main()
