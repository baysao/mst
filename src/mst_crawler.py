# -*- coding: utf-8 -*-

import json
from random import randrange
import requests
from lxml import html
from loguru import logger
import time
from libs.user_agent import USER_AGENT

import os
# import database
import pattern

useragent = USER_AGENT[randrange(len(USER_AGENT) - 1)]
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
const_headers = {"User-Agent": useragent}
const_proxies = False

ignore_text = ["Bị ẩn theo yêu cầu người dùng"]


def get_request(path_url, headers={}, proxies=False):
    url = f"{pattern.BASE_URL}{path_url}"
    header = {}
    header.update(headers)
    logger.info(
        f"Send GET request:\n- URL: {url}\n- Header: {header}\n- Proxy: {proxies}"
    )
    response = requests.get(url, headers=headers, proxies=proxies)
    # response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        logger.info("Send GET request successfully")
        return tree
    else:
        logger.error(f"Failed to retrieve content. Status code: {response.status_code}")
        return False


def is_more_data(handler_page, active_page, els):
    return handler_page == active_page and els


def crawl_data_province(url, headers=const_headers, proxies=False):
    tree = get_request(url, headers, proxies)
    if not tree:
        logger.error("Failed to get data provinces")
        return

    # conn = database.get_db_connection()
    # cur = conn.cursor()

    # Sử dụng XPath để tìm phần tử
    province_els = tree.xpath("//table//tr")
    data_insert = []
    id = 0
    for province_el in province_els:
        id = id + 1
        province_info = province_el.xpath(".//a")[0]
        province_name = province_info.text_content().strip()
        province_link = province_info.get("href")
        data_insert.append({"id": id, "name": province_name, "slug": province_link})
        # logger.info(f"- {province_name} | {province_link}")
        # sql = """
        #     INSERT INTO mst_province (name, slug)
        #     VALUES (%s, %s)
        # """
        # cur.execute(sql, (province_name, province_link))

    # database.end_db_connection(cur, conn)
    y = json.dumps(data_insert, indent=4)
    print(y)
    with open("province.json", "w") as outfile:
        outfile.write(y)
        # json.dump(y, outfile)

    logger.info(f"Get provinces data successfully. Total: {len(province_els)}")
    return


def crawl_data_district(headers=const_headers, proxies=False):
    provinces = []
    with open("province.json", "r") as openfile:
        provinces = json.load(openfile)
   
    for province in provinces:
        crawl_data_district_by_province(province, headers, proxies)
        time.sleep(3)
   
# def crawl_data_all_district(headers=const_headers, proxies=False):
#     provinces = []
#     with open("province.json", "r") as openfile:
#         provinces = json.load(openfile)

#     data_insert = []   
#     for province in provinces:
#         pro_id = province["id"]
#         with open("district_" + str(prod_id) + ".json", "r") as openfile1:
#             districts = json.load(openfile1)
#             for district in districts:
#                 dis_id = district["id"]
#                 dis_url = district["slug"]
#                 data_insert.insert(crawl_data_district_by_url(dis_url, headers, proxies))
#                 time.sleep(3)
#     y = json.dumps(data_insert, indent=4)
#     print(y)
def crawl_data_district_by_province(
    province_data, headers=const_headers, proxies=False
    #province_data, cur, conn, headers=const_headers, proxies=False
):
    # province_data = (1, 'Hà Nội', '/tra-cuu-ma-so-thue-theo-tinh/ha-noi-7') | id - name - slug
#    logger.info(f"Get Province in {province_data[1]} by link {province_data[2]}")
    #tree = get_request(province_data[2], const_headers, proxies)
    #print(province_data)
    tree = get_request(province_data["slug"], const_headers, proxies)
    if not tree:
        logger.error("Failed to get data districts")
        return
    

    data_insert = []
    id = 0
    # Sử dụng XPath để tìm phần tử
    district_els = tree.xpath('//div[@id="sidebar"]//li')
    for district_el in district_els:
        id = id + 1
        district_info = district_el.xpath(".//a")[0]
        district_name = district_info.text_content().strip()
        district_link = district_info.get("href")
        logger.info(f"- {district_name} | {district_link}")
        data_insert.append({"id": id, "name": district_name, "slug":district_link, "province_id":  province_data["id"],  "province_name": province_data["name"]})
        # sql = """
        #     INSERT INTO mst_district (name, slug, province_id, province_name)
        #     VALUES (%s, %s, %s, %s)
        # """
        # cur.execute(
        #     sql, (district_name, district_link, province_data[0], province_data[1])
        # )

    y = json.dumps(data_insert, indent = 4)
    print(y)
    with open("district_" + strg(province_data["id"]) + ".json", "w") as outfile:
        outfile.write(y)
        
    logger.info(f"Get districts data successfully. Total: {len(district_els)}")
    return y


# def crawl_data_district_by_url(district, headers=const_headers, proxies=False):
#     dis_url = district["slug"]
#     dis_id = district["id"]
#     tree = get_request(dis_url, headers, proxies)
#     if not tree:
#         logger.error("Failed to get data districts")
#         return

#     data_insert = []
#     id = 0
#     # Sử dụng XPath để tìm phần tử
#     district_els = tree.xpath('//div[@id="sidebar"]//li')
#     for district_el in district_els:
#         id = id + 1
#         district_info = district_el.xpath(".//a")[0]
#         district_name = district_info.text_content().strip()
#         district_link = district_info.get("href")
#         print(f"- {district_name} | {district_link}")
#         data_insert.append({"id": id, "name": district_name, "slug":district_link, "province_id":  province_data["id"],  "province_name": province_data["name"]})

#     with open("district_" + strg(province_data["id"]) + ".json", "w") as outfile:
#         outfile.write(y)        
#     logger.info(f"Get districts data successfully. Total: {len(district_els)}")
#     return


def crawl_data_career(url, headers=const_headers, proxies=False):
    # conn = database.get_db_connection()
    # cur = conn.cursor()

    is_more = True
    handle_page = 1
    try_count = 0
    total_crawl = 0
    id = 0
    data_insert = []
    while is_more:
        time.sleep(3)
        handle_url = f"{url}?page={handle_page}"
        try:
            tree = get_request(handle_url, headers, proxies)
            if not tree:
                logger.error("Failed to get data career")
                return
        except requests.exceptions.RequestException as err:
            logger.error(err.response.json())
            if try_count > 3:
                logger.info("Not have more data need crawl.")
                is_more = False
                return err.response.json()
            else:
                try_count += 1
                logger.warning("Try crawl more data!")

        # Sử dụng XPath để tìm phần tử
        career_els = tree.xpath("//tbody//tr")

        for career_el in career_els:
            id = id + 1
            career_code_info = career_el.xpath(".//td[1]//a")[0]
            career_code = career_code_info.text_content().strip()
            career_name = career_el.xpath(".//td[2]//a")[0].text_content().strip()
            career_link = career_code_info.get("href")
            obj = {"id": id, "code": career_code, "name": career_name, "slug": career_link}
            print(obj)
            data_insert.append(obj)
            print(f"- {career_code} | {career_name} | {career_link}")
            # sql = """
            #             INSERT INTO mst_career (code, name, slug)
            #             VALUES (%s, %s, %s)
            #         """
            # cur.execute(sql, (str(career_code), career_name, career_link))

        total_crawl += len(career_els)

        active_pages = tree.xpath('//span[@class="page-numbers current"]')
        active_page = int(active_pages[0].text_content().strip())
        if is_more_data(handle_page, active_page, career_els):
            handle_page += 1
            try_count = 0
            logger.info("Have more data need crawl")
        else:
            if try_count > 3:
                logger.info("Not have more data need crawl.")
                is_more = False
            else:
                try_count += 1
                logger.warning("Try crawl more data!")
        logger.info(f"Get districts data successfully. Total: {total_crawl}")
    y = json.dumps(data_insert, indent = 4)        
    with open("careers.json", "w") as outfile:
        outfile.write(y) 
    #database.end_db_connection(cur, conn)
    return


def crawl_data_company(crawl_by="district", headers=const_headers, proxies=False):
    logger.info(f"Get companies data by {crawl_by}")
    provinces = []
    with open("province.json", "r") as openfile:
        provinces = json.load(openfile)
       
        for province in provinces:
            print(province)
            pro_id = province["id"]
            with open("district_" + str(pro_id) + ".json", "r") as openfile1:
                districts = json.load(openfile1)
                for district in districts:
                    print(district)
                    crawl_data_company_by_data(crawl_by, province, district, headers, proxies)

    # conn = database.get_db_connection()
    # cur = conn.cursor()
    # sql_by_mode = {
    #     "province": "SELECT * FROM mst_province;",
    #     "district": "SELECT * FROM mst_district;",
    #     "career": "SELECT * FROM mst_career;",
    # }
    # cur.execute(sql_by_mode.get(crawl_by))
    # datas = cur.fetchall()
#   for data in datas:
        # district_data = (1, 'Hà Nội', '/tra-cuu-ma-so-thue-theo-tinh/ha-noi-11483', 1, 'Hà Nội') | id, name, slug, province_id, province_name
 #      crawl_data_company_by_data(crawl_by, data, cur, conn, headers, proxies)
    #database.end_db_connection(cur, conn)
    logger.info(f"Get companies data by {crawl_by} successfully!")


def crawl_data_company_by_data(
        crawl_by, province, district, headers=const_headers, proxies=False
):
    logger.info(f"crawl_data_company_by_data {crawl_by}.")
    # district_data = (1, 'Hà Nội', '/tra-cuu-ma-so-thue-theo-tinh/ha-noi-11483', 1, 'Hà Nội') | id, name, slug, province_id, province_name
    province_id = None
    district_id = None
    career_id = None
    url = ""
    province_id = district["province_id"]
    district_id = district["id"]
    province_name = province["name"]
    district_name = district["name"]
    url = district["slug"]
    # if crawl_by == "province":
    #     province_id = data[0]
    #     url = data[2]
    # elif crawl_by == "district":
    #     province_id = data["province_id"]
    #     district_id = data["id"]
    #     url = data["slug"]
    # else:
    #     career_id = data[0]
    #     url = data[3]
    logger.info(
        f"crawl_data_company_by_data {crawl_by}:\n- province_id: {province_id}\n- district_id: {district_id}\n- career_id: {career_id}\n- url: {url}"
    )

    is_more = True
    handle_page = 1
    try_count = 0
    total_crawl = 0
    pa = str(province_id) + "/" + str(district_id) 
    os.makedirs(pa, exist_ok=True)
    while is_more:
        handle_url = f"{url}?page={handle_page}"
        try:
            time.sleep(3)
            tree = get_request(handle_url, headers, proxies)
            if not tree:
                logger.error("Failed to get data career")
                return
        except requests.exceptions.RequestException as err:
            logger.error(err.response.json())
            if try_count > 3:
                logger.info("Not have more data need crawl.")
                is_more = False
                return err.response.json()
            else:
                try_count += 1
                logger.warning("Try crawl more data!")

        # Sử dụng XPath để tìm phần tử
        company_els = tree.xpath('//div[@class="tax-listing"]/div')
        for company_el in company_els:
            company_link_el = company_el.xpath("./h3/a")[0]
            company_link = company_link_el.get("href")
            company_name = company_link_el.text_content().strip()
            obj = crawl_data_company_by_url(
                company_link,
                province_id,
                district_id,
                career_id,
                headers,
                proxies,
            )
            obj["province_name"] = province_name
            obj["district_name"] = district_name
            obj["tags"] = [province_name, district_name, company_name]
            y = json.dumps(obj, indent = 4)
            print(y)
            with open(pa + company_link + ".json", "w") as outfile:
                outfile.write(y)            
        total_crawl += len(company_els)

        active_pages = tree.xpath('//span[@class="page-numbers current"]')
        active_page = int(active_pages[0].text_content().strip())
        if is_more_data(handle_page, active_page, company_els):
            handle_page += 1
            try_count = 0
            logger.info("Have more data need crawl")
        else:
            if try_count > 3:
                logger.info("Not have more data need crawl.")
                is_more = False
            else:
                try_count += 1
                logger.warning("Try crawl more data!")
        logger.info(f"Get company data successfully. Total: {total_crawl}")
    return


def crawl_data_company_by_url(
    url="",
    province_id=None,
    district_id=None,
    career_id=None,
    headers={},
    proxies=False,
):
   
    try:
        time.sleep(3)
        tree = get_request(url, headers, proxies)
        if not tree:
            logger.error("Failed to get data company")
            return
    except requests.exceptions.RequestException as err:
        logger.error(err.response.json())
        return err.response.json()

    # Sử dụng XPath để tìm phần tử
    company_els = tree.xpath("//tbody//tr")
    company_name_el = tree.xpath("//thead//span")  # Tên công ty
    company_name_globe_el = tree.xpath(
        '//i[@class="fa fa-globe"]/../../td[2]/span'
    )  # Tên quốc tế
    company_name_short_el = tree.xpath(
        '//i[@class="fa fa-reorder"]/../../td[2]/span'
    )  # Tên viết tắt
    conpany_tax_el = tree.xpath(
        '//i[@class="fa fa-hashtag"]/../../td[2]/span'
    )  # Mã số thuế
    conpany_address_el = tree.xpath(
        '//i[@class="fa fa-map-marker"]/../../td[2]/span'
    )  # Địa chỉ
    conpany_user_el = tree.xpath(
        '//i[@class="fa fa-user"]/../../td[2]/span/a'
    )  # Người đại diện
    conpany_phone_el = tree.xpath(
        '//i[@class="fa fa-phone"]/../../td[2]/span'
    )  # Điện thoại
    conpany_active_date_el = tree.xpath(
        '//i[@class="fa fa-calendar"]/../../td[2]/span'
    )  # Ngày hoạt động
    conpany_manage_el = tree.xpath(
        '//i[@class="fa fa-users"]/../../td[2]/span'
    )  # Quản lý bởi
    conpany_category_el = tree.xpath(
        '//i[@class="fa fa-building"]/../../td[2]/a'
    )  # Loại hình doanh nghiệp
    conpany_status_el = tree.xpath(
        '//i[@class="fa fa-info"]/../../td[2]/a'
    )  # Tình trạng hoạt động
    conpany_last_update_el = tree.xpath("//td//em")  # Cập nhật gần nhất
    company_career_els = tree.xpath(
        '//table[@class="table"]//tbody//tr'
    )  # Ngành nghề kinh doanh

    company_name = (
        len(company_name_el) and company_name_el[0].text_content().strip() or None
    )
    company_name_globe = (
        len(company_name_globe_el)
        and company_name_globe_el[0].text_content().strip()
        or None
    )
    company_name_short = (
        len(company_name_short_el)
        and company_name_short_el[0].text_content().strip()
        or None
    )
    conpany_tax = (
        len(conpany_tax_el) and conpany_tax_el[0].text_content().strip() or None
    )
    conpany_address = (
        len(conpany_address_el) and conpany_address_el[0].text_content().strip() or None
    )
    conpany_user = (
        len(conpany_user_el) and conpany_user_el[0].text_content().strip() or None
    )
    conpany_phone = (
        len(conpany_phone_el) and conpany_phone_el[0].text_content().strip() or None
    )
    conpany_active_date = (
        len(conpany_active_date_el)
        and conpany_active_date_el[0].text_content().strip()
        or None
    )
    conpany_manage = (
        len(conpany_manage_el) and conpany_manage_el[0].text_content().strip() or None
    )
    conpany_category = (
        len(conpany_category_el)
        and conpany_category_el[0].text_content().strip()
        or None
    )
    conpany_status = (
        len(conpany_status_el) and conpany_status_el[0].text_content().strip() or None
    )
    conpany_last_update = (
        len(conpany_last_update_el)
        and conpany_last_update_el[0].text_content().strip()
        or None
    )

    if company_name in ignore_text:
        company_name = None
    if company_name_globe in ignore_text:
        company_name_globe = None
    if company_name_short in ignore_text:
        company_name_short = None
    if conpany_tax in ignore_text:
        company_name = None
    if conpany_address in ignore_text:
        conpany_address = None
    if conpany_user in ignore_text:
        conpany_user = None
    if conpany_phone in ignore_text:
        conpany_phone = None
    if conpany_active_date in ignore_text:
        conpany_active_date = None
    if conpany_manage in ignore_text:
        conpany_manage = None
    if conpany_category in ignore_text:
        conpany_category = None
    if conpany_status in ignore_text:
        conpany_status = None
    if conpany_last_update in ignore_text:
        conpany_last_update = None

    # print('Ngành nghề kinh doanh')
    company_career_code = []
    company_career_name = []
    for company_career in company_career_els:
        career_code_info = company_career.xpath(".//td[1]//a")[0]
        career_code = career_code_info.text_content().strip()
        company_career_code.append(career_code)
        company_career_name.append(
            company_career.xpath(".//td[2]//a")[0].text_content().strip()
        )
    company_career_codes = ", ".join(company_career_code)
    company_career_names = ", ".join(company_career_name)
    obj = {
        "company_name": company_name,
        "company_name_short": company_name_short,
            "company_name_globe": company_name_globe,
            "conpany_tax":conpany_tax,
            "conpany_address": conpany_address,
            "district_id": district_id,
            "province_id": province_id,
            "conpany_user":conpany_user,
            "conpany_phone":conpany_phone,
            "conpany_active_date":conpany_active_date,
            "conpany_manage":conpany_manage,
            "conpany_category":conpany_category,
            "conpany_status":conpany_status,
            "conpany_last_update":conpany_last_update,
            "company_career_codes":company_career_codes,
            "company_career_names":company_career_names,
            "url":url
    }
    # y = json.dumps(obj, indent = 4)
    #print(y)
    
    return obj
    # print(company_career_codes)
    # print(', '.join(company_career_names))

    # sql = """
    #     INSERT INTO mst_company (name, name_short, name_global, tax, address, district_id, province_id, representative, phone, active_date, manage_by, category, status, last_update, career_code, career_name, slug)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    # """
    # cur.execute(
    #     sql,
    #     (
    #         company_name,
    #         company_name_short,
    #         company_name_globe,
    #         conpany_tax,
    #         conpany_address,
    #         district_id,
    #         province_id,
    #         conpany_user,
    #         conpany_phone,
    #         conpany_active_date,
    #         conpany_manage,
    #         conpany_category,
    #         conpany_status,
    #         conpany_last_update,
    #         company_career_codes,
    #         company_career_names,
    #         url,
    #     ),
    # )
    # conn.commit()


# Lấy thông tin về tỉnh/thành phố
#crawl_data_province(pattern.URL_PATH_BY_PROVINCE, const_headers) 
# Lấy thông tin quận huyện theo URL
#crawl_data_district()



# ========================================================================================== Job
# crawl_data_district_by_url('/tra-cuu-ma-so-thue-theo-tinh/ha-noi-7', const_headers) # Test


# Lấy thông tin ngành nghề

# crawl_data_career(pattern.URL_PATH_BY_CAREER, const_headers)
# =================================================== Job


# Lấy thông tin công ty
crawl_data_company()
# =========================================================================================== Job
# crawl_data_company_by_url('/2100689933-cong-ty-tnhh-mtv-vang-bac-kim-hue', const_headers)
# crawl_data_company_by_url('/2100689059-cong-ty-tnhh-xang-dau-tra-vinh-petro', const_headers)
# crawl_data_company_by_url('/0315739605-001-van-phong-dai-dien-cong-ty-tnhh-chint-vietnam-holding-tai-ha-noi', const_headers)

# if __name__ == "__main__":
# config = load_config()
# headers = {'User-Agent': config['user_agent']}
# proxies = {
#    'http': config['http_proxy'],
#    'https': config['https_proxy']
# }
# url = 'https://example.com'
# crawl_data(url, headers, proxies)
