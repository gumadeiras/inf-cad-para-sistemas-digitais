#include <cstdlib>
#include "aagReader.h"

using namespace std;


int main()
{
    AAGReader reader("C17.aag");
    reader.readFile();

    return EXIT_SUCCESS;
}








