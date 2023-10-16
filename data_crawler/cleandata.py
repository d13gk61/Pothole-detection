# read file csv
with open('data_crawler/data/products.csv', 'r') as file:
    lines = file.readlines()

# create a new file and remove //live.
with open('data_crawler/data/newproducts.csv', 'w') as new_file:
    for line in lines:
        url = line.strip()  # Loại bỏ khoảng trắng và ký tự xuống dòng từ mỗi URL
        new_url = url.replace("lazy,//", "")  # remove "lazy,//"
        new_file.write(new_url + '\n')  # rewrite to new file

print("done")

