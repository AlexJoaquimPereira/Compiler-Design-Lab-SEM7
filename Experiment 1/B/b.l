/* Comvert decimal to hex*/
%{
#include <stdio.h>
#include <stdlib.h>
%}

%%
[0-9]+   {printf("Hexadecimal of %s is %X\n", yytext, atoi(yytext));}

.|\n     { ECHO; }

%%

int main() {
    printf("Enter decimal numbers:\n");
    yylex();
}

int yywrap() {
    return 0;
}