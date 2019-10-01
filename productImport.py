from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


response = webdriver.Chrome()
response.implicitly_wait(20)
response.get("http://lucky-coyote.w6.wpsandbox.pro/wp-admin/post-new.php?post_type=product")
username = "arehman622"
password = "arehman622"
user = response.find_elements_by_xpath("//input[@id='user_login']")
passw = response.find_elements_by_xpath("//input[@id='user_pass']")
login = response.find_elements_by_xpath("//input[@id='wp-submit']")
user[0].send_keys(username)
passw[0].send_keys(password)
login[0].click()
with open("dOuput_Username.csv", errors='ignore') as csvfile:
    readCSV = csv.DictReader(csvfile)
    productType = "simple"
    accData = list(readCSV)
    startFrom = 0   # Start from which row
    i = startFrom
    noOfSkips = 0
    productAdded = 0
    for row in accData[startFrom:]:
        if(noOfSkips!=0):
            noOfSkips -= 1
            i += 1
            continue
        productType = "simple"
        if(accData[i+1]["Title"] == row["Title"]):
            productType = "variation"
        response.get("http://lucky-coyote.w6.wpsandbox.pro/wp-admin/post-new.php?post_type=product")
        title = response.find_elements_by_xpath("//input[@id='title']")
        title[0].send_keys(row["Title"])
        desc = '{}\n<div style="overflow: auto;">\n<table class="shop_attributes">\n<tbody>\n<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n</tbody>\n</table>\n</div>'.format(row["Title"],row["Item Specific Label 2"],row["Item Specific Value 2"],row["Item Specific Label 7"],row["Item Specific Value 7"],row["Item Specific Label 8"],row["Item Specific Value 8"],row["Item Specific Label 3"],row["Item Specific Value 3"],row["Item Specific Label 4"],row["Item Specific Value 4"],row["Item Specific Label 9"],row["Item Specific Value 9"],row["Item Specific Label 5"],row["Item Specific Value 5"],row["Item Specific Label 6"],row["Item Specific Value 6"],row["Item Specific Label 10"],row["Item Specific Value 10"])
        description = response.find_elements_by_xpath("//textarea[@id='content']")
        description[0].send_keys(desc)
        vendor = Select(response.find_element_by_xpath("//select[@id='dokan_product_author_override']"))
        vendor.select_by_visible_text(row["user"])
        response.implicitly_wait(0)
        categoryStr = row["Category Name"]
        success = 0
        while(success == 0 and categoryStr):
            try:
                category ="//label[contains(text(),'{}')]".format(categoryStr)
                response.find_elements_by_xpath(category)[0].click()
                success = 1
            except:
                categoryStr = categoryStr[:-1]
                success = 0
        response.implicitly_wait(20)
        img1 = response.find_elements_by_xpath("//input[@id='knawatfibu_url']")
        img1[0].send_keys(row["Image 1"])
        response.find_elements_by_xpath("//a[@id='knawatfibu_preview']")[0].click()
        response.implicitly_wait(0)
        mustWait = WebDriverWait(response,10).until(EC.presence_of_element_located((By.XPATH,"//img[@id='knawatfibu_img' and contains(@style,'display: inline')]")))
        response.implicitly_wait(20)
        j=2
        idx = 0
        while(row["Image {}".format(j)] and j<101):
            if(j==3):
                idx = j
                imgpath = "//input[@id='knawatfibu_url{}']".format(idx)
            else:
                idx = idx+1
                imgpath = "//input[@id='knawatfibu_url{}']".format(idx)
            response.find_elements_by_xpath(imgpath)[0].send_keys(row["Image {}".format(j)])
            prevPath = "//a[@id='knawatfibu_preview{}']".format(idx)
            response.find_elements_by_xpath(prevPath)[0].click()
            j+=1
        if(productType == "simple"):
            price = response.find_elements_by_xpath("//input[@id='_regular_price']")
            price[0].send_keys(row["Price"].lstrip("$€£"))
        elif (productType == "variation"):
            prodType = Select(response.find_element_by_xpath("//select[@id='product-type']"))
            prodType.select_by_value("variable")
            response.find_element_by_xpath("//a[@href='#product_attributes']").click()
            attrAdded = 0
            k=1
            while(row["Dropdown Name {}".format(k)]):
                success = 0
                while(success == 0):
                    try:
                        response.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/button[1]")[0].click()
                        success = 1
                    except:
                        response.implicitly_wait(0)
                        weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/button[1]")))
                        response.implicitly_wait(20)
                        success = 0
                k += 1
            k=1
            while(row["Dropdown Name {}".format(k)]):
                success = 0
                while(success == 0):
                    try:
                        dropDownName = response.find_elements_by_xpath("//input[@name='attribute_names[{}]']".format(attrAdded))
                        dropDownName[0].send_keys(row["Dropdown Name {}".format(k)])
                        success = 1
                    except:
                        response.implicitly_wait(0)
                        weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='attribute_names[{}]']".format(attrAdded))))
                        response.implicitly_wait(20)
                        success = 0
                options = ""
                totalrows = 0
                l = i
                while(accData[l]["Title"] == row["Title"]):
                    options = options + "|" + accData[l]["Dropdown Option {}".format(k)]
                    l += 1
                    totalrows += 1
                success = 0
                while(success == 0):
                    try:
                        choices = response.find_elements_by_xpath("//textarea[@name='attribute_values[{}]']".format(attrAdded))
                        choices[0].send_keys(options)
                        success = 1
                    except:
                        response.implicitly_wait(0)
                        weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='attribute_values[{}]']".format(attrAdded))))
                        response.implicitly_wait(20)
                        success = 0
                success = 0
                while(success == 0):
                    try:
                        response.find_element_by_xpath("//input[@name='attribute_variation[{}]']".format(attrAdded)).click()
                        success = 1
                    except:
                        response.implicitly_wait(0)
                        weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='attribute_variation[{}]']".format(attrAdded))))
                        response.implicitly_wait(20)
                        success = 0
                attrAdded += 1
                k += 1
            success = 0
            while(success == 0):
                try:
                    response.find_element_by_xpath("//button[@class='button save_attributes button-primary']").click()
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button save_attributes button-primary']")))
                    response.implicitly_wait(20)
                    success = 0
            success = 0
            while(success == 0):
                try:
                    response.find_elements_by_xpath("//li[@class='variations_options variations_tab variations_tab show_if_variable']//a")[0].click()
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='variations_options variations_tab variations_tab show_if_variable']//a")))
                    response.implicitly_wait(20)
                    success = 0
            success = 0
            while(success == 0):
                try:
                    variant = Select(response.find_element_by_xpath("//select[@id='field_to_edit']"))
                    variant.select_by_value("link_all_variations")
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='field_to_edit']")))
                    response.implicitly_wait(20)
                    success = 0
            success = 0
            while(success == 0):
                try:
                    response.find_element_by_xpath("//a[@class='button bulk_edit do_variation_action']").click()
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button bulk_edit do_variation_action']")))
                    response.implicitly_wait(20)
                    success = 0
            alert = response.switch_to.alert
            alert.accept()
            success = 0
            while(success == 0):
                try:
                    alert = response.switch_to.alert
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 60).until(EC.alert_is_present())
                    response.implicitly_wait(20)
                    success = 0
            alert.accept()
            expands = response.find_elements_by_xpath("//strong[contains(text(),'#')]")
            success = 0
            while(success == 0):
                try:
                    expands[0].click()
                    success = 1
                except:
                    success = 0
            for xpnd in expands[1:]:
                time.sleep(0.5)
                xpnd.click()
            line = 1
            count1 = 0
            for x in range(totalrows):
                if(count1 == 15):
                    count1 = 0
                if(line == 16):
                    line = 1
                    success = 0
                    while(success == 0):
                        try:
                            response.find_element_by_xpath("//div[@id='variable_product_options_inner']//div[@class='toolbar']").click()
                            response.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[4]/button[1]").click()
                            success = 1
                        except:
                            response.implicitly_wait(0)
                            weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[4]/button[1]")))
                            response.implicitly_wait(20)
                            success = 0
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='button-primary save-variation-changes' and @disabled]")))
                    response.implicitly_wait(20)
                    success = 0
                    time.sleep(3)
                    while(success == 0):
                        try:
                            response.find_element_by_xpath("//div[@class='toolbar']//a[@class='next-page']").click()
                            success = 1
                        except:
                            response.implicitly_wait(0)
                            weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='toolbar']//a[@class='next-page']")))
                            response.implicitly_wait(20)
                            success = 0
                    success = 0
                    while(success == 0):
                        try:
                            response.find_element_by_xpath("//div[@id='variable_product_options_inner']//div[@class='toolbar']").click()
                            success = 1
                        except:
                            response.implicitly_wait(0)
                            weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='variable_product_options_inner']//div[@class='toolbar']")))
                            response.implicitly_wait(20)
                            success = 0
                    time.sleep(4)
                    response.execute_script("window.scrollTo(0, 0)") 
                    expands = response.find_elements_by_xpath("//strong[contains(text(),'#')]")
                    success = 0
                    while(success == 0):
                        try:
                            expands[0].click()
                            success = 1
                        except:
                            success = 0
                    for xpnd in expands[1:]:
                        time.sleep(0.5)
                        xpnd.click()
                success = 0
                while(success == 0):
                    try:
                        regPrice = response.find_element_by_xpath("//input[@id='variable_regular_price_{}']".format(count1))
                        regPrice.send_keys(accData[i+x]["Price"])
                        success = 1
                    except:
                        response.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[3]/div[{}]/h3[1]/strong[1]".format(line+1)).click()
                        response.implicitly_wait(0)
                        weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='variable_regular_price_{}']".format(count1))))
                        response.implicitly_wait(20)
                        success = 0
                line += 1
                count1 += 1
            success = 0
            while(success == 0):
                try:
                    response.find_element_by_xpath("//div[@id='variable_product_options_inner']//div[@class='toolbar']").click()
                    response.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[4]/button[1]").click()
                    success = 1
                except:
                    response.implicitly_wait(0)
                    weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[4]/button[1]")))
                    response.implicitly_wait(20)
                    success = 0
            response.implicitly_wait(0)
            weWait = WebDriverWait(response, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='button-primary save-variation-changes' and @disabled]")))
            response.implicitly_wait(20)
            noOfSkips = totalrows - 1
        success = 0
        response.execute_script("window.scrollTo(0, 0)") 
        while(success == 0):
            try:
                response.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/input[2]").click()
                success = 1
            except:
                response.implicitly_wait(0)
                weWait = WebDriverWait(response, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[5]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/input[2]")))
                response.implicitly_wait(20)
                success = 0    
        productAdded += 1
        print("product(s) added: "+ str(productAdded))
        i+=1