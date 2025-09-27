/*compute avg of given numbers*/
%{
#include <stdio.h>
#include <stdlib.h>

double sum = 0;
int count = 0;
%}

%%
[0-9]+(\.[0-9]+)?   {
                        sum += atof(yytext);
                        count++;
                    }

[ \t\n]+            ;

.                   ;

%%

/* Main function to run the lexer */
int main() {
    printf("Enter numbers separated by spaces (CTRL+D to calc avg):\n");
    yylex();
}


int yywrap() {
    if (count > 0) {
        printf("\n--------------------------------\n");
        printf("Average of %d numbers is: %f\n", count, sum / count);
        printf("--------------------------------\n");
    } else {
        printf("\nNo numbers were entered.\n");
    }
    return 0;
}