import g4f

def chatbot(zapros, napravleniya):
    if napravleniya == "медицина":
        prompt = f"{zapros} - связано с медициной. Ответ на эту {zapros} по точке зрения медицине"
    elif napravleniya == "IT":
        prompt = f"{zapros} - связано с IT. Ответ на эту {zapros} по точке зрения IT"
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": prompt}],
    )

    return response
