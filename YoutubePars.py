from requests_html import HTMLSession
from colorama import Fore 
from bs4 import BeautifulSoup as bs
import re
import json
session = HTMLSession()
def get_video_info(url):
    response = session.get(url)
    response.html.render(timeout=60)
    soup = bs(response.html.html, "html.parser")
    result = {}
    result["title"] = soup.find("meta", itemprop="name")['content']
    result["views"] = soup.find("meta", itemprop="interactionCount")['content']
    result["description"] = soup.find("meta", itemprop="description")['content']
    result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
    result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_json = json.loads(data)
    videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
    videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
    likes_str = likes_label.split(' ')[0].replace(',','')
    result["likes"] = '0' if likes_str == 'No' else likes_str
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    result["likes"] = ''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ])
    result["likes"] = 0 if result['likes'] == '' else int(result['likes'])
    channel_name = soup.find("span", itemprop="author").next.next['content']
    channel_subscribers = videoSecondaryInfoRenderer['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']
    result['channel'] = {'name': channel_name, 'subscribers': channel_subscribers}
    return result

if __name__ == "__main__":
    url = input(f"{Fore.RED}Ссылку -> ")    
    
    data = get_video_info(url)
    print(f"{Fore.GREEN}Тайтл типА: {data['title']}")
    print(f"{Fore.GREEN}Просмотры: {data['views']}")
    print(f"{Fore.GREEN}Дата публикации: {data['date_published']}")
    print(f"{Fore.GREEN}Продолжительность: {data['duration']}")
    print(f"{Fore.GREEN}Тэги: {data['tags']}")
    print(f"{Fore.GREEN}Лайки: {data['likes']}")
    print(f"\n{Fore.GREEN}Описание: {data['description']}\n")
    print(f"\n{Fore.GREEN}Название канала: {data['channel']['name']}")
    print(f"{Fore.GREEN}Cабы: {data['channel']['subscribers']}")
