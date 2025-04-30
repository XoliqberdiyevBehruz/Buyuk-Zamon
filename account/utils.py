def get_course_price(payment_type, tariff):
    if tariff == 'premium':
        if payment_type == 'naqd' or payment_type == 'karta':
            return 17_900_000
        elif payment_type == 'nasya':
            return 18_900_000
    if tariff == 'vip':
        if payment_type == 'naqd' or payment_type == 'karta':
            return 25_900_000
        elif payment_type == 'nasya':
            return 26_900_000
    if payment_type == 'naqd' or payment_type == 'karta' or payment_type == 'nasya' and tariff == 'biznes':
        return 100_000_000
    else:
        return None