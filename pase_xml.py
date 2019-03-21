import os
import json
import copy
import xml.etree.ElementTree as etree
from collections import OrderedDict


num = 0
help_list = []


def parse_data(root, all_list):
    """
    由于用的是单列表的方式, 层级关系用一个变量即可控制,
    若以字典的形式保存,则会出现同级多层列表,无法使用这种方式来控制

    递归的实现,则是建立在当前的父问题的角度考虑,假设子问题已经实现,所以该法会在子问题结束时返回,
    即[[...[key, value]...]]不断嵌套回去
    :param root: node object
    :param all_list: arraylist
    :return:
    """
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
    notice: 弃用,无法解析多层xml
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
                    print('save', save_dict)
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


def get_json(node):
    """
    递归调用，实现
    process:
        1.判断传入的节点是否有子节点
            有:
                判断该节点是否是唯一元素
                是:
                    不生成数组,递归
                否:
                    生成数组, 递归
            否:
                没有子节点,到达递归出口

        # 方式二(感觉有点小问题)
        2.判断传入的节点是否有子节点
            有:
                判断该子节点是否有同级节点的重复

                有重复:  生成数组  ---> 判断是否含有子节点(递归)
                无重复: 不生成数组 ---> 判断是否含有子节点(递归)
            否:
                没有子节点,到达递归出口
    """
    temp_dict = OrderedDict()
    # 从数组中取node
    if isinstance(node, list):
        node = node[0]

    # 递归出口
    if node.getchildren() == []:
        temp_dict[node.tag] = node.text

    if node.getchildren() != []:
        child_list = node.getchildren()

        # 判断元素是否唯一
        if len(child_list) == 1:
            temp_dict[child_list[0].tag] = get_json(child_list)
        else:
            for child in child_list:

                if temp_dict.get(child.tag) == None:
                    temp_dict[child.tag] = [get_json(child)]
                    # mid_dict = [get_json(child)]
                    # temp_dict[child.tag] = mid_dict
                else:
                    temp_dict[child.tag].append(get_json(child))
                    # mid_dict = get_json(child)
                    # temp_dict[child.tag].append(mid_dict)
    return temp_dict


def check_list(node, child_list):
    """
    判断列表中是否有和自己重复的元素
    notice: 比较的对象为element对象,且不可修改原有的节点列表
    """
    help_list = copy.deepcopy(child_list)
    tmp_list = list(zip(help_list, child_list))  # 0 为copy, 1为real
    i = 0
    for item in tmp_list:
        if node == item[1]:
            tmp_list.pop(i)
        i += 1

    comp_list = [i[1] for i in tmp_list]

    if comp_list == None:
        return False
    if node.tag in [i.tag for i in comp_list]:
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
