import re

# Remove qualquer indicativo de participação especial da musica
feat = re.compile(r'\s[\(\[\-]\s?((feat[uring]?\.?)|with)[^\-)]*[\]\)]?'
                    ,flags=re.I)

# Remove parenteses ou traços que separam o indicativo de versões da faixa.
# Como de remix, por exemplo. Mas mantendo o texto.
singVersions = re.compile(r'\s[\(\[]|(\s\-\s)|[\]\)]',flags=re.I)

# Remove apóstrofos do texto. Pois, alguma vezes, uma das musicas podem estar
# com um caractere diferentes, prejudicando a comparação.
apostrophe = re.compile(r'\'|\’')

# Remova todo tipo de deluxe ou versões especiais do titulo do album
version = re.compile(r'\s[\(\[\-].*[\]\)]?',flags=re.I)

movieIndicator = re.compile(r'\s[\(\[\-]\s?[fF]rom[^\-)]*[\]\)]?$'
                    ,flags=re.I)