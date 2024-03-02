class Bond(object):
    def __init__(self, name, cusip, face_value, coupon_rate, maturity):
        self.name = name
        self.cusip = cusip
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity = maturity

    def __repr__(self):
        return f"Bond({self.name}, {self.cusip}, {self.face_value}, {self.coupon_rate}, {self.maturity})"
