/*Identify whether the input is int, real num, word*/
%{
#include <stdio.h>
%}

%%

[0-9]+\.[0-9]+     { printf("'%s' is a real number\n", yytext); }
[0-9]+             { printf("'%s' is an integer\n", yytext); }
[a-zA-Z]+          { printf("'%s' is a word\n", yytext); }

%%

int main() {
    printf("Enter a string (real num, int, word):\n");
    yylex();
}

int yywrap(void) {
    return 0;
}