import convertible_bond.filehandler as fh

data_median2 = [
    ("日期", "转股溢价率%"),
    ("2012-01-01", 0.02),
    ("2012-01-02", 0.03),
    ("2012-01-03", 0.04),
    ("2012-01-04", 0.05)
]

fh.save_tuple_to_excel("test", data_median2)
