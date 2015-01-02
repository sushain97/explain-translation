#!/usr/bin/env python3

import argparse, subprocess, itertools, collections, pprint
from streamparser.streamparser import parse

def analyzeText(text, locPair, pair, directory=None):
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    if directory:
        p2 = subprocess.Popen(['lt-proc', '-a', './{2}-{3}.automorf.bin'.format(locPair[0], locPair[1], pair[0], pair[1])], stdin=p1.stdout, stdout=subprocess.PIPE, cwd=directory)
    else:
        p2 = subprocess.Popen(['lt-proc', '-a', '/usr/local/share/apertium/apertium-{0}-{1}/{2}-{3}.automorf.bin'.format(locPair[0], locPair[1], pair[0], pair[1])], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return p2.communicate()[0].decode('utf-8').strip()

def translateText(text, pair, directory=None):
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    if directory:
        p2 = subprocess.Popen(['apertium', '-d', directory, '{0}-{1}'.format(*pair)], stdin=p1.stdout, stdout=subprocess.PIPE)
    else:
        p2 = subprocess.Popen(['apertium', '{0}-{1}'.format(*pair)], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return p2.communicate()[0].decode('utf-8').strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Apertium translation parts")
    parser.add_argument('sourceLanguage', help="source language")
    parser.add_argument('targetLanguage', help="target language")
    parser.add_argument('text', help="input text", metavar='S')
    parser.add_argument('-m', '--maxSourceLength', help="maximum length of whole-word subsegments (for source text)", type=int, default=5)
    parser.add_argument('-M', '--maxTranslationLength', help='maximum length of whole word subsegments (for translated text)', type=int, default=5)
    parser.add_argument('-d', '--directory', help="directory of Apertium language pair", default=None)
    parser.add_argument('-t', '--table', help='prints reference table of characters', action='store_true', default=False)
    args = parser.parse_args()

    pair = (args.sourceLanguage, args.targetLanguage)

    sourceText = args.text #S
    analyzedSourceText = analyzeText(sourceText, pair, pair, directory=args.directory)
    analyzedSourceUnits = list(parse(analyzedSourceText, withText=True))

    Coorespondence = collections.namedtuple('Coorespondence', ['s', 't', 'i', 'j', 'k', 'l'])
    coorespondences = []

    analyzedSourceUnitsSubsegments = []

    for length in range(1, args.maxSourceLength + 1):
        for startIndex in range(0, len(analyzedSourceUnits) - length + 1):
            lastIndex = startIndex + length - 1 
            analyzedSourceUnitsSubsegments.append((analyzedSourceUnits[startIndex:lastIndex+1], startIndex, lastIndex)) #s, i, j (analyzed units forms of them)

    translatedText = translateText(sourceText, pair, directory=args.directory)
    analyzedTranslation = analyzeText(translatedText, pair, pair[::-1], directory=args.directory)
    analyzedTranslationUnits = list(parse(analyzedTranslation, withText=True))

    analyzedTranslationUnitsSubsegments = []
    for length in range(1, args.maxTranslationLength + 1):
        for startIndex in range(0, len(analyzedTranslationUnits) - length + 1):
            lastIndex = startIndex + length - 1
            analyzedTranslationUnitsSubsegments.append((analyzedTranslationUnits[startIndex:lastIndex+1], startIndex, lastIndex))

    #pprint.pprint(analyzedSourceUnits)

    translatedTextSubsegements = []
    for analyzedSourceUnitsSubsegment, startIndexInUnits, lastIndexInUnits in analyzedSourceUnitsSubsegments:
        sourceTextSubsegment = '' #s
        for i, (analyzedSourceUnitPreceedingText, analyzedSourceLexicalUnit) in enumerate(analyzedSourceUnitsSubsegment):
            sourceTextSubsegment += (analyzedSourceUnitPreceedingText if i != 0 else '') + analyzedSourceLexicalUnit.wordform

        startIndexInSourceText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedSourceUnits[:startIndexInUnits]))) + len(analyzedSourceUnitsSubsegment[0][0]) #i
        lastIndexInSourceText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedSourceUnits[:lastIndexInUnits+1]))) - 1 #j

        translatedTextSubsegment = translateText(sourceTextSubsegment, pair, directory=args.directory) #t
        analyzedTranslatedTextSubsegment = analyzeText(translatedTextSubsegment, pair, pair[::-1], directory=args.directory)
        analyzedTranslatedTextSubsegmentUnits = list(parse(analyzedTranslatedTextSubsegment, withText=True))

        subsegmentMatches = list(filter(lambda x: list(map(lambda y: str(y[1]), x[0])) == list(map(lambda z: str(z[1]), analyzedTranslatedTextSubsegmentUnits)) , analyzedTranslationUnitsSubsegments))
        if subsegmentMatches:
            startIndexInTranslatedText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedTranslationUnits[:subsegmentMatches[0][1]]))) + len(subsegmentMatches[0][0][0][0]) #k
            lastIndexInTranslatedText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedTranslationUnits[:subsegmentMatches[0][2]+1]))) - 1 #l

            coorespondences.append(Coorespondence(
                s=sourceTextSubsegment, 
                t=translatedTextSubsegment,
                i=startIndexInSourceText, 
                j=lastIndexInSourceText, 
                k=startIndexInTranslatedText, 
                l=lastIndexInTranslatedText
            ))

    #print('Source text: %s' % repr(sourceText))
    #print('Translated text: %s\n' % repr(translatedText))
    pprint.pprint(coorespondences)

    if args.table:
        print('\n')
        print('\n'.join(list(map(lambda i: '%s: %s %s' % (str(i).ljust(2), sourceText[i] if i < len(sourceText) else ' ', translatedText[i] if i < len(translatedText) else ' '), range(0, max(len(sourceText), len(translatedText)))))))

