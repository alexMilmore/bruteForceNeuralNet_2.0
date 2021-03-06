import numpy as np

# Architectures are stored in the database as strings
# This is kinda gross, but gets the job done
#TODO maybe make this a little nicer
def textToArchitecture(text):
    architecture = [];
    layer = ['', '', ''];
    index = 0;

    for i in range(0, len(text)):
        if (text[i] == ','):
            index += 1;
            if index > 3:
                index = 0;
        elif (text[i] == '_'):
            architecture.append(layer);
            layer = ['', '', ''];
            index = 0;
        else:
            layer[index] += text[i];

    # fix layers that don't fit together
    architecture = fixConvDense(architecture);

    return architecture;

# Convolutional and dense layers need a flatten or reshape layer to fit the two
# together. This must be specified in architecture, as denseTo2D or convFlatten
def fixConvDense(architecture):

    for i in range(0, len(architecture) - 1):
                currentLayer = architecture[i];
                nextLayer = architecture[i+1];

                if currentLayer != nextLayer:
                    # Conv and dense layers need to be reshaped to fit together
                    if ('dense' in currentLayer[0]) and ('conv2D' in nextLayer[0]):
                        architecture[i][0] = 'denseTo2D';
                    elif ('conv' in currentLayer[0]) and ('dense' in nextLayer[0]):
                        # add flatten layer to convert from 2d conv to 1d dense
                        architecture.insert(i+1, ['flatten', '1', '1']);
                # resnet layers need the input to be the same shape as the layer
                    elif ('Res' not in currentLayer[0]) and ('Res' in nextLayer[0]):
                        if ('conv2D' in nextLayer[0]):
                            architecture.insert(i+1, ['conv2D', nextLayer[1], nextLayer[2]]);
                        if ('dense' in nextLayer[0]):
                            architecture.insert(i+1, ['dense', nextLayer[1], nextLayer[2]]);

    return architecture;

# A dictionary is used to assign different filenames to different catagories
# This is input to the SQL server as a string, this allows us to turn it into
# a dictionary
def textToDict(text):
    dict = {};
    textArr = text.split(",");
    print (textArr);

    for entry in textArr:
        relation = entry.split("=");
        print(relation)
        if (relation[1].isnumeric()):
            dict[relation[0]] = int(relation[1]);
        else:
            dict[relation[0]] = relation[1];

    return dict;
