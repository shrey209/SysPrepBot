from pypdf import PdfReader
import os
from dataclasses import dataclass

@dataclass
class UserState:
    current_page: int
    current_book: int 

chat_map = {}

def initUser(chatid):
    chat_map[chatid] = UserState(0, 0)  

def getfile(no):
    folder_path = "./papers"
    files = sorted(os.listdir(folder_path))  
    if no >= len(files):
        raise IndexError("No more books available.")  
    return os.path.join(folder_path, files[no])  

def read_page(chatid):
    user = chat_map.get(chatid)
    
    if user is None:
        raise ValueError("User not initialized. Call initUser(chatid) first.")

    try:
        book_path = getfile(user.current_book)
    except IndexError:
        return "No more books available."

    reader = PdfReader(book_path)
    num_pages = len(reader.pages)

    page = user.current_page + 1  

   
    if page >= num_pages:
        try:
            book_path = getfile(user.current_book + 1)
        except IndexError:
            return "No more books available."
        
        page = 0  
        user.current_book += 1  

    
    user.current_page = page
    chat_map[chatid] = user

   
    return reader.pages[page].extract_text()


