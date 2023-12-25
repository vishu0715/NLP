import tkinter as tk
import random
import pickle
from tkinter import scrolledtext
from tkinter import simpledialog, messagebox
from Classification_folder.classification_code import *

def classify_text(model,no_to_label,vectorizer):
    # output_text.delete('1.0', 'end')  # Clear previous output
    input_text = input_text_area.get('1.0', 'end-1c')  # Retrieve text from input area
    doc,user_text_final,predicted_label=classification(input_text,model,no_to_label,vectorizer)
    # print(predicted_label)

    #getting disease to specialization file
    f=open(r'C:\Users\vishwak\Desktop\NLP_TEXT_CLASSIFICATION_PROJECT\Data files\Disease_DB.pkl','rb')
    dis_to_spec=pickle.load(f)
    f.close()
    #file handling done

    person=''
    for i in doc.ents:
        if(i.label_=='PERSON'):
            person=i.text
            break
    time=time_finder(user_text_final)
    if time in [None,'NV']:
        messagebox.showinfo("Error","Time entered is not present or not valid, so assigning random time.")
        time= random.randint(9,21)*100
    if(len(person)>0): 
        confirmation_window(predicted_label,time,dis_to_spec[predicted_label],person)
    else:
        confirmation_window(predicted_label,time,dis_to_spec[predicted_label])
    # confirmation_window()

""" def open_about_us_window():
    about_us_window = tk.Toplevel(root)
    about_us_window.title("About Us")
    about_us_label = tk.Label(about_us_window, text="Your text classification tool.", font=("Arial", 12))
    about_us_label.pack() """

""" def open_about_us_window():
    about_us_window = tk.Toplevel()
    about_us_window.title("About Us")
    about_us_window.attributes("-zoomed", True)
    about_us_window.configure(bg='#A7D9F5')

    about_us_label = tk.Label(about_us_window, text="Your Text Classification Tool", font=("Arial", 18), bg='#A7D9F5')
    about_us_label.pack(pady=50)

    about_us_info = tk.Label(about_us_window, text="This tool is designed to perform text classification tasks.", font=("Arial", 14), bg='#A7D9F5')
    about_us_info.pack()

    about_us_window.mainloop() """

def confirmation_window(disease,time,spec,name='Anonymous'):
    # Create a popup window for user confirmation
    msg='''Details are:
    Name: {0}
    Time: {1} hours
    Specialization: {2}
    Do you want to proceed with appointment booking?'''.format(name.capitalize(),time,spec)
    confirmed = messagebox.askyesno("Confirmation", msg)
    if confirmed:
        appointment_booking(time,spec,name)
    else:
        # Navigate back to the input window
        input_text_area.delete('1.0', 'end')
        # output_text.delete('1.0', 'end')

def booking(time,spec):
    f=open(r'C:\Users\vishwak\Desktop\NLP_TEXT_CLASSIFICATION_PROJECT\Data files\Disease_DB.pkl','rb')
    dis_to_spec=pickle.load(f)
    spec_doc=pickle.load(f)
    doc_avail=pickle.load(f)
    f.close()

    doc_id=''
    for i in spec_doc[spec]:
        avail=list(doc_avail[i])
        if(avail.count(time)==0):
            doc_id=i
            avail.append(time)
            doc_avail[i]=avail
            break 
    else:
        return [False] #no slot
    
    f=open(r'C:\Users\vishwak\Desktop\NLP_TEXT_CLASSIFICATION_PROJECT\Data files\Disease_DB.pkl','wb')
    pickle.dump(dis_to_spec,f)
    pickle.dump(spec_doc,f)
    pickle.dump(doc_avail,f)
    f.close()

    return [True,doc_id,spec_doc[spec][doc_id]]

def display_receipt(time,name,spec,doc_id,doc_name):
    print(time,name,spec,doc_id,doc_name)
    receipt_window = tk.Toplevel()
    receipt_window.title("Booking Receipt")
    receipt_window.state('zoomed')

    canvas = tk.Canvas(receipt_window, bg="white", width=800, height=800)
    # canvas.config(state='normal')
    canvas.pack()

    # Draw a rectangle for the receipt outline
    canvas.create_rectangle(50, 50, 700, 700, outline="black")
    
    # Insert the receipt details
    canvas.create_text(350, 30, text="*****------Booking Receipt------*****", font=("Arial", 25),anchor='center',fill='red')
    canvas.create_text(100, 80, text=f"Patient Name: {name.capitalize()}",font=("Arial", 20), anchor="w")
    canvas.create_text(100, 120, text=f"Appointment Time: {time} hours", font=("Arial", 20),anchor="w")
    canvas.create_text(100, 160, text=f"Doctor's Specialization: {spec}",font=("Arial", 20), anchor="w")
    canvas.create_text(100, 200, text=f"Doctor ID: {doc_id}", font=("Arial", 20),anchor="w")
    canvas.create_text(100, 240, text=f"Doctor Name: {doc_name}", font=("Arial", 20),anchor="w")
    canvas.create_text(350, 380, text="Thank you for booking!", font=("Arial", 25),anchor='center')

def appointment_booking(time,spec,name):
    booking_op=booking(time,spec)
    if (booking_op[0]):
        display_receipt(time,name,spec,booking_op[1],booking_op[2])
    else:
        msg='''No slots available at the specified time.
Try again with a different time or try again tomorrow.
Sorry for the inconvinience caused!'''
        messagebox.showinfo("Booking Failed.",msg)
    # Add details of the appointment in this window



# Create main window
model,no_to_label,vectorizer,report_dict= modelTrain()
root = tk.Tk()
root.title("Text Classification")
root.geometry("300x300")
root.state('zoomed')  # Maximize the window
root.configure(borderwidth=5)
label = tk.Label(root, text="Welcome to ABC Hospital Appointment Booking System", font=("Arial", 40))
label.pack(pady=20)


# Create input label
input_label = tk.Label(root, text="Enter Text(please keep time in HH:MM am/pm format):", font=("Arial", 20))
input_label.pack()

# Create input text area
input_text_area = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD,font=("Arial", 15))
input_text_area.pack(padx=10, pady=10)

""" # Create output label
output_label = tk.Label(root, text="Classification Result:", font=("Arial", 12))
output_label.pack()

# Create output text area
output_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
output_text.pack(padx=10, pady=10) """

# Create classify button
classify_button = tk.Button(root, text="Submit", command=lambda: classify_text(model=model, no_to_label=no_to_label, vectorizer=vectorizer),font=("Arial", 15))
classify_button.pack(pady=10)

""" # Create About Us button
about_us_button = tk.Button(root, text="About Us", command=open_about_us_window,font=("Arial", 15))
about_us_button.pack(pady=10) """

# Run the application
root.mainloop()