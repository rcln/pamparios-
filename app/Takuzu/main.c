#include "fonctions.h"

int main()
{
	srand(time(NULL));
	
	system("clear");	
	color_printf(GREEN, MAGENTA, "Début du programme"); printf("\n");


	char c[]="Grilles/G./grille..txt";
	choisir_grille(c); 
	jouer(c);
	color_printf(YELLOW, CYAN, "Fin du programme"); printf("\n");

	return 0;
}
