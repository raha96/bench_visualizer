from sys import argv
import re

if len(argv) != 3:
    print(f"Usage: {argv[0]} <input.bench> <output.dot>")
    exit(1)

#inpath = "c17_orig.bench"
#outpath = "c17_orig.gv"

inpath = argv[1]
outpath = argv[2]

fin = open(inpath, "r")
fout = open(outpath, "w")

fout.write('digraph "viz" {\n')

nets = set()
pios = set()
index = 0

for line in fin:
    line = line[:line.find("#")].strip()
    toks = re.findall(r'\b(\w+)\b', line)
    if len(toks) > 0:
        assert len(toks) > 1
        if len(toks) > 2:
            # Gate
            gin = toks[2:]
            gout = toks[0]
            gtype = toks[1]
            gname = f"gate{index}"
            for net0 in gin:
                fout.write(f"   {net0} -> {gname};\n")
                nets.add(net0)
            fout.write(f"   {gname} -> {gout};\n")
            fout.write(f'   {gname} [label="{gtype}" shape="rectangle"];\n')
            nets.add(gout)
            index += 1
        else:
            # PIO
            net = toks[1]
            ntype = toks[0]
            fout.write(f'   {net} [label="{ntype[0]}" shape="circle"];\n')
            nets.add(net)
            pios.add(net)

hidden_nets = nets - pios

for net in hidden_nets:
    fout.write(f'   {net} [label="" shape="point"];\n')

fout.write("}\n")

fin.close()
fout.close()

