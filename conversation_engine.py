import random

def imporve_reply(user_input, reply):

    text=user_input.lower()

    if any(word in text for word in [
        "wie gehts",
        "hallo",
        "hi",
        "na"
    ]):
        return reply + "\n\nUnd wie geht es dir ?"
    
    if any(word in text for word in [
            "ich habe",
            "ich bin",
            "ich arbeite",
            "ich mache",
            "ich programmiere"
        ]):

            question=[
                 "Magst du mir mehr davon erzählen ?"
                 "Wie ist es dazu gekommen ?"
                 "Wie läuft es bisher ?"
                 "Was ist dabei die größte Herausforderung ?"
                 "Und wie fühlst du dich damit ?"
            ]

            return reply + "\n\n" + random.choice(question)

    return reply
