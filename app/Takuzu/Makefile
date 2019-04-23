#################################################################
## AUTEURS : CHETOUANI Mohamed     GANESAN Chandra             ##
##                                                             ##
## DATE    : 10/12/2017																	       ##
##                                                             ##
## Makefile :	 Takuzu	Project																	 ##
## 			 																			             		 ##
##                                                             ##
#################################################################

SRC	=	main.c \
			fonctions.c \
			test_partie1.c \
			test_partie2.c \
			test_partie3.c 

NAME	=	Takuzu

CFLAGS	=	-Wall

$(NAME):
				gcc -o $(NAME) $(SRC) $(CFLAGS)

clean:
				rm -rf Takuzu

re:	clean
				-gcc -o $(NAME) $(SRC) $(CFLAGS)
