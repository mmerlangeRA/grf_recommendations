from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfpage import PDFPage
import io

class article:
    def __init__(self):
        print("new article")
        self.title = ""
        self.content = ""
        self.pages=[]

def extract_articles_from_pdf(pdf_path):
    title_font_size_threshold = 11  # Adjust this based on your PDF
    articles = []
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    current_article = None
    page_number=0
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_number +=1
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBox) or isinstance(element, LTTextLine):
                    x, y, text = element.bbox[0], element.bbox[3], element.get_text()
  
                    if(x>48 and x<220):
                        print(element)
                        print(text)
                        
                        #LTTextBoxHorizontal
                        if isinstance(element, LTTextBox):
                            for l in element:
                                print(l)
                                font_sizes = [char.size for char in l if isinstance(char, LTChar)]
                                text = l.get_text().strip()+" "
                                #print(text)
                                if font_sizes and max(font_sizes) > title_font_size_threshold:
                                    #print("title")
                                    if current_article is not None :
                                        #print("current_article is not None")
                                        if len(current_article.content)>0:#new article
                                            articles.append(current_article)
                                            current_article = article()
                                            current_article.pages.append(page_number)
                                            current_article.title = text
                                        else:
                                            current_article.title += text
                                    else:
                                        #print("current_article is None")
                                        current_article = article()
                                        current_article.title = text
                                        current_article.pages.append(page_number)

                                else:
                                    #print("not title")
                                    #print(font_sizes)
                                    if current_article is not None:
                                        current_article.content += " " + text
                                        if page_number not in current_article.pages:
                                            current_article.pages.append(page_number)
                    else:
                        print("wazza")
                        print(element)

    if current_article:
        articles.append(current_article)

    device.close()
    fake_file_handle.close()

    return articles

pdf_path = 'mini3.pdf'
pdf_path = '79478a96bf49d7f97fec134d2529d1c7.pdf'
articles = extract_articles_from_pdf(pdf_path)
for i, article in enumerate(articles):
    print(f"Article {i+1}:\n{article.title}\n\n")
    #print(article.content)
    print(article.pages)

#var PDF_SOURCE = "https://files.argoflow.io/document/79478a96bf49d7f97fec134d2529d1c7.pdf";