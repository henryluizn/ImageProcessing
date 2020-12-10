#### IMPORTS NECESSÁRIOS PARA O SCRIPT FUNCIONAR #####
import cv2 as cv
import argparse
import re
######################################################


if __name__ == "__main__":
    images = ['hulk1.png',
            'hulk2.png',
            'iron1.png',
            'iron2.png',
            'k3po1.png',
            'k3po2.png',
            'magneto1.png',
            'magneto2.png',
            'trooper1.png',
            'trooper2.png',
            'vader1.png',
            'vader2.png',
            'volve1.png',
            'volve2.png']

################## ALTERAÇÃO PARA NORMALIZAR HISTOGRAMAS ####################
#                * ALTERE A VARIÁVEL "NORMALIZE" DE 0 PARA 1 *

    normalize = 0

#############################################################################

    tam = len(images)               # quantidade de imagens
        
    maiorCorrel = -1                # -1 é o pior caso possível, imagem mais diferente
    maiorChisqr = float('inf')    # quanto maior o número mais diferente a imagem é
    maiorBhatta = 1                 # 1 é o pior caso possível, imagem mais diferente
    maiorInter = 0                  # quanto menor o valor, mais diferente a imagem é

    acertoCorrel = 0
    acertoChisqr = 0                # quantidade de acerto de cada método
    acertoBhatta = 0                
    acertoInter = 0

    methods = {
        'correl' : 'inter',
        'chisqr' : 'inter',         # 
        'bhatta' : 'inter', 
        'inter' : 'inter'
    }
    histograms = []             
    
    for i in range(0,tam):
        
        # reset dos Índices do maior percentual de cada método
        indexCorrel, indexChisqr, indexBhatta, indexInter = 1, 1, 1, 1 

        # preenchimento do vetor com os histogramas das imagens
        if i == 0:
            for k in range(0, tam):
                img1 = cv.imread('./Archive/'+images[k])
                histograms.insert(k,cv.calcHist([img1],
                                            [0, 1, 2],
                                            None,
                                            [256, 256, 256],
                                            [0, 256, 0, 256, 0, 256]
                                        ))
                if(normalize == 1):                     # se o vetor for normalizado
                    histograms[k] = cv.normalize(histograms[k], histograms[k], alpha = 0, beta = 1, norm_type = cv.NORM_MINMAX)

        for j in range(0,tam):
            if i != j:   

                histImg1 = histograms[i]
                histImg2 = histograms[j]

                        # comparando os histogramas com o método Intersection          
                compPercentCorrel = cv.compareHist(histImg1, histImg2, cv.HISTCMP_CORREL)
                if compPercentCorrel >= maiorCorrel:
                    maiorCorrel = compPercentCorrel     # testa se o maior atual precisa ser att e guarda o indice do maior
                    indexCorrel = j

                        # comparando os histogramas com o método ChiSquare
                compPercentChisquare = cv.compareHist(histImg1, histImg2, cv.HISTCMP_CHISQR)
                if compPercentChisquare <= maiorChisqr:
                    maiorChisqr = compPercentChisquare  # atualiza o menor valor encontrado
                    indexChisqr = j

                        # comparando os histogramas com o método Bhattacharyya
                compPercentBhatta = cv.compareHist(histImg1, histImg2, cv.HISTCMP_BHATTACHARYYA)
                if compPercentBhatta <= maiorBhatta:
                    maiorBhatta = compPercentBhatta     # atualiza o menor valor encontrado
                    indexBhatta = j

                        # comparando os histogramas com o método Intersection
                compPercentInter = cv.compareHist(histImg1, histImg2, cv.HISTCMP_INTERSECT)
                if compPercentInter >= maiorInter:
                    maiorInter = compPercentInter       # atualiza o maior valor encontrado
                    indexInter = j                    

        nomePersonagem = re.split("([1-2]+.png)$",images[i])    # nome personagem que está sendo comparado
        

            # atribuindo o nome das imagens que tiveram o maior percentual de igualdade
        methods['correl'] = re.split("([1-2]+.png)$",images[indexCorrel])
        methods['chisqr'] = re.split("([1-2]+.png)$",images[indexChisqr])
        methods['bhatta'] = re.split("([1-2]+.png)$",images[indexBhatta])
        methods['inter'] = re.split("([1-2]+.png)$",images[indexInter])

            # incrementa a quantidade de acertos dos métodos
        if nomePersonagem[0] == methods['correl'][0]:
            acertoCorrel += 1                            
        if nomePersonagem[0] == methods['chisqr'][0]:
            acertoChisqr += 1
        if nomePersonagem[0] == methods['bhatta'][0]:
            acertoBhatta += 1
        if nomePersonagem[0] == methods['inter'][0]:
            acertoInter += 1

            # reset do maior percentual de acerto de cada método
        maiorCorrel = -1                # -1 é o pior caso possível, imagem mais diferente
        maiorChisqr = float('inf')    # quanto maior o número mais diferente a imagem é
        maiorBhatta = 1                 # 1 é o pior caso possível, imagem mais diferente
        maiorInter = 0 


    print('\n\no número total de acertos com o método Correlation é: {}/{}'.format(acertoCorrel, 14))
    print('Percentual de acerto: {:.2f}%'.format(acertoCorrel/14*100))

    print('\n\no número total de acertos com o método ChiSquare é: {}/{}'.format(acertoChisqr, 14))
    print('Percentual de acerto: {:.2f}%'.format(acertoChisqr/14*100))

    print('\n\no número total de acertos com o método Bhattacharyya é: {}/{}'.format(acertoBhatta, 14))
    print('Percentual acerto: {:.2f}%'.format(acertoBhatta/14*100))

    print('\n\no número total de acertos com o método Inter é: {}/{}'.format(acertoInter, 14))
    print('Percentual acerto: {:.2f}%'.format(acertoInter/14*100))
