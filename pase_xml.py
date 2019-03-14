import os
import xml.etree.ElementTree as etree
import json
from collections import OrderedDict
import copy

num = 0
help_list = []

def parse_data(root, all_list):

    child_list = root.getchildren()
    num = 0
    for child in child_list:

        if child.getchildren() == []:
            all_list.append([child.tag, child.text])
        if child.getchildren() != []:
            all_list.append([child.tag, []])
            # print(all_list)
            save_list = all_list[num][1]
            parse_data(child, save_list)
        num += 1
    return all_list


def get_element(child, temp_list):
    """
    获得中间元素
    """
    tag_list = [[i.tag, i] for i in temp_list]
    for item in tag_list:
        if child.tag == item[0]:
            # 返回element
            return item[1]
    return None


def convert_json(root, all_dict):
    """
    改为字典的形式
    """
    global num
    child_list = root.getchildren()
    temp_list = copy.deepcopy(child_list)
    # print([i.tag for i in temp_list])
    for child in child_list:
        # print('temp_list', temp_list)
        print('child', child.tag, child.text)
        # print('num', num)
        temp_element = get_element(child, temp_list)
        if temp_element is not None:
            temp_list.remove(temp_element)

        if child.tag not in [i.tag for i in temp_list]:
            # 没有相同的子节点
            if child.getchildren() == []:
                all_dict[child.tag] = child.text

            if child.getchildren() != []:
                if all_dict.get(child.tag) is not None:
                    # 判断key是否有值, 没有值则创建,有值则添加
                    mid_list = all_dict[child.tag]
                    mid_list.append({})
                    print('mid_list', mid_list)
                    print('help', help_list)
                    num = help_list.pop()
                    save_dict = mid_list[num]
                    print('save_dict', save_dict)
                    num += 1
                    help_list.append(num)
                    # print(save_dict)
                    convert_json(child, save_dict)
                else:
                    all_dict[child.tag] = {}
                    save_dict = all_dict[child.tag]
                    print('help_', help_list)
                    print('svae', save_dict)
                    # num = 0
                    # help_list.append(num)
                    convert_json(child, save_dict)

        else:
            if child.getchildren() == []:

                all_dict[child.tag] = child.text
            if child.getchildren() != []:
                # 判断 合并

                if all_dict.get(child.tag) is not None:
                    mid_list = all_dict[child.tag]
                    mid_list.append({})
                    num = help_list.pop()
                    # print(help_list)
                    # print(num)
                    save_dict = mid_list[num]
                    num += 1
                    help_list.append(num)
                    convert_json(child, save_dict)
                else:
                    all_dict[child.tag] = []
                    mid_list = all_dict[child.tag]
                    mid_list.append({})

                    num = 0
                    help_list.append(num)
                    save_dict = mid_list[0]
                    # num += 1
                    # print(save_dict)
                    convert_json(child, save_dict)

    return all_dict

temp_dict = {}
def get_json(node):
    """
    递归调用，实现
    """
    temp_dict = {}
    # 递归出口
    if node.getchildren() == []:
        temp_dict[node.tag] = node.text

    if node.getchildren() != []:
        # 判断是否存在子节点重复
        child_list = node.getchildren()
        # print(child_list)
        for child in child_list:
            res = check_list(child, child_list)
            if res == True:
                # 有重复节点,生成数组[]
                # 是否append
                if temp_dict.get(child.tag) == None:
                    temp_dict[child.tag] = [get_json(child)]
                else:
                    temp_dict[child.tag].append(get_json(child))
            else:
                # 没有重复节点
                get_json(child)
            # 子节点是否还存在子节点,递归
            get_json(child)
    return temp_dict

def check_list(node, child_list):
    """
    判断列表中是否有和自己重复的元素
    """
    child_list.remove(node)
    if child_list == None:
        return False
    if node.tag in [i.tag for i in child_list]:
        # 重复返回True
        return True
    else:
        return False

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    xmlpath = os.path.join(dir_path, 'style1.xml')
    # tree = etree.parse(xmlpath)
    # root = tree.getroot()
    # all_list = []
    # res = parse_data(root, all_list)
    # print('res===', res)
    # --------------------------
    tree = etree.parse(xmlpath)
    root = tree.getroot()
    all_dict = OrderedDict()
    num = 0
    # res = convert_json(root, all_dict)
    res = get_json(root)

    print('res===', res)
    print(json.dumps(res))
