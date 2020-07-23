from bs4 import BeautifulSoup
import requests
import xlwt 
from xlwt import Workbook 

def str_splt(s, n, sym):
    
    count = 0
    c = 0
        
    for i in s:
        if i == sym and count == (n - 1):
            return c
        else:
            c += 1
            if i == sym:
                count += 1
    return c
            
                
def ball():
    
    months = ['october', 'november', 'december', 'january',
              'february', 'march']
        
    main = 'https://www.basketball-reference.com'
                
    all_months = 'https://www.basketball-reference.com/leagues/NBA_2020_games-'
    
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    
    cell = 2
    
    games = []
    for month in months:
        url = all_months + month + '.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        games_l = soup.find_all('tr')        
        
        for tr in games_l:
                box = list(tr.find_all('td'))

                for o in box:
                    b = str(o)
                    
                    if 'Box Score' in b:
                        b = b[55:83]
                        pbp_link = main + b[:11] + 'pbp' + '/' + b[11:]
                        games.append(pbp_link)
                        
                        
    for game in games:
        p = requests.get(game)
        pbp = BeautifulSoup(p.content, 'html.parser')
        log = pbp.find_all('tr')
        
        
        c=0
       
        for tr in (log):
            c +=1
            plays = list(tr.find_all('td'))
             
            for play in plays:
                
                dic = {}
                
                occur = str(play)
                
                ind = str_splt(occur, 2, '>')
                occur = occur[(ind+1):]
                
                ind_2 = str_splt(occur, 1, '<')
                ind_3 = str_splt(occur, 1, '>') + 1
                
                ind_4 = str_splt(occur, 2, '<')
                ind_5 = str_splt(occur, 2, '>') + 1 
                
                occur = occur[:ind_2] + occur[ind_3 : ind_4] + occur[ind_5: -10]
            
                if 'miss' and 'block' in occur:
                    x = occur.split()
                    
                    player = ' '.join(x[-2:])
                    att = x[3][0]
                    
                    
                    dic['player'] = player
                    dic['attempt'] = att
                    
                    
                    if c < len(log):
                        next_row = log[c]
                        z = str(next_row)
                    
                    #print(z)
                    if 'Offensive' in z:
                        dic['reb'] = 'O'
                        
                        n_row = log[c+1]
                        d = str(n_row).split()[5:]
                        
                        if  'makes' in d:
                            indie = d.index('makes')
                            dic['next'] = d[indie+1]
                            dic['bucket'] = True
                            
                            
                        elif  'misses' in d:
                            indie = d.index('misses')
                            dic['next'] = d[indie+1]
                            dic['bucket'] = False
                            
                        else:
                            dic['bucket'] = False
                        
                    elif 'Defensive' in z:
                        dic['reb'] = 'D'
                        
                    else:
                        dic['reb'] = '?'
                        
                    
                    sheet1.write(cell, 1, dic['player'] )
                    sheet1.write(cell, 2, dic['attempt'])
                    
                    if dic['reb'] == 'O':
                        
                        sheet1.write(cell, 4, 1)
                        sheet1.write(cell, 3, 0)
                        if len(dic) > 4:
                            sheet1.write(cell, 5, int(dic['next'][0]))
                            
                            if dic['bucket'] == True:
                                sheet1.write(cell, 6, int(dic['next'][0]))
                            else:
                                sheet1.write(cell, 6, 0)
                                
                    elif dic['reb'] == 'D':
                        sheet1.write(cell, 4, 0)
                        sheet1.write(cell, 3, 1)
                        
                    else:
                        sheet1.write(cell, 4, dic['reb'])           
                        
                    cell += 1                   
                    
        wb.save('blocks.xls')
