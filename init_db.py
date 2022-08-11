import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notices (title, content) VALUES (?, ?)",
            ('Microsoft anuncia uma prévia pública do suporte a Python para o Azure Functions', 'No recente evento Connect(), a Microsoft anunciou a prévia pública do suporte ao Python no Azure Functions. Os desenvolvedores podem criar funções usando o Python 3.6 com base no tempo de execução do Functions 2.0 e publicá-los em um plano de “consumo”.')
            )

cur.execute("INSERT INTO notices (title, content) VALUES (?, ?)",
            ('Flask: o que é e como codar com esse micro framework Python', 'Lançado em 2010 e desenvolvido por Armin Ronacher, a estrutura do Flask permite desenvolver aplicativos da web facilmente.Ronacher ganhou fama por liderar uma comunidade de entusiastas do Python chamada Poocco. O Flask é baseado no kit de ferramentas Werkzeg WSGI e na biblioteca Jinja2. Ambos são projetos herdados da Poocco.')
            )

connection.commit()
connection.close()