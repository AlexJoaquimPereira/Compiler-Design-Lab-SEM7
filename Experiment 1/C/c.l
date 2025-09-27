/*include line numbers in source program*/
%{
#include <stdio.h>
int line_number = 0;
%}

%%
.*\n     { printf("%5d %s", ++line_number, yytext); }
%%

/* Take a filename as an argument */
int main(int argc, char *argv[]) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error opening file");
            return 1;
        }
        yyin = file;
    }

    yylex();
}

int yywrap() {
    return 0;
}