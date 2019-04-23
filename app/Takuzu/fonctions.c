#include "fonctions.h"

void clear_terminal()
{
  printf("\033[2J");
  printf("\033[0;0H");
}

int color_printf(COULEUR_TERMINAL fg, COULEUR_TERMINAL bg, const char * format, ...)
{
  int res;
  va_list args;
  printf("\x1B[1;%02d;%02dm", fg + 30, bg + 40);
  va_start(args, format);
  res = vprintf(format, args);
  va_end(args);
  printf("\x1B[00m");
  return res;
}



/****************************************************/
/*********************PARTIE 1***********************/
/****************************************************/

/**
 * Fonction allouant dynamiquement une grille dont l'adresse est retournée.
 * @param n : nombre de lignes/colonnes (4, 6, ou 8)
 * @return  : adresse de la grille, NULL en cas d'erreur
 */
grille * creer_grille(int n){
	assert(n==4 || n==6 || n==8);

	grille *g = malloc(sizeof(grille));	
	if (g == NULL) 
		exit(0);	
	g->n = n;

	g->tab = malloc(n * n * sizeof(cellule));
   	if (g->tab == NULL)
        	exit(0);

	int i;
	for(i=0;i<n*n;i++){
		g->tab[i].val=-1;
		g->tab[i].initial=0;
	}
	return g;
}


/**
 * Fonction désallouant dynamiquement la grille passée en paramètre.
 * @param g : grille à désallouer
 */
void detruire_grille(grille * g){
	free(g->tab);
	g->tab=NULL;
	free(g);
	g=NULL;
}

/**
 * Fonction retournant 1 si l'indice est valide par rapport à la grille.
 * @param g      : grille
 * @param indice : entier
 * @return       : 1 si indice est un indice valide pour g, 0 sinon
 */
int est_indice_valide(grille * g, int indice){

  	if (indice >= 0 && indice <(g->n)) 
  		return 1;

  	else
        	return 0;	
}

/**
 * Fonction retournant 1 si (i,j) est une cellule de la grille.
 * @param g : grille
 * @param i : numéro de ligne
 * @param j : numéro de colonne
 * @return  : 1 si (i,j) correspond à une cellule de g, 0 sinon
 */
int est_cellule(grille * g, int i, int j){
	
	if(est_indice_valide(g,i)==1 && est_indice_valide(g,j)==1) 	
		return 1;
	else 
		return 0;
}


/**
 * Fonction retournant la valeur de la cellule (i,j) de la grille g.
 *
 * @param g : grille
 * @param i : numéro de ligne
 * @param j : numéro de colonne
 */
int get_val_cellule(grille * g, int i, int j){
	
	assert(est_cellule(g,i,j) && "pas une cellule");
	return g->tab[g->n*i+j].val;
}


/**
 * Fonction modifiant la valeur de la cellule (i,j) de la grille g avec 
 * la valeur passée en paramètre.
 * @param g : grille
 * @param i : indice de ligne
 * @param j : indice de colonne
 * @param valeur : valeur à mettre dans le champ val de la cellule (i,j) 
 */
void set_val_cellule(grille * g, int i, int j, int val){
	
	assert(est_cellule(g,j,i) && "(i,j) n'est pas une cellule");
 	assert((val>=-1 && val <=1) && "val non compris entre -1 et 1");
	g->tab[g->n*i+j].val = val;
}


/**
 * Fonction retournant 1 si la cellule (i,j) est une cellule initiale, 
 * et 0 sinon.
 * @param g : grille
 * @param i : indice de ligne
 * @param j : indice de colonne 
 */
int est_cellule_initiale(grille * g, int i, int j){
	
	assert(est_cellule(g,i,j) && "(i,j) n'est pas une cellule");
	if(g->tab[g->n*i+j].initial == 1)
		return 1;
	else
		return 0;
}


/**
 * Fonction retournant 1 si la cellule (i,j) de la grille g est vide,
 * et 0 sinon.
 * @param g : grille
 * @param j : indice de colonne 
 * @param i : indice de ligne
 */
int est_cellule_vide(grille * g, int i, int j){
	
	assert(est_cellule(g,i,j) && "(i,j) n'est pas une cellule");	
	if(get_val_cellule(g,i,j) == -1)
		return 1;
	else 
		return 0;
}

/**
 * affiche la valeur (WHITE_MAGENTA)
 * @param g : grille
 * @param i : indice de ligne
 * @param j : indice de colonne 
 */

void WHITE_MAGENTA(grille * g, int i, int j){
	
	if(get_val_cellule(g, i, j) == -1){
		color_printf(WHITE,MAGENTA,"       ");
	}
	else{
		if(est_cellule_initiale(g, i, j)){
			if(get_val_cellule(g, i, j) == 1){	
				color_printf(YELLOW,MAGENTA,"   1   ");
			}				
			else{
				color_printf(YELLOW,MAGENTA,"   0   ");
			}
		}	
		else{
			if(get_val_cellule(g, i, j) == 1){	
				color_printf(WHITE,MAGENTA,"   1   ");
			}				
			else{
				color_printf(WHITE,MAGENTA,"   0   ");
			}			
		}
	}	
}

/**
 * affiche la valeur (WHITE_CYAN)
 * @param g : grille
 * @param i : indice de ligne
 * @param j : indice de colonne 
 */

void WHITE_CYAN(grille * g, int i, int j){
	
	if(get_val_cellule(g, i, j) == -1){
		color_printf(WHITE,CYAN,"       ");
	}
	else{
		if(est_cellule_initiale(g, i, j)){
			if(get_val_cellule(g, i, j) == 1){	
				color_printf(YELLOW,CYAN,"   1   ");
			}				
			else{
				color_printf(YELLOW,CYAN,"   0   ");
			}
		}	
		else{
			if(get_val_cellule(g, i, j) == 1){	
				color_printf(WHITE,CYAN,"   1   ");
			}				
			else{
				color_printf(WHITE,CYAN,"   0   ");
			}			
		}
	}
}


/*
*MAGENTA_CYAN_MAGNETA_CYAN
*@param g : grille
*@param i : indice de ligne
*/

void M_C(grille * g, int i, char c){
	int j;
	printf("  ");
	for(j=0;j<(g->n);j++){								
		if(j%2==0)
			color_printf(WHITE,MAGENTA,"       ");
		else
			color_printf(WHITE,CYAN,"       ");				
	}
	printf("\n%c ",c);
	for(j=0;j<(g->n);j++){						
		if(j%2==0)
			WHITE_MAGENTA(g, i, j);			
		else
			WHITE_CYAN(g, i, j);
	}
	printf("\n  ");		
	for(j=0;j<(g->n);j++){	
		if(j%2==0)
			color_printf(WHITE,MAGENTA,"       ");
		else
			color_printf(WHITE,CYAN,"       ");				
	}
	printf("\n");
}

/*
*CYAN_MAGNETA_CYAN_MAGENTA
*@param g : grille
*@param i : indice de ligne
*/

void C_M(grille * g, int i, char c){
	int j;
	printf("  ");
	for(j=0;j<(g->n);j++){
								
		if(j%2!=0)
			color_printf(WHITE,MAGENTA,"       ");
		else
			color_printf(WHITE,CYAN,"       ");				
	}
	printf("\n%c ",c);
	for(j=0;j<(g->n);j++){						
		if(j%2!=0)
			WHITE_MAGENTA(g, i, j);					
		else
			WHITE_CYAN(g, i, j);
	}
	printf("\n  ");		
	for(j=0;j<(g->n);j++){						
		if(j%2!=0)
			color_printf(WHITE,MAGENTA,"       ");
		else
			color_printf(WHITE,CYAN,"       ");				
	}
	printf("\n");
	
}

/**
 * Fonction affichant la grille sur le terminal.
 * @param g : pointeur sur la grille que l'on souhaite afficher
 */
void afficher_grille(grille * g){
	
	system("clear");
	
	char c = 'A';
	int i;
	
	for(i=0;i<(g->n);i++){
 		printf("     %c ",c);	
		c++;
	}
	printf("\n");
	
	c-=(g->n);

	for(i=0;i<(g->n);i++){
		if(i%2==0)
			M_C(g,i,c);
		else
			C_M(g,i,c);
	c++;	
	}
}


/****************************************************/
/*********************PARTIE 2***********************/
/****************************************************/

/**
*Fonction modifiant une cellule pour la rendre initiale.
*@param g : pointeur sur la grille
*@param i : indice de ligne
*@param j : indice de colonne
*/
void rendre_cellule_initiale(grille * g,int i,int j){

	assert(est_cellule(g,i,j) && "(i,j) n'est pas une cellule\n");	
	if((est_cellule_initiale(g, i, j))==0)
		g->tab[g->n*i+j].initial = 1;
}

/**
*@param nom_fichier : fichier contenant l'instance du problème
*@return            : pointeur sur la grille créée
*/

grille * initialiser_grille(char nom_fichier[]){ 
	FILE * f = fopen(nom_fichier,"rt");
	if(f == NULL){
		printf("Probleme d'ouverture du fichier\n");
		exit(0);	
	}
	int n;
	fscanf(f,"%d",&n);
	grille * g = creer_grille(n);
		
	int nb_ini;
	fscanf(f,"%d",&nb_ini);
	
	
	int i, j, val, x;
	
		
	
	for(x=0;x<nb_ini;x++){
		fscanf(f,"%d %d %d",&i, &j, &val);	
		g->tab[g->n*i+j].val = val;
		g->tab[g->n*i+j].initial = 1;

	}

	fclose(f);
	return g;
}

/**
*Fonction testant si la grille est entièrement remplie.
*@param g : grille à tester
*@return  : 1 si la grille est pleine, 0 sinon
*/


int est_grille_pleine(grille * g){
	int a = 1;
	int i,j;
	for(i=0;i<(g->n);i++){
		for(j=0;j<(g->n);j++){
			if(g->tab[g->n*i+j].val == -1)
				a++;
		}
	}
	if(a == 1)
		return 1;
	else 
		return 0;
}

/**
*Fonction vérifiant qu'il n'existe pas 3 zéro ou 3 un consécutifs dans
*la grille (ligne ou colonne).
*@param g : grille à tester
*@return  : 1 si c'est le cas, 0 sinon
*/

int pas_zero_un_consecutifs(grille * g)
{
	int verif = 1;
	int i, j;

	for(i=0;i<(g->n);i++)
	{
		for(j=0;j<(g->n)-2;j++)
		{
			// verif horizontal
			if(get_val_cellule(g,i,j) == get_val_cellule(g,i,j+1) && get_val_cellule(g,i,j) == get_val_cellule(g,i,j+2))
				verif++;
			//verif vertical			
			if(get_val_cellule(g,j,i) == get_val_cellule(g,j+1,i) && get_val_cellule(g,j,i) == get_val_cellule(g,j+2,i))
				verif++;				
		}
	}
	
	if(verif == 1)
		return 1;
	else
		return 0;
}

/**
*Fonction testant si le nombre de zéros est égal au nombre de uns dans
*chaque ligne/colonne.
*@param g : grille à tester
*@return  : 1 si c'est le cas, 0 sinon
*/

int meme_nombre_zero_un(grille * g){
	int un;
	int zero;
	int total1 = 0;
	int total2=0;
	int i, j;
	//verif v
	for(i=0;i<(g->n);i++){
		un = 0;
		zero = 0;
		for(j=0;j<(g->n);j++){
			
			if(get_val_cellule(g,i,j) == 1)
				un++;
			else	
				zero++;			
		}
		if(un == zero)
			total1++;	
	}
	//verif h
	for(i=0;i<(g->n);i++){
		un = 0;
		zero = 0;
		for(j=0;j<(g->n);j++){
			
			if(get_val_cellule(g,j,i) == 1)
				un++;
			else	
				zero++;			
		}
		if(un == zero)
			total2++;	
	}	

	if(total1 == (g->n) && total2 == (g->n))	
		return 1;
	else 
		return 0;
}


/**
*Fonction testant qu'il n'existe pas deux lignes identiques ou deux
*colonnes identiques.
*@param  g : grille à tester
*@return   : 1 si c'est le cas, 0 sinon
*/

int lignes_colonnes_distinctes(grille * g){
	
	int verif, i, j, k;
	int distin = 0;
	
	//vertical	
	for(k=0;k<(g->n)-1;k++)
	{	
		for(i=1+k;i<(g->n);i++)
		{
			verif=0;
			for(j=0;j<(g->n);j++)
			{
				if(get_val_cellule(g,j,k) == get_val_cellule(g,j,i))
					verif++;
			}
			if(verif==(g->n))
				distin++;
		}
	}
	

	//horizontal	
	for(k=0;k<(g->n)-1;k++)
	{	
		for(i=1+k;i<(g->n);i++)
		{
			verif=0;
			for(j=0;j<(g->n);j++)
			{				
				if(get_val_cellule(g,k,j) == get_val_cellule(g,i,j))
					verif++;
			}
			if(verif==(g->n))
				distin++;
		}
	}
	
	if(distin == 0)
		return 1;
	else 
		return 0;

}

/**
*Fonction déterminant si la partie est gagnée.
*@param  g : grille à tester
*@return   : 1 si la partie est gagnée, 0 sinon
*/



int est_partie_gagnee(grille * g){
	if(est_grille_pleine(g) == 1 && pas_zero_un_consecutifs(g) == 1 && meme_nombre_zero_un(g) == 1 && lignes_colonnes_distinctes(g) == 1)
		return 1;
	else 	
		return 0;
}



/****************************************************/
/*********************PARTIE 3***********************/
/****************************************************/


/**
*Fonction déterminant si un mouvement est valide. Si c'est le cas,
*elle met à jour les indices de ligne et colonne et la valeur en
*fonction de la saisie.
*@param  g       : pointeur sur la grille
*@param  mouv    : chaîne de caractères contenant le mouvement
*@param  ligne   : indice de ligne à modifier en fonction de mouv
*@param  colonne : indice de colonne à modifier en fonction de mouv
*@param  val     : valeur à modifier en fonction de mouv
*@return         : 1 si le mouvement est valide, et 0 sinon
*/

int est_mouvement_valide(grille * g, char mouv[], int * ligne, int * colonne, int * val){
	* ligne = mouv[0]-'A';
	* colonne = mouv[1]-'A';
	if(mouv[2] != '\0')
		* val = mouv[2]-'0';
	else 
		* val = -1;

	if(est_cellule(g, *ligne, *colonne) == 1 && est_cellule_initiale(g, *ligne, *colonne) == 0){
		if(*val == -1){
			if(get_val_cellule(g, *ligne, *colonne) != -1)
				set_val_cellule(g, *ligne, *colonne, *val);
			
		}
		else 	
			set_val_cellule(g, *ligne, *colonne, *val);

		return 1;	
	}
	else 
		return 0;			


	}


/**
*Fonction effectuant un tour de jeu :
*	- saisie jusqu'à ce que l'utilisateur saisisse un mouvement valide,
*	- modification de la grille en fonction de la saisie.
*@param  g : pointeur sur la grille
*/

void tour_de_jeu(grille * g){
	char mvt[4];	
	int ligne, colonne, val;	
	do{
		printf("Saisir un mouvement : (ex: AA1)\n");
		scanf("%s",mvt);
	}
	while(est_mouvement_valide(g, mvt, &ligne, &colonne, &val) == 0);
}


/**
*Fonction permettant de jouer au Takuzu.
*@param ch : Chaîne de caractères contenant le nom du fichier
*correspondant à l'instance du Takuzu
*/

void jouer(char ch[]){
	
	grille * g = initialiser_grille(ch);
	
	do{
		afficher_grille(g);	
		tour_de_jeu(g);	
		
	}
	while(est_partie_gagnee(g) != 1);
	
	afficher_grille(g);

	printf("\n");
	color_printf(YELLOW, CYAN, "               ");
	color_printf(YELLOW, CYAN, "\nVous avez gagne\n"); 
	color_printf(YELLOW, CYAN, "               ");
	printf("\n");
	
	detruire_grille(g);
}


/**
*Fonction permettant de choisir aléatoirement une grille dont la taille
*est saisie par l'utilisateur.
*@param s : chaîne de caractères contenant le nom de la grille
*choisie aléatoirement
*/

void choisir_grille(char s[]){
	char size_g;
	char g = '1'; 

	do{
		printf("Saisir la taille de la grille\n");
		scanf("%c",&size_g);
	}
	while(size_g != '4' && size_g != '6' && size_g != '8'); 
    	int nb=rand()%5+1; 
	s+=size_g;
	s+=9;
	*s=size_g;
	s+=8;
	
	int i;
	for(i=1;i<6;i++){
		if(nb == i)
			*s = g;
		else
			g++;	
	}
}
