

def remove_duplicates(item_list, attribute):
    seen_values = []
    unique_items = []
    for item in item_list:
        value = getattr(item, attribute)
        if value not in seen_values:
            seen_values.append(value)
            unique_items.append(item)
    return unique_items
