%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

struct hash_node {
    char *word;
    int count;
    struct hash_node *next;
};

#define HASH_TABLE_SIZE 10000
struct hash_node *hash_table[HASH_TABLE_SIZE] = {NULL};

unsigned long hash_function(const char *str);
void hash_insert(const char *word);
void print_sorted_results();
int compare_nodes(const void *a, const void *b);

%}

%%

[a-zA-Z]+ {
    for (int i = 0; yytext[i]; i++) {
        yytext[i] = tolower(yytext[i]);
    }
    hash_insert(yytext);
}

.|\n      { /* Do nothing */ }

%%

unsigned long hash_function(const char *str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return hash % HASH_TABLE_SIZE;
}

void hash_insert(const char *word) {
    unsigned long index = hash_function(word);
    struct hash_node *current = hash_table[index];

    while (current != NULL) {
        if (strcmp(current->word, word) == 0) {
            current->count++;
            return;
        }
        current = current->next;
    }

    struct hash_node *new_node = (struct hash_node*) malloc(sizeof(struct hash_node));
    new_node->word = strdup(word);
    new_node->count = 1;
    new_node->next = hash_table[index];
    hash_table[index] = new_node;
}

int compare_nodes(const void *a, const void *b) {
    struct hash_node *node_a = *(struct hash_node **)a;
    struct hash_node *node_b = *(struct hash_node **)b;
    return strcmp(node_a->word, node_b->word);
}

void print_sorted_results() {
    int total_unique_words = 0;
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        for (struct hash_node *current = hash_table[i]; current != NULL; current = current->next) {
            total_unique_words++;
        }
    }

    if (total_unique_words == 0) return;

    struct hash_node **sorted_list = malloc(total_unique_words * sizeof(struct hash_node*));
    int k = 0;
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        for (struct hash_node *current = hash_table[i]; current != NULL; current = current->next) {
            sorted_list[k++] = current;
        }
    }

    qsort(sorted_list, total_unique_words, sizeof(struct hash_node*), compare_nodes);

    printf("\nWord Frequencies (from Hash Map)\n");
    for (int i = 0; i < total_unique_words; i++) {
        printf("%-20s : %d\n", sorted_list[i]->word, sorted_list[i]->count);
    }
    free(sorted_list);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) { perror("Error opening file"); return 1; }
    } else {
        printf("Usage: ./a.out <filename>\n"); return 1;
    }
    yylex();
    print_sorted_results();
    return 0;
}

int yywrap() {
    return 1;
}