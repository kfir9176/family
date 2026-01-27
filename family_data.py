from models import Person, UIItem

# הגדרת מאגר הנתונים של המשפחות
families = {
    # משפחת גדסי
    "gadasi_parents": [
        UIItem("main_title", "משפחת גדסי"),
        UIItem("header", "הורים:"),
        Person(name="שמשון", family="גדסי"),
        Person(name="מזל", family="גדסי"),
        UIItem("header", "ילדים:"),
        Person(name="אופיר", family="גדסי"),
        Person(name="אפרת", family="ג'מיל", has_family_id="jamil_parents"),
        Person(name="אסנת", family="בחור", has_family_id="bahur_parents"),
        Person(name="אמיתי", family="גדסי")
    ],

    # משפחת ג'מיל (הבת של גדסי)
    "jamil_parents": [
        UIItem("main_title", "משפחת ג'מיל"),
        UIItem("header", "הורים:"),
        Person(name="יוסף", family="ג'מיל"),
        Person(name="אפרת", family="ג'מיל"),
        UIItem("header", "ילדים:"),
        Person(name="נריה", family="ג'מיל", has_family_id="neria_jamil"),
        Person(name="טוהר", family="צדוק", has_family_id="tohar_zadok"),
        Person(name="איילת חן", family="ג'מיל"),
        Person(name="חננאל", family="ג'מיל"),
        Person(name="דוד יוחאי", family="ג'מיל")
    ],

    # משפחת נריה (הבן של ג'מיל)
    "neria_jamil": [
        UIItem("main_title", "משפחת נריה ויהל"),
        UIItem("header", "הורים:"),
        Person(name="נריה", family="ג'מיל"),
        Person(name="יהל", family="ג'מיל"),
        UIItem("header", "ילדים:"),
        Person(name="משה", family="ג'מיל")
    ],

    # משפחת צדוק (הבת של ג'מיל)
    "tohar_zadok": [
        UIItem("main_title", "משפחת צדוק"),
        UIItem("header", "הורים:"),
        Person(name="נתנאל", family="צדוק"),
        Person(name="טוהר", family="צדוק"),
        UIItem("header", "ילדים:"),
        Person(name="בת", family="צדוק"),
        Person(name="יוסף", family="צדוק")
    ],

    # משפחת בחור (הבת של גדסי)
    "bahur_parents": [
        UIItem("main_title", "משפחת בחור"),
        UIItem("header", "הורים:"),
        Person(name="איתן", family="בחור"),
        Person(name="אסנת", family="בחור"),
        UIItem("header", "ילדים:"),
        Person(name="אוריה", family="בוזגלו", has_family_id="oria_buzaglo"),
        Person(name="אריאל", family="בחור"),
        Person(name="טליה", family="בחור"),
        Person(name="שירה", family="בחור"),
        Person(name="עמיחי", family="בחור"),
        Person(name="עדי", family="בחור"),
        Person(name="אלרואי דוד", family="בחור")
    ],

    # משפחת בוזגלו (הבת של בחור)
    "oria_buzaglo": [
        UIItem("main_title", "משפחת בוזגלו"),
        UIItem("header", "הורים:"),
        Person(name="רונאל", family="בוזגלו"),
        Person(name="אוריה", family="בוזגלו"),
        UIItem("header", "ילדים:")
    ]
}

# --- יצירת רשימת "כל המשפחה" הממוינת ---
all_members = []
seen_names = set()

for family_list in families.values():
    for item in family_list:
        # בודקים אם זה אדם (ולא כותרת) ואם השם עוד לא הופיע
        if isinstance(item, Person):
            full_name = f"{item.name} {item.family}"
            if full_name not in seen_names:
                all_members.append(item)
                seen_names.add(full_name)

# הוספת רשימת ה"כל" למילון המשפחות
families["all"] = [UIItem("main_title", "כולם (א-ב)")] + sorted(all_members, key=lambda x: x.name)