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

int main() {
    printf("Enter numbers separated by spaces (CTRL+D to calc avg):\n");
    yylex();

    if (count > 0) {
        printf("\nAverage of %d numbers is: %f\n", count, sum / count);
    } else {
        printf("\nNo numbers were entered.\n");
    }

    return 0;
}

int yywrap() {
    return 1;
}