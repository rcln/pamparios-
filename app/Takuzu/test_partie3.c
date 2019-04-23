#include "fonctions.h"
#include "test_partie3.h"

void test_est_mouvement_valide(){
	grille *g = creer_grille(4);
	int val_cellule[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};

	int i;
	for(i = 0 ; i < 16 ; i++)
	{
		g->tab[i].val = val_cellule[i];
		g->tab[i].initial = initial_cellule[i];
	}
	int ligne,colonne,val;
	char m1[]="AA1";
	char m2[]="AB0";
	if(est_mouvement_valide(g, m1, &ligne, &colonne, &val)==1 && est_mouvement_valide(g, m2, &ligne, &colonne, &val)==0)
		printf("Test de la fonction rendre_cellule_initiale passé !\n");
	else
		printf("Test de la fonction rendre_cellule_initiale non passé !\n");

}

void test_tour_de_jeu(){
}

void test_jouer(){
}

void test_choisir_grille(){
}

void test_partie3(){
	printf("///////////////////////////////////////////////////\n//  Code correspondant aux tests de la partie 3  //\n///////////////////////////////////////////////////\n");
	test_est_mouvement_valide();
	test_tour_de_jeu();
	test_jouer();
	test_choisir_grille();
}
