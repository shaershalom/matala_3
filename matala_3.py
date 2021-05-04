import re
import json

with open("WhatsApp.txt", 'r' , encoding='utf-8') as file:
    text =file.readlines()
    file.close()

# פונקציה שתפקידה ליצור זהות חסויה לכל אדם 
def Confidential_identity_generator(text):
    list_identity=list()
    dict_identity=list()
    id_num=0
    for line in text[5:]:
        identity=line[line.find("-"):line.find(":",line.find("-"))]
        list_identity.append(identity)
    list_identity = list(dict.fromkeys(list_identity))

    for identity in list_identity:
        id_num =id_num + 1 
        if identity != "": 
            id_identity={"id": id_num , "identity" : identity }  
            dict_identity.append(id_identity)
    
    return dict_identity

# פונקציה שתפקידה הצפנת הודעות
def encryption_message(text): 
    dict_Confidential= Confidential_identity_generator(text)
    encryption_message=list()
    for line in text[5:]:
        time = line[:line.find("-")]
        identity=line[line.find("-"):line.find(":",line.find("-"))]
        test_text=line[line.find(":",line.find("-")):].strip()
        dict1={"datetime": time  , "id" : identity, "text" : test_text}
        encryption_message.append(dict1)
    
    for message in encryption_message:
        for identity in dict_Confidential:
            if message["id"] == identity["identity"]:
                message["id"]=identity["id"]
        
    return encryption_message


# פונקציה שתפקידה ליצור metadata
def generator_metadata(text):
    dict_identity=Confidential_identity_generator(text)
    metadata=dict()
    str_metadata = text[1]
    
    chat_name= re.search('"(.*)"', str_metadata).group(1)
    creation_date = str_metadata[:str_metadata.find("-")] 
    num_of_participants = len(dict_identity)
    creator =re.search('נוצרה על ידי(.*)', str_metadata).group(1)

    metadata ={"chat_name": chat_name , "creation_date": creation_date, "num_of_participants": num_of_participants, "creator": creator}

    return metadata

# פונקציה שתפקידה  לבצע את שלב 4 ושלב 5 
def Step_four_and_fifth(text):
    Step_four=dict()
    metadata=generator_metadata(text)
    encryption_all_message=encryption_message(text)
    Step_four={"messages": encryption_all_message , "metadata": metadata } 
    file_json = json.dumps(Step_four , ensure_ascii=False)
    
    # כתיבה לקובץ חיצוני    
    with open(f"{metadata['chat_name']}.txt", 'w' , encoding='utf-8') as file_end:
        file_end.write(file_json)
        file.close()
    
    return file_json


# ניתן להריץ כל פונקציה בנפרד על מנת לראות את התוצאות של כל שלב 
# הרצה סופית 
print(Step_four_and_fifth(text))    
        
        
    
    

