import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

pres = ['tokyo', 'kanagawa', 'saitama', 'chiba']#全国の不動産(hokkaido)なども可
url="https://www.home4u.jp"

for pre in pres:
  res = requests.get(url + "/sell/company/" + pre)#urlの取得
  soup = BeautifulSoup(res.text, 'html.parser')#指定したurlのhtml情報の取得

  name_data = []#会社名を代入するための配列
  pos_data = []#住所を代入するための配列
  tel_data = []#電話番号を代入するための配列
  fax_data = []#FAX番号を代入するための配列

  ###会社名の取得
  names = soup.find_all('span', attrs={'class':'relComWrapName'})#htmlのspanタグのrelComWrapNameクラスの要素を全て取得
  for name in names:
    company_name = name.find('a').text#会社名の取得
    print(company_name)
    name_data.append(company_name)#配列にcompany_nameの追加

  #会社の住所の取得
  positions = soup.find_all('dd', attrs={'class': 'addrSetCts'})#htmlのddタグのaddSetCtsクラスの要素を全て取得
  for pos in positions:
    company_position = pos.text#住所の取得
    print(company_position)
    pos_data.append(company_position)#配列にcompany_positionの追加


  #電話番号・FAX番号の取得
  for tel_url in names:
    tel_url = tel_url.find('a').get('href')#aタグのリンク先の取得
    res = requests.get(url + tel_url)#リンク先のurl取得
    soup = BeautifulSoup(res.text, 'html.parser')#リンク先のhtml要素の取得
    tel = soup.find_all('td')[1].text#電話番号の取得
    fax = soup.find_all('td')[2].text#FAXの取得
    time.sleep(0.1)#0.1秒停止
    print(tel)
    print(fax)
    tel_data.append(tel)#配列にtelの追加
    fax_data.append(fax)#配列にfaxの追加


  #会社名、住所、電話番号、FAX番号の列に配列の値を代入
  df = pd.DataFrame({
    "会社名": name_data,
    "住所": pos_data,
    "電話番号": tel_data,
    "FAX番号(連絡先)": fax_data
  })
  df.to_csv(f'不動産情報{pre}.csv', index=False)#csvファイル出力
  df.to_excel(f'不動産情報{pre}.xlsx', index=False)#xlsxファイル出力