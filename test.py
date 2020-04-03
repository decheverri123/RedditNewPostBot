import re


s = "[USA-NE] [H] cash VGA GTX 770 2GB, Various LGA1151 Intel CPUs [W] PayPal"


start = s.find("[H]")
end = s.find("[W]")
target = s[start:end].lower()

print('paypal' in target or 'cash' in target)
