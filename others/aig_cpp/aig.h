#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <fstream>
#include <sstream>
#include <set>

using namespace std;

class AigNode
        {
        
public: 
        //virtual ~nodoaig()=0;
        //virtual void xxx()=0;
        };

class AndNode:public AigNode{
    int i0;
    int i1;
    int saida;

public:
    AndNode(int, int, int);
    //void imprime(ostream& saida);
    friend class Aig;  //sera que precisa?
};


class InputNode:public AigNode{
    int saida;
public:
    InputNode(int);
    //void imprime(ostream& saida);
    friend class Aig;  //sera que precisa?
};

class OutputNode:public AigNode{
    int i0;

public:
    OutputNode(int);
    //void imprime(ostream& saida);
    friend class Aig;  //sera que precisa?
};



class Aig{
      int ni;
      int no; 
      int maxvar_index;
      int nl;
      int na;
      map<int,AigNode*> nodos; //deve conter todos os nodos and e entradas
      map<int,AigNode*> saidas; //deve conter todas as saidas
      //alternativas ao map:
      //a1) o map poderia ser um vetor?
      //a2) poderia ser sem vetor e sem map, mas ser uma netlist onde existe
      //um vetor ou lista para cada rede?
      //a3) botar uma lista de consumidores da saidas dentro da propria and
public:
      bool insert(AndNode *);
      bool insert(InputNode *);
      bool insert(OutputNode *);
      
      };
