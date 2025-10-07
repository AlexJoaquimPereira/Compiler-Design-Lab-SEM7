%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Binary Search Tree
struct word_node {
    char *word;
    int count;
    struct word_node *left;
    struct word_node *right;
};

struct word_node *root = NULL;

void add_word(char *word);
void print_sorted_frequencies(struct word_node *node);
%}

WORD [a-zA-Z]+

%%

{WORD} {
    // Convert yytext to lowercase in-place
    for (int i = 0; yytext[i]; i++) {
        yytext[i] = tolower(yytext[i]);
    }
    // Add the processed word to the tree
    add_word(yytext);
}

.|\n { /* Ignore */ }

%%

/* add_word: Inserts a word into the BST.
 * - If the word already exists, its count is incremented.
 * - If it's a new word, a new node is created and inserted.
 */
void add_word(char *word) {
    struct word_node *current = root;
    struct word_node *parent = NULL;
    int comparison;

    while (current != NULL) {
        parent = current;
        comparison = strcmp(word, current->word);
        if (comparison == 0) {
            current->count++;
            return;
        } else if (comparison < 0) {
            current = current->left;
        } else {
            current = current->right;
        }
    }

    struct word_node *new_node = (struct word_node*) malloc(sizeof(struct word_node));
    new_node->word = strdup(word);
    new_node->count = 1;
    new_node->left = NULL;
    new_node->right = NULL;

    if (parent == NULL) {
        root = new_node;
    } else if (strcmp(word, parent->word) < 0) {
        parent->left = new_node;
    } else {
        parent->right = new_node;
    }
}

/* In-order traversal of the BST to print words and their frequencies in sorted order.*/
void print_sorted_frequencies(struct word_node *node) {
    if (node == NULL) {
        return;
    }
    print_sorted_frequencies(node->left);
    printf("%-20s : %d\n", node->word, node->count);
    print_sorted_frequencies(node->right);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error opening file");
            return 1;
        }
        yyin = file;
    } else {
        printf("Please provide an input file (./a.out <filename>)\n");
        return 1;
    }
    yylex();
    printf("Word Frequencies\n");
    print_sorted_frequencies(root);
}

int yywrap() {
    return 1;
}