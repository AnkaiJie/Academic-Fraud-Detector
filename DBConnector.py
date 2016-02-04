'''
Created on Feb 3, 2016

@author: Ankai
'''

import mysql.connector
from academicThings import AcademicPublisher
from academicThings import Paper

class AuthorDbController:
        
    # author is an AcademicPublisher Object
    def insert(self, author):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        data_author = (author.getFirstName(), author.getLastName())
        add_author = ("INSERT INTO authors "
               "(first_name, last_name) VALUES (%s, %s)")
        cursor.execute(add_author, data_author)
        
        conn.commit()
        cursor.close()
        conn.close()
        
    def delete(self, author):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        data_author = (author.getFirstName(), author.getLastName())
        delete_author = ( "DELETE FROM authors WHERE first_name= %s and last_name = %s")
        cursor.execute(delete_author, data_author)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    
    ''' testing not complete'''
    def connectPaperList(self, author, paper_list):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        data_author = (author.getFirstName(), author.getLastName())
        cursor.execute('SELECT id FROM authors WHERE first_name= %s and last_name = %s;',data_author )
        author_id = cursor.fetchone()[0]
        
        for paper in paper_list:
            title = paper.getInfo()['Title']
            date = paper.getInfo()['Publication date']
            year = date[:4]
            
            data_paper = (year, title)
            
            cursor.execute('SELECT id FROM papers WHERE year= %s and title = %s;',data_paper)
            paper_id = cursor.fetchone()[0]
            print(paper_id)
            print (author_id)
        
            data = (author_id, paper_id)
        
            #print('INSERT INTO paper_authors (author_id, paper_id) VALUES (%s, %s);', data)
        
            cursor.execute('INSERT INTO paper_authors (author_id, paper_id) VALUES (%s, %s);', data)
        
        conn.commit()
        cursor.close()
        conn.close()
   

class PaperDbController:
        
    # author is an AcademicPublisher Object
    def insert(self, paper):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        title = paper.getInfo()['Title']
        date = paper.getInfo()['Publication date']
        year = date[:4]
        data_paper = (year, title)
        add_paper = ("INSERT INTO papers "
               "(year, title) VALUES (%s, %s)")
        
        print(add_paper, data_paper)
        cursor.execute(add_paper, data_paper)
        
        conn.commit()
        cursor.close()
        conn.close()
        
    def delete(self, paper):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        title = paper.getInfo()['Title']
        date = paper.getInfo()['Publication date']
        year = date[:4]
        data_paper = (year, title)
        delete_paper = ( "DELETE FROM papers WHERE year= %s and title = %s")

        cursor.execute(delete_paper, data_paper)
        
        conn.commit()
        cursor.close()
        conn.close()
        

'''TESTING
ankai = AcademicPublisher()
ankai.first_name='ankai'
ankai.last_name='jie'
authDb = AuthorDbController()
authDb.delete(ankai)
'''

'''vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 1)'''
authDb = AuthorDbController()
authDb.connectPaperList('l', [1,2])

'''p1 = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')
papDb = PaperDbController()
papDb.insert(p1)'''

