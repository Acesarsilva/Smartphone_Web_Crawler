import pandas as pd
import util

def main():
    start_links = pd.read_csv('start_links.csv')['links'].tolist()
    downloaded_url = []
    border = start_links
    while(border):
        url = border.pop(0)
        if (url not in downloaded_url):
            try:
                html = util.download_url(url)
                #call html classifier
                links = util.get_links(html,url)
                border.extend(links)
                downloaded_url.append(url)
                print(downloaded_url)
            except:
                print('Bad Download: ', url)
                border.append(url)

if __name__ == "__main__":
    main()