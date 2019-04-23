#include "fonctions.h"
#include "test_partie2.h"

void test_rendre_cellule_initiale(){
	grille * g=creer_grille(4);
	int i=0;
	int j=0;
	rendre_cellule_initiale(g,i,j);
	if(g->tab[0].initial==1 && g->tab[1].initial==0)
		printf("Test de la fonction rendre_cellule_initiale passé !\n");
	else
		printf("Test de la fonction rendre_cellule_initiale non passé !\n");
}

void test_initialiser_grille(){
	char c[]="grille.txt";
	grille *g = initialiser_grille(c);
	detruire_grille(g);
	printf("test de la fonction initialiser_grille passé !\n");
}

void test_est_grille_pleine(){

	grille *g1 = creer_grille(4);
	int val_cellule_1[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_1[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};

	grille *g2 = creer_grille(4);
	int val_cellule_2[16] = {-1,1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,0,-1};
	int initial_cellule_2[16] = {0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0};

	int i;
	for(i = 0 ; i < 16 ; i++){
		g1->tab[i].val = val_cellule_1[i];
		g1->tab[i].initial = initial_cellule_1[i];

		g2->tab[i].val = val_cellule_2[i];
		g2->tab[i].initial = initial_cellule_2[i];
	}
	if(est_grille_pleine(g1)==1 && est_grille_pleine(g2)==0)
		printf("Test de la fonction est_grille_pleine passé !\n");
	else
		printf("Test de la fonction est_grille_pleine non passé !\n");

	detruire_grille(g1);
	detruire_grille(g2);
}

void test_pas_zero_un_consecutifs()
{
	grille *g1 = creer_grille(4);
	int val_cellule_1[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_1[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	grille *g2 = creer_grille(4);
	int val_cellule_2[16] = {1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_2[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	int i;
	for(i = 0 ; i < 16 ; i++)
	{
		g1->tab[i].val = val_cellule_1[i];
		g1->tab[i].initial = initial_cellule_1[i];

		g2->tab[i].val = val_cellule_2[i];
		g2->tab[i].initial = initial_cellule_2[i];
	}
	if(pas_zero_un_consecutifs(g1) == 1 && pas_zero_un_consecutifs(g2) == 0)
		printf("Test de la fonction pas_zero_un_consecutifs passé !\n");
	else
		printf("Test de la fonction pas_zero_un_consecutifs non passé !\n");

	detruire_grille(g1);
	detruire_grille(g2);
}

void test_meme_nombre_zero_un()
{
	grille *g1 = creer_grille(4);
	int val_cellule_1[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_1[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	grille *g2 = creer_grille(4);
	int val_cellule_2[16] = {1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_2[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	int i;
	for(i = 0 ; i < 16 ; i++)
	{
		g1->tab[i].val = val_cellule_1[i];
		g1->tab[i].initial = initial_cellule_1[i];

		g2->tab[i].val = val_cellule_2[i];
		g2->tab[i].initial = initial_cellule_2[i];
	}

	if(meme_nombre_zero_un(g1) == 1 && meme_nombre_zero_un(g2) == 0)
		printf("Test de la fonction meme_nombre_zero_un passé !\n");
	else
		printf("Test de la fonction meme_nombre_zero_un non passé !\n");

	detruire_grille(g1);
	detruire_grille(g2);
}

void test_lignes_colonnes_distinctes()
{
	grille *g1 = creer_grille(4);
	int val_cellule_1[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_1[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	grille *g2 = creer_grille(4);
	int val_cellule_2[16] = {0,0,1,0,1,1,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_2[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};

	int i;
	for(i = 0 ; i < 16 ; i++)
	{
		g1->tab[i].val = val_cellule_1[i];
		g1->tab[i].initial = initial_cellule_1[i];

		g2->tab[i].val = val_cellule_2[i];
		g2->tab[i].initial = initial_cellule_2[i];
	}


	if(lignes_colonnes_distinctes(g1) == 1  && lignes_colonnes_distinctes(g2) == 0)
		printf("Test de la fonction lignes_colonnes_distinctes passé !\n");
	else
		printf("Test de la fonction lignes_colonnes_distinctes non passé !\n");

	detruire_grille(g1);
	detruire_grille(g2);
}

void test_est_partie_gagnee()
{
	grille *g1 = creer_grille(4);
	int val_cellule_1[16] = {0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_1[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};
	grille *g2 = creer_grille(4);
	int val_cellule_2[16] = {1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0};
	int initial_cellule_2[16] = {0,1,0,1,0,0,1,0,0,1,0,0,1,1,0,1};

	int i;
	for(i = 0 ; i < 16 ; i++)
	{
		g1->tab[i].val = val_cellule_1[i];
		g1->tab[i].initial = initial_cellule_1[i];

		g2->tab[i].val = val_cellule_2[i];
		g2->tab[i].initial = initial_cellule_2[i];
	}


	if(est_partie_gagnee(g1) == 1 && est_partie_gagnee(g2) == 0 )
		printf("Test de la fonction est_partie_gagnee passé !\n");
	else
		printf("Test de la fonction est_partie_gagnee non passé !\n");

	detruire_grille(g1);
	detruire_grille(g2);
}

void test_partie2(){
	printf("///////////////////////////////////////////////////\n//  Code correspondant aux tests de la partie 2  //\n///////////////////////////////////////////////////\n");
	test_rendre_cellule_initiale();
	test_initialiser_grille();
	test_est_grille_pleine();
	test_pas_zero_un_consecutifs();
	test_meme_nombre_zero_un();
	test_lignes_colonnes_distinctes();
	test_est_partie_gagnee();
}
