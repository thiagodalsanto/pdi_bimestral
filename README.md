## Projeto Bimestral (Processamento Digital de Imagens - PDI )

Este repositório contém um projeto bimestral de Processamento Digital de Imagens (PDI) que oferece uma ampla gama de recursos para o processamento e manipulação de imagens. A aplicação foi desenvolvida em Python e utiliza várias bibliotecas, incluindo OpenCV, PIL e TKInter, para fornecer uma interface amigável e funcionalidades poderosas.

## Sobre o trabalho:

* Disciplina: OP63I-CC8 - Processamento De Imagens E Reconhecimento De Padrões	
* Turma: 2023/2 - 8º Período
* Docente: Prof. Dr. Pedro Luiz de Paula Filho

## Recursos 
- **Conversão de Cores:** O usuário pode converter a imagem enviada para qualquer padrão de cor presente no OpenCV.
- **Aplicação de Threshold:** O usuário pode converter a imagem enviada para Threshold RGB ou Gray Tones Threshold.
- **Controle de Contrase:** O usuário pode controlar o contraste da imagem enviada.
- **Identificação de Bordas:** O usuário pode aplicar o filtro Canny, para identificar bordas através dos limiares superior e inferior.
- **Aplicação de Morfologia:** O usuário pode aplicar morfologias de Erosão e Dilatação na imagem enviada.
- **Aplicação de Blur:** O usuário pode Aplicar Blur Bilateral, Gaussiano e Mediano na imagem enviada.
- **Controle de Duplicidade:** O usuário é impedido de atribuir uma conversão de cores à uma imagem que já teve conversão de cores.
- **Histórico de Atividades e Deleção:** A aplicação possui um histórico de atividades executadas na imagem, onde aparecem os filtros aplicados e os valores para cada filtro. Além de poder deletar qualquer um deles, independente da ordem.
- **Preview:** A aplicação fornece em tempo real uma imagem preview, com as conversões e aplicações feitas nela.

## Dependências
**Dependêndicas utilizadas:** Python 3, OpenCV (cv2), PIL e TKInter.

### Para o Linux:  
`pip install opencv-python tkinter pillow` 

### Para o Windows:
1. Python 3.11.5 ([Instalador 64-bit](https://www.python.org/downloads/windows/))
2. `pip install opencv-python tkinter pillow` 

## Como Utilizar
1. Clone o repositório do GitHub: `git clone https://github.com/thiagodalsanto/pdi_bimestral.git`
2. Instale as [dependências](#dependências) utilizadas
3. Execute o aplicativo em uma IDE, dentro da raiz do projeto, com o comando:
   1. Linux: `python3 main.py`
   2. Windows: `python main.py`

## Imagens da Aplicação
Imagem 1 - Aplicação com uma imagem enviada (esquerda), o preview da imagem (direita), na esquerda inferior os filtros possíveis a serem aplicados, a direita dos filtros está o histórico com os dados selecionados para cada um dos filtros. Na direita inferior consta os botões interativos com a aplicação e histórico.

<p align="center">
    <img src="https://i.imgur.com/t4gyd9G.png" width="800">
</p>

Imagem 2 - Imagem com filtro RGB to YCrCb aplicado, tentando aplicar o filtro RGB to XYZ, oque mostra um dos controlares criados, mostrando que é impossível fazer isso, já que a imagem não está em RGB mais. 
<p align="center">
    <img src="https://i.imgur.com/gHqJdg8.png" width="800">
</p>