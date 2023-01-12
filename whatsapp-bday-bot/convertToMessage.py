def convert_result_to_message(result):
    if len(result) == 0:
        return "Sorry, we currently don't have that person in our database. \n Type @help for assistance"
    message = ""
    for data in result:
        message += f"Name: {data['name']}\n"
        message += f"Date Of Birth: {data['DOB']}\n"
        message += '\n\n'
    # message = 'converting'
    return message