%{
#include <stdio.h>
#include "y.tab.h"

/* Keep track of the line number for error reporting */
extern int yylineno;
%}

ID     [a-zA-Z_][a-zA-Z0-9_]*
NUMBER [0-9]+

%%
"for"   { return FOR; }

{ID}    { return ID; }
{NUMBER} { return NUMBER; }

"=="    { return T_EQ; }
"!="    { return T_NEQ; }
"<="    { return T_LTE; }
">="    { return T_GTE; }

"++"    { return T_INC; }
"--"    { return T_DEC; }

[ \t]   { /* Skip whitespace */ }

\n      { yylineno++; }

"//".* { /* Ignore single-line comment */ }
"/*"([^*]|(\*+[^*/]))*\*+"/" { /* Ignore multi-line comment */ }

.       { return yytext[0]; }

%%

int yywrap() {
    return 1;
}
