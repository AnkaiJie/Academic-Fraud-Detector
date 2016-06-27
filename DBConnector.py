'''
Created on Feb 3, 2016

@author: Ankai
'''

import mysql.connector

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
        
        #print('paper list objects: ' + author.getPapers())
        self.connectPaperList(author, author.getPapers())
        
        
    def delete(self, author):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        data_author = (author.getFirstName(), author.getLastName())
        delete_author = ( "DELETE FROM authors WHERE first_name= %s and last_name = %s")
        cursor.execute(delete_author, data_author)
        
        conn.commit()
        cursor.close()
        conn.close()
        
    #connect already created author to a paper written by him/her
    def connectPaper(self, author, paper):
        conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
        cursor = conn.cursor()
        
        data_author = (author.getFirstName(), author.getLastName())
        print('data author: '+ str(data_author))
        #data_author = ('athanasios', 'vasilakos')
        
        cursor.execute('SELECT id FROM authors WHERE first_name= %s and last_name = %s LIMIT 0, 1;',data_author )
        author_id = cursor.fetchone()[0]

            
        title = paper.getInfo()['Title']
        date = paper.getInfo()['Publication date']
        year = date[:4]
            
        data_paper = (year, title)
        #data_paper = (2011, 'Body Area Networks: A Survey')
        print('data_paper: '+str(data_paper))
            
        cursor.execute('SELECT id FROM papers WHERE year= %s and title = %s LIMIT 0, 1;',data_paper)
        paper_id = cursor.fetchone()[0]
        
        data = (author_id, paper_id)
        
        #print('INSERT INTO paper_authors (author_id, paper_id) VALUES (%s, %s);', data)
        
        cursor.execute('INSERT INTO paper_authors (author_id, paper_id) VALUES (%s, %s);', data)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    
    #connects already created author to a list of papers, all by that author
    def connectPaperList(self, author, paper_list):
        for paper in paper_list:        
            papCtrl = PaperDbController()
            papCtrl.insert(paper) 
            self.connectPaper(author, paper)
   

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

'''vas = AcademicPublisher('https://scholar.google.ca/citations?user=_yWPQWoAAAAJ&hl=en&oi=ao', 10)
authDb = AuthorDbController()
authDb.insert(vas)'''
#authDb.connectPaper()

'''p1 = Paper('https://scholar.google.ca/citations?view_op=view_citation&hl=en&user=_yWPQWoAAAAJ&citation_for_view=_yWPQWoAAAAJ:u5HHmVD_uO8C')
papDb = PaperDbController()
papDb.insert(p1)'''

'''conn = mysql.connector.connect(user='Ankai', password='Ankai', host='localhost', database='pythonura')
cursor = conn.cursor()

data_paper = (2011, 'Body area networks: A survey')
cursor.execute('SELECT id FROM papers WHERE year= %s and title = %s;',data_paper)
print(str(cursor.fetchone()[0]))

        
cursor.close()
conn.close()'''

