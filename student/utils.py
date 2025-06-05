def format_text(text, student):
    student_data = {
        "NAME": student.full_name,
        "PAID": student.paid,
        "DEBT": student.debt,
        "CONTRACT_NUMBER": student.contract_number
    }

    for key, value in student_data.items():
        if key in text:
            text = text.replace(key, str(value))
    return text