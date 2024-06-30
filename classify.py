# -*- coding: UTF-8 -*-
# Time : 2024/6/30 下午1:56
# FILE : classify
# PROJECT : myFilter
# Author : kkk

import argparse

from UrlFilter import UrlFilter

root_parser = argparse.ArgumentParser(description='''
    功能:
    1.url格式化过滤，去除rule文件中定义的后缀的url资源，并输出到新文件 formated_url.txt
    2.域名与ip分离，并分别输出到 ip.txt domain.txt
    3.根据root_domain中的根域名过滤出对应的子域名，输出到 subdomain.txt
    
    默认文件:
    rule.txt        url格式化时，去除rule文件中定义的后缀的url
    subfix.txt      url格式化时，去除subfix文件定义的后缀，不去除该行，用于去除尾部无用字符
    root_domain.txt 子域名提取时，提取root_domain的所有子域名和有关域名
''', formatter_class=argparse.RawTextHelpFormatter)

# 添加文件参数
root_parser.add_argument('-f', '--file', default="./url.txt", help="待操作文件路径")
# 添加rule文件参数
root_parser.add_argument('-r', '--rule', default="./rule.txt", help="rule文件路径")
# 添加root文件参数
root_parser.add_argument('--root', default="./root_domain.txt", help="根域名文件路径")
# 添加格式化参数
root_parser.add_argument('--format', action='store_true',
                         help="将文件内容中的rule.txt规定的后缀的url去除,并去除subfix.txt中规定的后缀")
# 添加分离参数
root_parser.add_argument('--detach', action='store_true', help="将文件分离为domain.txt和ip.txt")

# 添加分离参数
root_parser.add_argument('--purity', action='store_true', help="根据root_domain中的规则提取对应的子域名")

args = root_parser.parse_args()


def format_file(file_path):
    url_list = UrlFilter.url_format("./rule.txt", file_path)
    with open("./output/formated_url.txt", 'w', encoding="utf-8") as fp:
        for item in url_list:
            fp.write(item + "\n")


def detach_file(file_path):
    ip, domain = UrlFilter.domain_ip_detach(file_path)

    ip_file = open("./output/ip.txt", mode="w", encoding="utf-8")
    for item in ip:
        ip_file.write(item + "\n")
    ip_file.close()

    domain_file = open("./output/domain.txt", mode="w", encoding="utf-8")
    for item in domain:
        domain_file.write(item + "\n")
    domain_file.close()


def purify_subdomain(file):
    subdomain = UrlFilter.purify_subdomain(file, args.root)
    with open("./output/subdomain.txt", mode='w', encoding="utf-8") as fp:
        for item in subdomain:
            fp.write(item + "\n")
    pass


if args.format:
    print("格式化文件中")
    format_file(args.file)
    print("格式化文件成功,文件保存在output/formated_url.txt中")
elif args.detach:
    print("分离文件中,文件保存在output/domain.txt和output/ip.txt中")
    detach_file(args.file)
    print("分离文件成功")
elif args.purity:
    print("提取域名中")
    purify_subdomain(args.file)
    print(f"提取域名成功,文件保存在output/subdomain.txt中")
else:
    print("请选择操作参数，详情运行 -h 参数查看")
