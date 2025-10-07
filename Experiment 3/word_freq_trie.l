%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define ALPHABET_SIZE 26

struct trie_node {
    struct trie_node *children[ALPHABET_SIZE];
    int word_count;
};

struct trie_node *root = NULL;

struct trie_node* create_node();
void insert_word(const char *word);
void print_sorted_results(struct trie_node *node, char *prefix, int level);

%}

%%

[a-zA-Z]+ {
    for (int i = 0; yytext[i]; i++) {
        yytext[i] = tolower(yytext[i]);
    }
    insert_word(yytext);
}

.|\n      { /* Do nothing */ }

%%
struct trie_node* create_node() {
    struct trie_node *new_node = (struct trie_node*) malloc(sizeof(struct trie_node));
    if (new_node) {
        new_node->word_count = 0;
        for (int i = 0; i < ALPHABET_SIZE; i++) {
            new_node->children[i] = NULL;
        }
    }
    return new_node;
}

void insert_word(const char *word) {
    if (root == NULL) {
        root = create_node();
    }
    struct trie_node *crawler = root;
    for (int i = 0; word[i] != '\0'; i++) {
        int index = word[i] - 'a';
        if (crawler->children[index] == NULL) {
            crawler->children[index] = create_node();
        }
        crawler = crawler->children[index];
    }
    crawler->word_count++;
}

void print_sorted_results(struct trie_node *node, char *prefix, int level) {
    if (node == NULL) return;
    if (node->word_count > 0) {
        prefix[level] = '\0';
        printf("%-20s : %d\n", prefix, node->word_count);
    }
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i] != NULL) {
            prefix[level] = 'a' + i;
            print_sorted_results(node->children[i], prefix, level + 1);
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Error opening file");
            return 1;
        }
    } else {
        printf("Usage: ./a.out <filename>\n");
        return 1;
    }
    yylex();
    char prefix_buffer[100];
    printf("\nWord Frequencies (from Trie)\n");
    print_sorted_results(root, prefix_buffer, 0);

    return 0;
}

int yywrap() {
    return 1;
}