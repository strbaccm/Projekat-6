from bs4 import BeautifulSoup
import requests, openpyxl 

# ''' blok string

#kreiramo novi eksel fajl
#aktivni sheet gdje cemo smjestati podatke

excel = openpyxl.Workbook()
print(excel.sheetnames)

sheet = excel.active
sheet.title = 'IMDB Movie Ratings'
print(excel.sheetnames)

#potrebne su nam 4 kolone, kreiramo ih

sheet.append(['Movie Rank', 'Movie Name', 'Year of Release', 'IMDB Rating'])



try:
    source = requests.get('https://www.imdb.com/chart/top/')
    source.raise_for_status()  #hvata gresku ukoliko upisemo nepostojecu adresu

    soup = BeautifulSoup(source.text, 'html.parser') 
    
    #find nalazi prvi pogodatak
    #find_all uvijek vraca listu, fin_all trazi sve tr
    #len vraca duzinu liste

    movies = soup.find('tbody', class_ = "lister-list" ).find_all('tr')  
    
    for movie in movies:

        #trayimo tag a , pa trazimo dalje kontent a
        #koristimo tekst metod 
        #dobijamo ime filma

        name = movie.find('td', class_="titleColumn").a.text

        #trazimo rank filma
        #sa text medotom izvlacimo sav tekst koji se nalazi u tom tagu
        #get_text: dobijamo takodje sav tekst samo bez razmaka
        #sa split dobijamo listu, potreban nam je nulti clan liste

        rank = movie.find('td', class_="titleColumn").get_text(strip = True).split('.')[0]


        #trazimo godinu filma
        #span je tag
        #pomocu strip metode uklanjamo zagrade, string metoda

        year = movie.find('td', class_="titleColumn").span.text.strip('()')


        # trazimo ocjenu filma
        #pristupamo strong tagu i trazimo tekst

        rating = movie.find('td', class_ = "ratingColumn imdbRating").strong.text


    
        print(rank, name, year, rating)

        #popunjavamo exel file

        sheet.append([rank, name, year, rating])
        

except Exception as e:
    print(e)


excel.save('IMDB Movie Ratings.xlsx')
   

 