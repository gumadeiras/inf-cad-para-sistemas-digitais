
#include <cstdlib>
#include <iostream>
#include "gerentebdd.h"

using namespace std;

int main(int argc, char *argv[])
{
    gerentebdd g;
    set<string> conjunto_variaveis;
    if(argc != 3){
      cout << "Please provide two expressions to compare" << endl;
      return EXIT_FAILURE;
    }
    string expr1 = argv[1];
    string expr2 = argv[2];
    nodobdd *nd1=g.create_from_equation(expr1, conjunto_variaveis);
    nodobdd *nd2=g.create_from_equation(expr2, conjunto_variaveis);
    // nodobdd *c=g.create_from_equation("c", conjunto_variaveis);
    // nodobdd *nd3=g.cofactor(nd1, c, '+');
    // nodobdd *nd4=g.cofactor(nd2, c, '-');
    if (nd1==nd2)
       {
       cout<<"as duas expr sao iguais"<<endl;
       cout<<expr1<<endl;
       cout<<expr2<<endl;
       }
    // system("PAUSE");
    return EXIT_SUCCESS;
}
