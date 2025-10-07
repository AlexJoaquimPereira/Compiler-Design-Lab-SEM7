%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_WORDS 5000
#define MAX_WORD_LEN 50

struct word_entry {
    char word[MAX_WORD_LEN];
    int count;
};

struct word_entry word_list[MAX_WORDS];
int unique_word_count = 0;

void add_word(char *word);
int compare_words(const void *a, const void *b);
%}

%%

[a-zA-Z]+ {
    for (int i = 0; yytext[i]; i++) {
        yytext[i] = tolower(yytext[i]);
    }
    add_word(yytext);
}

.|\n      { /* Do nothing */ }

%%
void add_word(char *word) {
    for (int i = 0; i < unique_word_count; i++) {
        if (strcmp(word, word_list[i].word) == 0) {
            word_list[i].count++;
            return;
        }
    }

    if (unique_word_count < MAX_WORDS) {
        strcpy(word_list[unique_word_count].word, word);
        word_list[unique_word_count].count = 1;
        unique_word_count++;
    }
}

int compare_words(const void *a, const void *b) {
    struct word_entry *word_a = (struct word_entry *)a;
    struct word_entry *word_b = (struct word_entry *)b;
    return strcmp(word_a->word, word_b->word);
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
    qsort(word_list, unique_word_count, sizeof(struct word_entry), compare_words);
    printf("\nWord Frequencies (Sorted)\n");
    for (int i = 0; i < unique_word_count; i++) {
        printf("%-20s : %d\n", word_list[i].word, word_list[i].count);
    }

    return 0;
}

int yywrap() {
    return 1;
}