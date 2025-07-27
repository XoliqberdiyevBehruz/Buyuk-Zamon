def format_text(text, student):
    student_data = {
        "NAME": student.full_name,
        "PAID": student.paid,
        "DEBT": student.debt,
        "CONTRACT_NUMBER": student.contract_number, 
        "PHONE": student.phone_number,
        "STUDENT_ID_DATE": student.student_id_time,
        "STUDENT_ID": student.student_id,
        "COURSE_PRICE": student.course_price,
        "TARIFF": student.tariff,
        "STATUS": student.status,
        "TYPE": student.type,
        "TG_ID": student.telegram_id,
        "TG_USERNAME": student.telegram_username,
        "TG_NAME": student.telegram_full_name
    }

    for key, value in student_data.items():
        if key in text:
            text = text.replace(key, str(value))
    return text