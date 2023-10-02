import requests, io, PyPDF2, pandas as pd


def Get_content(url):

    web_page = requests.get(url) 
    file = io.BytesIO(web_page.content)
    pdf = PyPDF2.PdfReader(file)

    content = []
    for page in pdf.pages:
        content.append(page.extract_text())

    return content


def Make_lines(pages):
    for i in range(0, len(pages)):
        pages[i] = pages[i].split("\n")

    lines = []
    for page in pages:
        for line in page:
            lines.append(line.lstrip())

    return lines


def Select_content(lines):
    course_subjects = []

    for line in lines:
        if Verify_line(line):
            course_subjects.append(line)
    return course_subjects
        

def Verify_line(line):
    initials = ["MCZ", "MCT", "ESZ", "EST", "NHZ"] #Initials of Computer Science subjects
    for initial in initials:
        if initial in line[:5:]:
            return True
            

def Format_content(lines):
    for i in range(0, len(lines)):
        lines[i] = [
                    lines[i][:11:].replace(" ", ""), 
                    lines[i][11:(len(lines[i])-8):].strip(), 
                    lines[i][(len(lines[i])-8):(len(lines[i])-2):].strip().replace(" ", "-")
                    ]
        
    return lines


def Subject_key(subject):
    name = subject[1]

    if name.startswith("Á"):
        return "A" + name[1:]
    elif name.startswith("Â"):
        return "A" + name[1:]
    elif name.startswith("É"):
        return "E" + name[1:]
    elif name.startswith("Í"):
        return "I" + name[1:]
    elif name.startswith("Ó"):
        return "O" + name[1:]
    
    return name


def Sort_subjects(lines):
    sorted_lines = sorted(lines, key=Subject_key)

    return sorted_lines


def Create_table(data):
    df = pd.DataFrame({"Sigla":[], "Nome":[], "T-P-I":[]})

    for sub in data:
        df.loc[len(df.index)] = [sub[0], sub[1], sub[2]]

    print(df)
    xlsx_archive = input("Deseja salvar em archivo xlsx (Excel)? ( s / N )")
    print(xlsx_archive)
    if (xlsx_archive.lower() == "s"):
        df.to_excel("tabelaBCC.xlsx")
        print("Arquivo criado.")

    return df


if __name__ == "__main__":
    url = "https://www.ufabc.edu.br/images/consepe/resolucoes/resolucao-211-revisao-do-pp-do-bacharelado-em-ciencia-da-computacao-esta-versao-contempla-as-retificacoes.pdf"

    step_1 = Get_content(url)
    step_2 = Make_lines(step_1)
    step_3 = Select_content(step_2)
    step_4 = Format_content(step_3)
    step_5 = Sort_subjects(step_4)
    step_6 = Create_table(step_5)