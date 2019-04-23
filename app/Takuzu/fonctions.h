#ifndef FONCTIONS_H
#define FONCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <time.h>


//////////////////////////////////////////////////////////////
// Code permettant d'utiliser les couleurs dans le terminal //
//////////////////////////////////////////////////////////////


// Couleurs possibles
typedef enum
  {
    BLACK,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
    WHITE
  } COULEUR_TERMINAL;


void clear_terminal();

int color_printf(COULEUR_TERMINAL fg, COULEUR_TERMINAL bg, const char * format, ...);


////////////////////////////////////////////
// DÉFINIR LE TYPE STRUCTURÉ cellule ici  //
////////////////////////////////////////////
typedef struct
{
	int val;
	int initial;
}cellule;


//////////////////////////////////////////
// DÉFINIR LE TYPE STRUCTURÉ grille ici //
//////////////////////////////////////////
typedef struct 
{
	cellule *tab;
	int n;
}grille;




/****************************************************/
/*********************PARTIE 1***********************/
/****************************************************/


grille * creer_grille(int n);

void detruire_grille(grille * g);

int est_indice_valide(grille * g, int indice);

int est_cellule(grille * g, int i, int j);

int get_val_cellule(grille * g, int i, int j);

void set_val_cellule(grille * g, int i, int j, int val);

int est_cellule_initiale(grille * g, int i, int j);

int est_cellule_vide(grille * g, int i, int j);

void WHITE_MAGENTA(grille * g, int i, int j);

void WHITE_CYAN(grille * g, int i, int j);

void M_C(grille * g, int i, char c);

void C_M(grille * g, int i, char c);

void afficher_grille(grille * g);


/****************************************************/
/*********************PARTIE 2***********************/
/****************************************************/


void rendre_cellule_initiale(grille * g,int i,int j);

grille * initialiser_grille(char nom_fichier[]);

int est_grille_pleine(grille * g);

int pas_zero_un_consecutifs(grille * g);

int meme_nombre_zero_un(grille * g);

int lignes_colonnes_distinctes(grille * g);

int est_partie_gagnee(grille * g);


/****************************************************/
/*********************PARTIE 3***********************/
/****************************************************/


int est_mouvement_valide(grille * g, char mouv[], int * ligne, int * colonne, int * val);

void tour_de_jeu(grille * g);

void jouer(char ch[]);

void choisir_grille(char s[]);



#endif