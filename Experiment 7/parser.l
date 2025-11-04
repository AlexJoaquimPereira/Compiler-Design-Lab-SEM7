%{
/*
 * This is the Lexer (Scanner) file.
 * It's responsible for reading the input and generating tokens
 * (e.g., INT, FLOAT, ID, NUMBER) for YACC to parse.
 */
#include <stdio.h>
#include <stdlib.h>
#include "y.tab.h"

extern YYSTYPE yylval;
void yyerror(const char *s);

%}

ID     [a-zA-Z_][a-zA-Z0-9_]*
NUMBER [0-9]+

%%
"int"       { return T_INT; }
"float"     { return T_FLOAT; }

{ID}        { return T_ID; }
{NUMBER}    { 
              yylval.int_val = atoi(yytext); 
              return T_NUMBER; 
            }

[ \t]       { /* Skip whitespace */ }

\n          { yylineno++; }

.           { return yytext[0]; }

%%

int yywrap() {
    return 1;
}
