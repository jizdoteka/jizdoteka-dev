from django import forms
from random import randint


class RegisterForm(forms.Form):

    def rand_anti_question():
        day_list = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]

        rand_day_num = randint(0, len(day_list))
        rand_addition = randint(0, len(day_list))
        correct_day_num = rand_day_num + rand_addition
        correct_day_index = correct_day_num

        if correct_day_index >= len(day_list):
            correct_day_index = correct_day_index - len(day_list)

        print (len(day_list))
        print (correct_day_index)

        question = "Dnes je %s. V případě, že je toto tvrzení pravdivé, co bude za %s dny?" % (day_list[rand_day_num], rand_addition)
        return (question, day_list[correct_day_index])

    user_email = forms.CharField(max_length = 100, label = "Vaše emailová adresa")
    user_email_confirm = forms.CharField(max_length = 100, label = "Vaše emailová adresa - kontrola")
    user_password = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo")
    user_password_confirm = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo - kontrola")

    cont_question, correct_day = rand_anti_question()
    random_antibot = forms.CharField(max_length = 50, label = cont_question)

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length = 100, label = "Váš email")
    user_pass = forms.CharField(widget = forms.PasswordInput(), label = "Vaše heslo")

class ManageForm(forms.Form):
    user_mail = forms.EmailField(max_length = 100, label = "Váš email")
    user_mail_confirm = forms.EmailField(max_length = 100, label = "Váš email - kontrola")
    user_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput(), label = "Vaše heslo")
    user_pass_confirm = forms.EmailField(max_length = 100, widget = forms.PasswordInput(), label = "Vaše heslo - kontrola")

class CarManageForm(forms.Form):
    pass
