#include "aagReader.h"

AAGReader::AAGReader(string sourcePath)
{
    source.open(sourcePath.c_str());
    debug.open("aagComentado.txt");
}

Aig* AAGReader::readFile()
{
    //treating header
    source.getline(buf, 250, '\n');
    string s=buf;
    line.str(s);
    line >> word;

    if(strcmp("aag",word.c_str())!=0)
    {
        qDebug() << "the file is not an AAG file!";
        return NULL;
    }

    int nNodes, nInputs, nFFs, nOutputs, nAnds;
    line >> word;
    nNodes = atoi(word.c_str());
    line >> word;
    nInputs = atoi(word.c_str());
    line >> word;
    nFFs = atoi(word.c_str());
    line >> word;
    nOutputs = atoi(word.c_str());
    line >> word;
    nAnds = atoi(word.c_str());

    if (nNodes != nInputs + nFFs + nAnds) {
        qDebug() << "Wrong file header";
        return NULL;
    }

    if (nFFs != 0) {
        qDebug() << "FF not supported yet";
        return NULL;
    }

    debug << s << "\nThe file header is ok!\n\n";

    AigNode nodes[nNodes + 1];
    AigNode outs[nOutputs];
    AigNode ins[nInputs];

    //treating inputs
    for (int i = 0; i < nInputs; i++) {
        debug << "read the input" << i << " from the file\n";
        debug << "   create in" << i << " and add it to an input list and the all nodes list\n";
    }

    //treating outputs
    debug << "\n";
    for (int i = 0; i < nOutputs; i++) {
        debug << "read the output" << i << " from the file\n";
        debug << "   create out" << i << " and add it to an output list and the all nodes list\n";
    }

    //connecting ands
    debug << "\n";
    for (int i = 0; i < nAnds; i++) {
        debug << "read the and" << i << " output and inputs\n";
        debug << "   connect the and" << i << " and set the inversion of this pins\n";
    }

    int i=0;
    debug << "\n";
    while(source)
    {
        source.getline(buf, 250, '\n');
        s=buf;
        line.seekg(0);line.str(s);
        line >> word;

        if(strcmp("c",word.substr(0).c_str())==0){
            debug << "the comments began. Ignore the file from here!\n";
            break;
        } else if(strcmp(word.substr(0).c_str(),"i")==0){

        } else if(strcmp(word.substr(0).c_str(),"o")==0){

        } else if(strcmp(word.substr(0).c_str(),"l")==0){

        }
    }

    debug << "\ncreate the AIG and add all nodes\n";
    debug << "return the AIG";

    return NULL;
}
