import spelling
from tkinter import *
import tkinter.font as tf
from nltk import sent_tokenize, word_tokenize
import string
spelling.tokenize_file()
spelling.train1()
tk = Tk()
tk.title('test')
tk.geometry('850x850')

tk.resizable(width=False, height=False)

a=0.0
input_L = Label(tk, text='TEXT：')
input_L.grid(row=5, column=1, sticky='E')
input_C =Text(tk,height=20,width=70)
input_C.grid(row=5, column=2,sticky='NW')

output_L=Label(tk,text='Result: ')
output_L.grid(row=8, column=1, sticky='E')
output_C =Text(tk,height=20,width=70)
output_C.grid(row=8, column=2, sticky='NW')
input_C.tag_add('tag',a)
input_C.tag_config('tag',foreground='red')
input_C.tag_add('tag1',a)
input_C.tag_config('tag1',foreground='blue')
def value():
    #print(input_C.get("1.0","end"))
    output_C.delete('1.0','end')
    del_estr = string.punctuation
    replace = " " * len(del_estr)
    sentences = sent_tokenize(text=input_C.get("1.0","end"))
    input_C.delete('1.0', 'end')
    for i in sentences:
        out = i.translate(str.maketrans(del_estr, replace))
        word_list = word_tokenize(out.lower())
        input=word_tokenize(i)
        pos=[]
        for i in range(len(input)):
            pos.append(3)
        '''
        for i in range(len(input)):
            if input[i].lower()=='it':
                #a = str(i + 1) + '.0'
                input_C.insert('2.0', input[i]+' ', 'tag')
            else:
                input_C.insert('2.0', input[i]+' ')
        '''
        #print(word_list)
        output=spelling.real_word_correction(word_list)[0]
        result=output.translate(str.maketrans(del_estr, replace))
        result_list=word_tokenize(result.lower())
        #print(result_list)
        for i in range(len(word_list)):
            if word_list[i].lower()==result_list[i].lower():
                continue
            else:
                for k in range(len(input)):
                    if input[k]==word_list[i]:
                        if spelling.know(word_list[i].lower())==True:
                            pos[k]=1
                        else:
                            pos[k]=0
                a=word_list[i]+'--->'+result_list[i]
                output_C.insert('2.0', a+'\n')
        for i in range(len(input)):
            if pos[i] == 0:
                        # a = str(i + 1) + '.0'
                input_C.insert('2.0', input[i] + ' ', 'tag')
            elif pos[i]==1:
                input_C.insert('2.0', input[i] + ' ', 'tag1')
            else:
                input_C.insert('2.0', input[i] + ' ')
                #output_C.insert('2.0', '\n')

        #output=word_list

    #output_C.grid(row=9, column=2, sticky='NW')
def only_spelling():
    output_C.delete('1.0', 'end')
    sentences = sent_tokenize(text=input_C.get("1.0", "end"))
    input_C.delete('1.0', 'end')
    punkt_list = r",.?\"``” “ '''!()/\\-<>:@#$%^&*~"
    for i in sentences:
        word_list = word_tokenize(i)
        new_list=[]
        for i in range(len(word_list)):
            #print(word_list[i])
            if word_list[i].isdigit():
                new_list.append(word_list[i])
            elif word_list[i] in punkt_list:
                new_list.append(word_list[i])
            else:
                new_list.append(spelling.non_word_correct(word_list[i].lower()))
        for i in range(len(word_list)):
            if word_list[i].isupper()==True:
                new_list[i]=new_list[i].upper()
            elif word_list[i].istitle()==True:
                new_list[i]=new_list[i].title()
        for i in range(len(new_list)):
            if word_list[i] == new_list[i]:
                input_C.insert('2.0', word_list[i] + ' ')
            else:
                input_C.insert('2.0', word_list[i] + ' ', 'tag')
                output_C.insert('2.0',word_list[i]+'--->'+new_list[i]+'\n')
AnNiu = Button(tk, text='Real-word correction', fg='blue', bd=2, width=20, command=value)
AnNiu.grid(row=6, column=2, sticky='NW')
button = Button(tk, text='Non-word correction', fg='blue', bd=2, width=20, command=only_spelling)
button.grid(row=7, column=2, sticky='NW')


tk.mainloop()
