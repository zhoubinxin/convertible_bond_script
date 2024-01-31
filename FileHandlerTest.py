import convertible_bond.FileHandler as fh

excel_name = "转股溢价率中位数"

data_median = {
    "日期": ["2012-01-01", "2012-01-02", "2012-01-03", "2012-01-04", ],
    "转股溢价率%": [0.02, 0.03, 0.04, 0.05]
}

fh.save_to_excel(excel_name, data_median)

json_name = "test"

data = ["128022.SZ",
        "128012.SZ",
        "110034.SH",
        "128017.SZ",
        "113009.SH",
        "123002.SZ",
        "113012.SH",
        "113010.SH",
        "110033.SH",
        "110030.SH",
        "128021.SZ",
        "128025.SZ"]

key = "testkey"

fh.save_json_data(json_name, data, key)
json_data = fh.get_json_data(json_name, key)

print(json_data)
