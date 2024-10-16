import json

link_list = []


with open('testing.json', 'r', encoding='utf-8') as jf:
    data = json.load(jf)
    
for div in data:
    links = div.get('links', [])

    if len(links) >= 2:
        link_list.append(links[1])
        print(1)

    else:
        pass


print(link_list)
    # print(json.dumps(data, indent=4, ensure_ascii=False))
