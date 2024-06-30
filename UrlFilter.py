# -*- coding: UTF-8 -*-
# Time : 2024/6/29 下午3:53
# FILE : UrlFilter
# PROJECT : myFilter
# Author : kkk

"""
1.格式化url
2.域名ip分类
"""
from urllib.parse import urlparse, urlunparse
import re


class UrlFilter:

    @staticmethod
    def url_format(rule_path, url_path) -> list:
        """
        去除指定后缀的url
        url前缀补齐斜杠
        url后缀去除 \
        :param rule_path:
        :param url_path:
        :return:
        """
        rule_list = []
        url_list = []
        new_url_list = []
        # 获取规则列表
        with open(rule_path, encoding="utf-8") as fp:
            content = fp.read().strip()
            rule_list = content.split('\n')
        # 获取待操作url
        with open(url_path, encoding="utf-8") as fp:
            content = fp.read().strip()
            url_list = content.split('\n')
        # 对每个url操作
        for url in url_list:
            # 得到path部分
            url = urlparse(url)
            # 去除后缀,先去除,才能匹配到最后的后缀
            with open("./subfix.txt", encoding="utf-8") as fp:
                content = fp.read().strip()
                delete_subfix = content.split('\n')
            for subfix in delete_subfix:
                if url.path.lower().endswith(subfix):
                    url = url._replace(path=url.path[:-len(subfix)])
            # 斜杠替换
            if not url.path.lower().endswith(tuple(rule_list)):
                # 替换斜杠
                url = url._replace(path=url.path
                                   .replace("../", "qclbyx@gmail.com")
                                   .replace("./", "/")
                                   .replace("//", "/")
                                   .replace("qclbyx@gmail.com", "../")
                                   )
                # 添加前缀
                if not url.path.startswith("/"):
                    url = url._replace(path=f"/{url.path}")
                res_url = urlunparse(url)
                new_url_list.append(res_url)

        return new_url_list
        pass

    @staticmethod
    def domain_ip_detach(subdomain_ip_file: str) -> tuple:
        ip_list = []
        domain_list = []

        file = open(subdomain_ip_file, encoding="utf-8")
        domain_ip_list = file.read().strip().split("\n")
        file.close()
        # print(domain_ip_list)
        # ip正则
        patten = re.compile(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
        for item in domain_ip_list:
            res = patten.match(item)
            if res:
                ip_list.append(item)
            else:
                domain_list.append(item)

        return ip_list, domain_list

    @staticmethod
    def purify_subdomain(target_file: str, root_domain_file: str) -> list:
        """
        返回包含根域名整体关键字的所有子域名
        :param target_file: 目标子域名文件
        :param root_domain_file: 存放根域名的文件
        :return: 包含根域名整体关键字的子域名列表
        """
        result = []

        # 读取根域名文件，获取所有根域名
        with open(root_domain_file, encoding='utf-8') as f_root:
            root_domains = [line.strip() for line in f_root.readlines() if line.strip()]

        # 遍历目标子域名文件，筛选出包含根域名整体关键字的子域名
        with open(target_file, encoding='utf-8') as f_target:
            for line in f_target:
                subdomain = line.strip()
                # 检查是否包含任何根域名的整体关键字
                for root_domain in root_domains:
                    if root_domain in subdomain:
                        result.append(subdomain)
                        break  # 找到匹配的根域名后结束循环

        return result


if __name__ == '__main__':
    # url_list = UrlFilter.url_format("./rule.txt", "./url.txt")
    # for url in url_list:
    #     print(url)

    # ip, domain = UrlFilter.domain_ip_detach("./subdomain_ip.txt")
    # print(ip, domain)

    subdomain = UrlFilter.purify_subdomain("./subdomain_ip.txt", "root_domain.txt")
    print(subdomain)
    pass
