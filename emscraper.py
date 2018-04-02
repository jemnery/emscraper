import os
from lxml import html
import requests
from self_email import send_self_email

def is_in_stock(tree):
    in_stock = False
    buy_btn_id = "ctl00_FeaturedContent_LinkButton1" # <a> element    
    buy_btn = tree.xpath("//a[@id = '%s']" % buy_btn_id)    

    if not buy_btn:
        out_of_stock_btn_id = "ctl00_FeaturedContent_LinkButton11" # <a> element
        out_of_stock_btn = tree.xpath("//a[@id = '%s']" % out_of_stock_btn_id)
        if not out_of_stock_btn:
            raise Exception("Neither button found")            
    else:
        in_stock = True 

    return in_stock

def get_product_urls():
    product_list = []
    
    # generally im stock:
    #product_list.append("uss-thunderchild-ncc-63549-model")
    #product_list.append("klingon-bird-of-prey-model")
    #product_list.append("klingon-ktinga-class-battlecruiser-model")

    # 404 test:
    # product_list.append("uss-enterprise-ncc-1701-starship-invalid")

    product_list.append("uss-enterprise-ncc--1701-2271-model")
    product_list.append("uss-enterprise-ncc-1701-e-starship-model")
    product_list.append("uss-enterprise-ncc-1701-d-model")
    product_list.append("enterprise-nx-01-model-ship")
    product_list.append("uss-enterprise-ncc-1701-starship")

    root_url = "https://shop.eaglemoss.com/star-trek-official-starship-collection/"
    url_dict = {}
    for product in product_list:
        url_dict[product] = root_url + product
    return url_dict
    
def get_anchor_html(name, url, status):
    a = '<a href="' + url + '">' + name + ' -' + status + '</a>'
    return a

def scan_local_files():
    with os.scandir("./html") as filesInDir:  
            for entry in filesInDir:
                # print all entries that are files
                if entry.is_file():
                    ext = os.path.splitext(entry.name)[-1].lower()
                    if (ext == ".html"):
                        print("Processing local HTML file:" + entry.name)
                        with open(entry.path, "r") as f:
                            page = f.read()
                            tree = html.fromstring(page)

def main():
    url_list = get_product_urls()
    anchors = []
    in_stock_count = 0
    not_in_stock_count = 0
    not_found_count = 0

    for k, v, in url_list.items():
        print("Processing product page: " + k)
        a = ""
        page = requests.get(v)

        if (page.status_code == 200):  # OK
            tree = html.fromstring(page.content)

            if tree is not None:
                in_stock = is_in_stock(tree)
                if in_stock:
                    in_stock_count += 1
                    status = '<strong>IN STOCK!</strong>'
                else:
                    not_in_stock_count += 1
                    status = 'not in stock'
        else:
            not_found_count += 1
            status = str(page.status_code) + " " + page.reason
                
        a = get_anchor_html(k, v, status)
        anchors.append(a)

    email_body = '<h3>Summary</h3><p>In stock: ' + str(in_stock_count) + '; not in stock: ' + str(not_in_stock_count) + '</p>'
    email_body += '<h3>Products</h3><p>'
    for anchor in anchors:
        email_body += anchor + '<br /><br />'
    email_body += '</p>'

    email_subject = 'Eaglemoss auto stock check (' + str(in_stock_count) + ' in stock)'
    send_self_email(email_subject, email_body)

if __name__ == "__main__":
    main()