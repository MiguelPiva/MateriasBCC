import json, pandas as pd, requests


# Limited subjects codes
list_codes = ["MCZA035-17", "MCZA036-17", "MCZA001-13", "MCTB007-17", "MCZA002-17", "MCZA003-17", "MCZA004-13", "MCZA005-17", "MCTB009-17", "MCZA037-17", "MCZA006-17", "ESZG013-17", "MCZA007-13", "MCZA051-17", "ESZI030-17", "MCZA016-17", "ESZG019-17", "MCTB018-17", "MCZB012-13", "ESZI013-17", "MCZA008-17", "ESZB022-17", "MCZB015-13", "MCZB018-13", "MCTC021-15", "MCZA032-17", "ESZI034-17", "MCZA010-13", "MCZA011-17", "MCZA012-13", "MCZA013-13", "MCZA014-17", "MCZA015-13", "ESTG013-17", "ESZI022-17", "MCZA038-17", "MCZA039-17", "MCZA040-17", "MCZA041-17", "MCZA017-13", "MCTC022-15", "MCZA018-17", "MCZA042-17", "MCZA033-17", "ESZI033-17", "MCZA019-17", "MCZA020-13", "MCZA034-17", "MCZA021-17", "MCZA022-17", "MCZA023-17", "ESZI029-17", "MCZA024-17", "MCZA044-17", "MCZA045-17", "MCZA025-13", "MCZA046-17", "MCZA026-17", "MCZA027-17", "ESZI014-17", "MCZA028-13", "MCZA029-13"]


# Extract text from the url
def Extract_text(url):
    response = requests.get(url)
    Url_status(response.status_code)

    js_content = response.text.strip().rstrip(";")
    js_content = js_content.replace("todasDisciplinas=", "")
    data = json.loads(js_content)

    return data


# Check if the url is valid
def Url_status(response):
    if (response != 200):
        print("Erro ao acessar a página.")
        exit()
    
    return


# Create a pandas dataframe
def Create_table(data):
    df = pd.DataFrame(data)

    return df


# Format the pandas dataframe
def Format_table(table):
    rm_columns = ["horarios", "campus", "id", "creditos", "nome_campus", "vagas_ingressantes", "recomendacoes", "obrigatoriedades"]
    table.drop(columns=rm_columns, inplace=True )
    table["tpi"] = table["tpi"].apply(process_tpi)

    return table


# Format the tpi column
def process_tpi(line):
    line = [str(line).replace(", ", "-").lstrip("[").rsplit("]")]

    return str(line).replace("[['", "").replace("', '']]","")


# print limited subjects
def Print_subjects(table):
    num_linhas, num_colunas = table.shape
    for i in range(num_linhas):
        valor = table.iloc[i, 0]
        if (valor in list_codes):
            print(">","".join(table["nome"].iloc[i:i+1].str.rstrip()), end=" - ")
            print("".join(table["tpi"].iloc[i:i+1].str.rstrip()))


# Main
if __name__ == "__main__":
    url_js = "https://matricula.ufabc.edu.br/cache/todasDisciplinas.js"

    step_1 = Extract_text(url_js)
    step_2 = Create_table(step_1)
    step_3 = Format_table(step_2)
    step_4 = Print_subjects(step_3)