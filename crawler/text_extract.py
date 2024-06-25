from bs4 import BeautifulSoup

def extract_anchors(soup):
    """
    HTML 문서에서 'a' 태그의 텍스트를 추출합니다.
    """
    count = 0
    a_list = []
    for element in soup.descendants:
        if element.name == 'a':
            text = element.get_text()
            a_list.append(text)
    
    a_list = [a for a in a_list if a != '[편집]' and a != '[편집 요청 도움말]']
    a_list = [a for a in a_list if a.startswith('[') and a.endswith(']')]
    return a_list

def extract_tag_data(tag_data, a_list):
    """
    텍스트에서 'a' 태그의 내용을 기반으로 데이터를 분리하여 사전에 저장합니다.
    """
    anker_list = [anker for anker in a_list if anker.startswith('[') and anker.endswith(']')]
    
    tag_set = {}
    count = 0
    while count < len(anker_list):
        cur_pos = tag_data.find(anker_list[count])
        next_pos = tag_data.find(anker_list[count + 1]) if count + 1 < len(anker_list) else -1
        if cur_pos != -1:
            tag_set[anker_list[count]] = (
                tag_data[cur_pos + len(anker_list[count]): next_pos] if next_pos != -1 else tag_data[cur_pos + len(anker_list[count]):]
            ).strip()
        count += 1
    return tag_set

def replace_keys_with_values(text, tag_set):
    """
    텍스트에서 키를 값으로 대체합니다.
    """
    for key, value in tag_set.items():
        text = text.replace(key, f" ({value}) ")
    return text

def remove_display_none(soup):
    """
    'display: none' 스타일을 가진 모든 요소를 제거합니다.
    """
    for element in soup.find_all(style=True):
        if element.attrs == None:
            continue
        if element and 'style' in element.attrs:
            style = element['style']
            if 'display:none' in style.replace(' ', '').lower():
                element.decompose()

def main():
    # 파일에서 HTML 내용 읽기
    with open('./output/test.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # BeautifulSoup을 사용하여 HTML 내용 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 'display: none' 스타일을 가진 요소 제거
    remove_display_none(soup)

    # 텍스트 추출
    text_data = soup.get_text()
    with open('./text_data.txt', 'w', encoding='utf-8') as file:
        file.write(text_data)

    # '[편집]' 텍스트 제거
    text_data = text_data.replace('[편집]', '')
    text_data = text_data.replace('[편집 요청 도움말]', '')


    # 'a' 태그 텍스트 추출
    a_list = extract_anchors(soup)
    new_a_list = list(dict.fromkeys(a_list))

    # print(new_a_list)

    
    # print(a_list)
    
    # 텍스트 분리 및 광고 제거
    split_text = text_data.split('\n')
    with open('./output/split_text.txt', 'w', encoding='utf-8') as file:
        for line in split_text:
            file.write(line + '\n')

    namu_data_index = -1;
    for i in range(len(split_text)):
        if split_text[i].find('분류') != -1:
            namu_data_index = i
            namu_data = split_text[i]
            break
    ad_index = namu_data.find('파워링크')
    namu_data = namu_data[:ad_index].strip()
    
    tag_data_index = -1
    for i in reversed(range(len(split_text))):
        find = True
        tag_data = split_text[i]
        for tag in new_a_list:
            if tag_data.find(tag) == -1:
                find = False
                break
        if find == True:
            tag_data_index = i
            break
    
    new_a_list = sorted(new_a_list, key=lambda x: tag_data.rfind(x))
    print(new_a_list)


    # 필요시 본문 데이터와 태그 데이터를 분리해서 저장
    if tag_data_index == namu_data_index:
        tag_data = namu_data[namu_data.rfind(new_a_list[0]):].strip()
        namu_data = namu_data[0: namu_data.rfind(new_a_list[0])].strip()

    #저작물 관련 문구 제거
    ad_index = namu_data.find('이 저작물은')
    if ad_index != -1:
        namu_data = namu_data[:ad_index].strip()

    #저작물 관련 문구 제거
    ad_index = tag_data.find('이 저작물은')
    if ad_index != -1:
        tag_data = tag_data[:ad_index].strip()


    tag_set = extract_tag_data(tag_data, new_a_list)

    # 태그 키를 값으로 대체
    namu_data = replace_keys_with_values(namu_data, tag_set)
    
    # 추출된 텍스트를 새로운 파일에 저장
    with open('./output/namu_data.txt', 'w', encoding='utf-8') as file:
        file.write(namu_data)

if __name__ == "__main__":
    main()
