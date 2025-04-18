def validate_amount(new_value):
    if new_value == "":
        return True  # Permitir vacío
    try:
        float(new_value)
        return True
    except ValueError:
        return False
