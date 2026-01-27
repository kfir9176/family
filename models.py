import flet as ft

class Person:
    def __init__(self, name, family="", age="לא ידוע", phone="לא ידוע", address="לא ידוע", birthday="לא ידוע", has_family_id=None):
        self.name = name
        self.family = family
        self.age = age
        self.phone = phone
        self.address = address
        self.birthday = birthday
        self.has_family_id = has_family_id
        self.type = "person" # סימון פנימי שזה אדם

class UIItem:
    def __init__(self, type, title):
        self.type = type # "main_title" או "header"
        self.title = title