explain-translation
===================

This Python script explains an Apertium translation in terms of its parts. More specifically, it looks for coorespondences between the translation of a text and its source. Run the script using `./explain.py`. To see the available options, try `./explain.py --help`:

```
$ ./explain.py --help
usage: explain.py [-h] [-m MAXSOURCELENGTH] [-M MAXTRANSLATIONLENGTH]
                  [-d DIRECTORY] [-t]
                  sourceLanguage targetLanguage S

Apertium translation parts

positional arguments:
  sourceLanguage        source language
  targetLanguage        target language
  S                     input text

optional arguments:
  -h, --help            show this help message and exit
  -m MAXSOURCELENGTH, --maxSourceLength MAXSOURCELENGTH
                        maximum length of whole-word subsegments (for source
                        text)
  -M MAXTRANSLATIONLENGTH, --maxTranslationLength MAXTRANSLATIONLENGTH
                        maximum length of whole word subsegments (for
                        translated text)
  -d DIRECTORY, --directory DIRECTORY
                        directory of Apertium language pair
  -t, --table           prints reference table of characters
```

An Example
----------
```
$ ./explain.py es ca "El tigre cuyo propietario es un pato rió." -t
[Coorespondence(s='El', t='El', i=0, j=1, k=0, l=1),
 Coorespondence(s='tigre', t='tigre', i=3, j=7, k=3, l=7),
 Coorespondence(s='propietario', t='propietari', i=14, j=24, k=12, l=21),
 Coorespondence(s='es', t='és', i=26, j=27, k=32, l=33),
 Coorespondence(s='un', t='un', i=29, j=30, k=35, l=36),
 Coorespondence(s='pato', t='ànec', i=32, j=35, k=38, l=41),
 Coorespondence(s='rió', t='va riure', i=37, j=39, k=43, l=50),
 Coorespondence(s='.', t='.', i=40, j=40, k=51, l=51),
 Coorespondence(s='El tigre', t='El tigre', i=0, j=7, k=0, l=7),
 Coorespondence(s='cuyo propietario', t='el propietari del qual', i=9, j=24, k=9, l=30),
 Coorespondence(s='es un', t='és un', i=26, j=30, k=32, l=36),
 Coorespondence(s='un pato', t='un ànec', i=29, j=35, k=35, l=41),
 Coorespondence(s='pato rió', t='ànec va riure', i=32, j=39, k=38, l=50),
 Coorespondence(s='rió.', t='va riure.', i=37, j=40, k=43, l=51),
 Coorespondence(s='tigre cuyo propietario', t='tigre el propietari del qual', i=3, j=24, k=3, l=30),
 Coorespondence(s='cuyo propietario es', t='el propietari del qual és', i=9, j=27, k=9, l=33),
 Coorespondence(s='es un pato', t='és un ànec', i=26, j=35, k=32, l=41),
 Coorespondence(s='un pato rió', t='un ànec va riure', i=29, j=39, k=35, l=50),
 Coorespondence(s='pato rió.', t='ànec va riure.', i=32, j=40, k=38, l=51),
 Coorespondence(s='El tigre cuyo propietario', t='El tigre el propietari del qual', i=0, j=24, k=0, l=30),
 Coorespondence(s='tigre cuyo propietario es', t='tigre el propietari del qual és', i=3, j=27, k=3, l=33),
 Coorespondence(s='cuyo propietario es un', t='el propietari del qual és un', i=9, j=30, k=9, l=36),
 Coorespondence(s='es un pato rió', t='és un ànec va riure', i=26, j=39, k=32, l=50),
 Coorespondence(s='un pato rió.', t='un ànec va riure.', i=29, j=40, k=35, l=51)]

0 : E E
1 : l l
2 :    
3 : t t
4 : i i
5 : g g
6 : r r
7 : e e
8 :    
9 : c e
10: u l
11: y  
12: o p
13:   r
14: p o
15: r p
16: o i
17: p e
18: i t
19: e a
20: t r
21: a i
22: r  
23: i d
24: o e
25:   l
26: e  
27: s q
28:   u
29: u a
30: n l
31:    
32: p é
33: a s
34: t  
35: o u
36:   n
37: r  
38: i à
39: ó n
40: . e
41:   c
42:    
43:   v
44:   a
45:    
46:   r
47:   i
48:   u
49:   r
50:   e
51:   .
```

