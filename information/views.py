from django.shortcuts import render
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from .forms import UploadFileForm
from PyPDF2 import PdfReader
import yake 
from googletrans import Translator



def upload_file(request):
    if request.method=='POST':
        form=UploadFileForm(request.POST,request.FILES)
        mypdf=request.FILES['fiel']
        if form.is_valid():
            
            pdf_reader = PdfReader(mypdf)
            num_pages = len(pdf_reader.pages)
            
            if num_pages>=15:
            
                get_all_text=extract_text(mypdf)
                summary=summarize(get_all_text)
                top_keywords=get_keywords(get_all_text)
                
                translated_text1 = get_text_in_english(summary)
                keyword1=get_keyword_in_english(top_keywords)
                
                translated_text2 = get_text_in_marathi(summary)
                keyword2=get_keyword_in_marathi(top_keywords)
            
            
                return render(request,'index.html',{'text':summary,'translated_text1':translated_text1,'keyword1':keyword1,'translated_text2':translated_text2,'keyword2':keyword2})
            else:
                msg = "Can't upload: PDF should have more than 15 pages."
                return render(request, 'index.html', {'form': form, 'msg': msg})

    else:
        form=UploadFileForm()
    return render(request,'index.html',{'form':form})
        

def extract_text(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]  
        text += page.extract_text()    
    return text

    

def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=5)  
    summary = " ".join(str(sentence) for sentence in summary)
    
    return summary


def get_keywords(text):
    extracted_keywords = yake.KeywordExtractor()
    keywords = extracted_keywords.extract_keywords(text)
    word = [keyword[0] for keyword in keywords]
    return word



def get_text_in_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='mr', dest='en')
    return translated_text.text


def get_keyword_in_english(keyword):
    translator = Translator()
    a=[]
    for key in keyword:
        translated_word = translator.translate(key, src='mr', dest='en').text
        a.append(translated_word)
    return a
    



def get_text_in_marathi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='mr')
    return translated_text.text


def get_keyword_in_marathi(keyword):
    translator = Translator()
    a=[]
    for key in keyword:
        translated_word = translator.translate(key, src='en', dest='mr').text
        a.append(translated_word)
    return a
    

