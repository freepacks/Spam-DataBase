from django.shortcuts import render
from api.forms import Mail
from django.contrib import messages
import pickle
import numpy as np
import re


def MailTransf(email):
    freq_words = ['make', 'address', 'all', '3d', 'our', 'over', 'remove', 'internet', 'order', 'mail', 'receive', 'will', 'people', 'report', 'addresses', 'free', 'business', 'email', 'you', 'credit', 'your', 'font', '000', 'money', 'hp', 'hpl', 'george', '650', 'lab', 'labs', 'telnet', '857', 'data', '415', '85', 'technology', '1999', 'parts', 'pm', 'direct', 'cs', 'meeting', 'original', 'project', 're', 'edu', 'table', 'conference']
    freq_caract = [';', '(', '[', '!', '$', '#']
    freq_w_list = [ 100*email.split(" ").count(x)/len(email.split(" ")) for x in freq_words]
    freq_c_list = [ 100*email.count(x)/len(email) for x in freq_caract]
    lengt_Capital = [len(x) for x in re.findall("[A-Z]+", email)]
    
    freq_w_list.extend(freq_c_list)
    freq_w_list.extend([np.mean(lengt_Capital), np.max(lengt_Capital), np.sum(lengt_Capital)])

    return [freq_w_list]


def index(request):
    if request.method == 'POST':
        form = Mail(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            filename = "api/finalized_model.sav"
            loaded_model = pickle.load(open(filename, 'rb'))
            resultat = loaded_model.predict(MailTransf(mail))
            if resultat == [0]:
                message_final = "It's not a spam"
                #message_final = '<p style="color:red;">A red paragraph.</p>'
            else:
                message_final = "Becarefull there is a high chance this mail is a spam"
            messages.success(request,message_final)
    else:
        form = Mail()
    return render(request, 'index.html',{"mail":form})