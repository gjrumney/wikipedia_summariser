import requests
from bs4 import BeautifulSoup
import time
import re
from transformers import pipeline
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)   

summariser = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

topic = ' '

def search_wiki(topic): # finds corresponding wiki article to topic
   
    f_topic = topic.replace(' ', '_')
    wiki_url = f'https://en.wikipedia.org/wiki/{f_topic}'
    
    return wiki_url

    
def web_scrape(wiki_url): # scrapes wiki article for cleaning
    
    d = requests.get(wiki_url)
    soup = BeautifulSoup(d.text, 'html.parser')
    
    text = ' '
    
    for p in soup.find_all('p'):
        text += p.text
        text += '\n'

    
    return text.strip()

def confirmer(text): # confirms whether article is correct using first line - asks for more specific topic if wrong
    
    global topic
    
    test = text.split('.')[0]
    print('\n' + test + '\n')
    check = input('Is this the correct topic? (Y/N) ')
    
    while check.lower() not in ['y', 'n']:
        print("That answer is invalid.")
        check = input('Is this the correct topic? (Y/N) ')
    
    while check.lower() == 'n':
        new_topic = input("Please specify further: ")
        new_wiki_url = search_wiki(new_topic)
        new_topic_info = web_scrape(new_wiki_url)
        text = new_topic_info
        topic = new_topic
        
        print('\n' + new_topic_info.split('.')[0] + '\n')
        check = input('Is this the correct topic? (Y/N) ')
        
        while check.lower() not in ['y', 'n']:
            print("That answer is invalid.")
            check = input('Is this the correct topic? (Y/N) ')
    
    if check.lower() == 'y':
        return text
    
    else:
        print('That answer is invalid.')
        return None

def summarise_text(text, chunk_size=800, min_length=30): # breaks text into chunks and summarises each
    if len(text) < min_length:
        print("Input text is too short for summarization.")
        return text
    
    total_chunks = (len(text) + chunk_size - 1) // chunk_size
    print('\n' +
        f'Total length of article: {len(text)}'
        + f'\n' + f'Predicted number of chunks: {total_chunks}' + '\n')
    
    completed_chunks = 0
    
    summaries = []
    
    for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
    
            try:
                start = time.time()
                max_length = min(150, len(chunk) // 2)
                summary = summariser(chunk, max_length=max_length, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])
                end = time.time()
                
                completed_chunks += 1
                print(f'{completed_chunks} / {total_chunks} completed ({end - start}s)')  
        
            except IndexError as e:
                print("IndexError:", e)
                print("Cleaned text length:", len(text))
                return "Error in summarization."
 
    first_sum = '\n'.join(summaries)
    return first_sum

def second_summ(first_sum, chunk_size=500): # performs a second summarisation if needed
    
    final_summary = []
    completed_chunks = 0
    
    total_chunks = (len(first_sum) + chunk_size - 1) // chunk_size
    print('\n' +
        f'Total length of first summary: {len(first_sum)}'
        + f'\n' + f'Predicted number of chunks: {total_chunks}' + '\n')


    for i in range(0, len(first_sum), chunk_size):
            chunk = first_sum[i:i + chunk_size]
    
            try:
                start = time.time()
                max_length = min(150, len(chunk) // 2)
                summary = summariser(chunk, max_length=max_length, min_length=10, do_sample=False)
                final_summary.append(summary[0]['summary_text'])
                end = time.time()
                
                completed_chunks += 1
                print(f'{completed_chunks} / {total_chunks} completed ({end - start}s)')  
        
            except IndexError as e:
                print("IndexError:", e)
                print("Cleaned text length:", len(first_sum))
                return "Error in summarization."
    
    final = '\n'.join(final_summary)
    return final
    
def main():
    
    start = time.time()
    
    global topic 
    topic = input('What do you want to learn about? ')
    wiki_url = search_wiki(topic)
    text = web_scrape(wiki_url)
    correct_text = confirmer(text)
    
    if correct_text:
        summary = summarise_text(correct_text)
        
        sentences = re.split(r'(?<=[.!?]) +', summary)  # Split on sentence-ending punctuation
        formatted_summary = '\n'.join(sentence.strip() for sentence in sentences if sentence)  # Strip whitespace and filter out empty strings
        
        filename = topic.replace(' ', '_')
        
        with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
            file.write(formatted_summary)
        end = time.time()
        
        print('\n'
              + f'Current length: {len(summary)}' 
              + f'\nSummary stored in "{filename}.txt"'
              + f'\nCompleted in {end - start}s')
        
        cont = input('\nFurther summarisation? (Y/N) ')
        
        while cont.lower() not in ['y', 'n']:
            print('That answer is invalid.')
            cont = input('\nFurther summarisation? (Y/N) ')
        
        if cont.lower() == 'n':
            pass
        
        else:
            start = time.time()
                        
            final_summary = second_summ(summary)
            
            sentences = re.split(r'(?<=[.!?]) +', final_summary)  
            formatted_summary = '\n'.join(sentence.strip() for sentence in sentences if sentence) 
            
            filename = topic.replace(' ', '_')
            
            with open(f'summaries/{filename}.txt', 'w', encoding='utf-8') as file:
                file.write(formatted_summary)
            end = time.time()
                
            print('\n'
                + f'Final length: {len(final_summary)}' 
                + f'\nSummary stored in "{filename}.txt"'
                + f'\nCompleted in {end - start}s')
            
        
        

if __name__ == '__main__':          
    main()




    
    