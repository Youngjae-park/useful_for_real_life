import tkinter
import os
from selenium import webdriver
import time
import json


count = 0
### def_start
u_driver = None
present_user_name = None
now = os.getcwd()

json_data = json.load(open(now+'\\Login_Info.json'))

def login():
    global count
    global present_user_name
    global u_driver
    driver = webdriver.Chrome(executable_path=now+"\chromedriver.exe")
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sel_num = id_listbox.curselection()[0]
    temp_id = id_listbox.get(sel_num)
    present_user_name = temp_id
    temp_pw = pw_listbox.get(sel_num)
    label_state.config(text=temp_id + "(으)로 로그인되었습니다.")

    time.sleep(1)
    driver.find_element_by_name('username').send_keys(temp_id)
    driver.find_element_by_name('password').send_keys(temp_pw)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
    count += 1
    u_driver = driver

def logout():
    global u_driver
    link = 'https://www.instagram.com/' + present_user_name
    u_driver.get(link)
    time.sleep(1)
    u_driver.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR > div > button > svg').click()
    time.sleep(1)
    u_driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()

def add_id():
    global json_data
    temp_id = entry_id.get()
    temp_pw = entry_pw.get()
    if temp_id in json_data['Info']:
        label_state.config(text= "이미 존재하는 아이디입니다.")
        return
    id_listbox.insert(id_listbox.size(), temp_id)
    pw_listbox.insert(pw_listbox.size(), temp_pw)
    json_data["Info"][temp_id] = temp_pw
    with open(now+'\\Login_Info.json', 'w') as make_file:
        json.dump(json_data, make_file, indent= "\t")
    label_state.config(text="추가될 ID : "+ str(id_listbox.get(id_listbox.size()-1)))

def delete_id():
    global json_data
    global id_listbox, pw_listbox
    sel_num = id_listbox.curselection()
    label_state.config(text= id_listbox.get(sel_num[0]) + " 이 삭제되었습니다. ")
    temp_id = id_listbox.get(sel_num[0])
    json_data['Info'].pop(temp_id)
    with open(now+'\\Login_Info.json', 'w') as make_file:
        json.dump(json_data, make_file, indent= "\t")
    id_listbox.delete(sel_num[0])
    pw_listbox.delete(sel_num[0])

def show_pw():
    sel_num = id_listbox.curselection()
    label_state.config(text = id_listbox.get(sel_num[0]) + "의 비밀번호는 \"" + pw_listbox.get(sel_num[0]) + "\"입니다")

### def_end

window = tkinter.Tk() # Make basic window
frame = tkinter.Frame(window)
scrollbar = tkinter.Scrollbar(frame)
scrollbar.pack(side ="right", fill = "y")

window.title("Insta_login_Sotong5") # title name
window.geometry("350x400+100+100") # width x height + init_x + init_y
window.resizable(True, True) # add '#' infront of this code, if you wanna be able to change the size of window

label_in_login = tkinter.Label(window, text = "insta_login", width = 400, height=2, relief = "ridge", bd = 2, bg = "gray", padx =1, pady =1)
label_in_login.pack(side = "top")

id_listbox = tkinter.Listbox(frame, selectmode = 'browse', yscrollcommand = scrollbar.set ,height = 15, width = 100)
pw_listbox = tkinter.Listbox(frame)

# with open('C:\\Users\VRPC\\Desktop\영재\소통파이브\\facebook_macro\\test.json') as f:
#     json_data = json.load(f)

for j_info in json_data['Info']:
    id_listbox.insert(id_listbox.size(), j_info)
    pw_listbox.insert(pw_listbox.size(), json_data['Info'][str(j_info)])

# MAKING TEST_SET
# for line in range(1, 11):
#     id_listbox.insert(line, "test" + str(line))
#     pw_listbox.insert(line, "test"+str(line))

id_listbox.pack(side = "top")
scrollbar["command"] = id_listbox.yview
frame.pack()

frame_entry = tkinter.Frame(window)
label_id_entry = tkinter.Label(frame_entry, text = "ID")
label_id_entry.pack(side="left")
entry_id = tkinter.Entry(frame_entry)
entry_id.pack(side = "left")
label_pw_entry = tkinter.Label(frame_entry, text="PW")
label_pw_entry.pack(side = "left")
entry_pw = tkinter.Entry(frame_entry)
entry_pw.pack(side = "left")
frame_entry.pack(side = "top")

frame_button = tkinter.Frame(window)
add_button = tkinter.Button(frame_button, overrelief = 'solid', text="ADD", width = 5, command = add_id, repeatdelay = 1000, repeatinterval = 100)
add_button.pack(side = 'left', ipadx = 10)
delete_button = tkinter.Button(frame_button, overrelief = 'solid', text="DELETE", width = 5, command = delete_id, repeatdelay = 1000, repeatinterval = 100)
delete_button.pack(side = 'left', ipadx = 10)
show_pw_button = tkinter.Button(frame_button, overrelief = 'solid', text="SHOW_PW", width = 5, command = show_pw, repeatdelay = 1000, repeatinterval = 100)
show_pw_button.pack(side = "left", ipadx = 10)
login_button = tkinter.Button(frame_button, overrelief = 'solid', text="LOGIN", width = 5, command = login, repeatdelay = 1000, repeatinterval = 100)
login_button.pack(side = 'left', ipadx = 10)
logout_button = tkinter.Button(frame_button, overrelief = 'solid', text="LOGOUT", width = 5, command = logout, repeatdelay = 1000, repeatinterval = 100)
logout_button.pack(side = 'left', ipadx = 10)
frame_button.pack()

label_present_id = tkinter.Label(window, text = "현재 접속된 ID: ",width = 400, height = 2, relief = "ridge", bd = 2, bg = "gray", padx = 1, pady = 1)
label_present_id.pack(side = "bottom")

label_state = tkinter.Label(window, text = "추가될 ID: ", width = 400, height = 2, relief = "ridge", bd = 2, bg = "gray", padx = 1, pady = 1)
label_state.pack(side = "bottom")

window.mainloop()