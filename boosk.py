from data import livres, aime_livres

def livres_tries_par_annee():
    return sorted(livres, key=lambda l: l["année"])

]def plus_ancien_et_recent():
    livres_trie = livres_tries_par_annee()
    return livres_trie[0], livres_trie[-1]

def compteur_livres():
    d = {}
    for _, titre in aime_livres:
        d[titre] = d.get(titre, 0) + 1
    return d

def pagination_utilisateurs(utilisateurs, taille=2):
    i = 0
    while i < len(utilisateurs):
        yield utilisateurs[i:i+taille]
        i += taille
