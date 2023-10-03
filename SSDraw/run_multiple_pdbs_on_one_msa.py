"""
Reads in helper script to run SSDraw for multiple PDBs and one multiple sequence alignment
Then combines images into a single image

Example:
python run_multiple_pdbs_on_one_msa.py -i example_run.txt -o output
"""
import sys
import os
from PIL import Image
import argparse

def combine_images(imgs):

    height = min([img.height for img in imgs])
    width = min([img.width for img in imgs])
    pic = Image.new('RGB', (width, height*len(imgs)))

    height_i = 0

    for img in imgs:
        x = img.crop((0,0,width,height))
        pic.paste(x, (0, height_i))
        height_i+=height
    return pic


def get_args():
    parser_description="A helper script to run SSDraw for multiple PDBs from a single multiple sequence alignment."
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = parser_description,
        epilog="")
    parser.add_argument("-i", "--input", help="name of input script")
    parser.add_argument("-o","--output", help="name of output image")
    
    args = parser.parse_args()
    return args, parser

def main():
    
    args,parser = get_args()

    ssdraw_params = {
        "FASTA": [],
        "PDB": [],
        "NAME": [],
        "OUTPUT": [],
        "ADDITIONAL_PARAMS": []
    }

    with open(args.input, "r") as f:
        lines = f.readlines()

    current_param = ""
    read_state = False

    for line in lines:
        words = line.split()

        if len(words) > 0:

            if words[0] in ssdraw_params.keys():
                current_param = words[0]
                continue

            if words[0] == "{":
                read_state = True
                continue
            
            if words[0] == "}":
                read_state = False
                current_param = ""
            
            if words[0][0] == "#":
                continue

            if current_param != "" and read_state:
                ssdraw_params[current_param].append(line.strip())

            

    # check if pdbs, names, and outputs are the same length

    if len(ssdraw_params["PDB"]) != len(ssdraw_params["NAME"]) or len(ssdraw_params["PDB"]) != len(ssdraw_params["OUTPUT"]):
        raise Exception("Number of options in PDB, NAME, and OUTPUT sections must be the same")
    

    # make dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    fasta = ssdraw_params["FASTA"][0]
    additional_params = " ".join(ssdraw_params["ADDITIONAL_PARAMS"])
    imgs = []
    for i in range(len(ssdraw_params["PDB"])):

        pdb = ssdraw_params["PDB"][i]
        name = ssdraw_params["NAME"][i]
        output = args.output+"/"+ssdraw_params["OUTPUT"][i]

        ssdraw_command = "python SSDraw.py -f {:} -p {:} -n {:} -o {:} {:}".format(fasta, pdb, name, output, additional_params)
        os.system(ssdraw_command)
        imgs.append(Image.open(output+".png"))
        
    print("Creating composite image {:}/{:}.png".format(args.output,args.output))
    combine_images(imgs).save("{:}/{:}.png".format(args.output,args.output))
    

if __name__ == '__main__':
    main()
