class Tresh_filter:
    def __init__(self, threshold_high, threshold_low):
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
    def update(self, value_init, new_value):
        if new_value>self.treshold_low and new_value<self.treshold_high :
            return new_value
        else :
            return value_init