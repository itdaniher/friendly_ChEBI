### Friendly-ChEBI

#### Introduction

"Chemical Entities of Biological Interest (ChEBI) is a freely available dictionary of molecular entities focused on ‘small’ chemical compounds."

`friendly_ChEBI` is a project to make this archive of organic compounds trivially usable for both interactive lookups and programmatic (API) access with the
intent of facilitating new applications and reference resources.

The main purpose of this project is to serve as a chemical reference, allowing the end user to quickly check molecular mass and chemical structure from a
command line environment. The [whoosh](https://whoosh.readthedocs.io) project is used for ChEBI indexing and search. The
[docopt-ng](https://github.com/bazaar-projects/docopt-ng) project is used for the command line interface and documentation.


#### Usage:

To get you started fast, a recent copy of ChEBI is contained in this repo.
To use it, you'll need to install dependencies and build an index.

##### Setup:

``` bash
sudo apt install python3-pip
sudo pip3 install pipenv
pipenv install .
pipenv run build_index
pipenv search [options] (KEYWORDS...)
```

##### Searching:

For convenience, `search.py` can be invoked as `pipenv run search`.

```
Usage:
    search.py --field_help
    search.py [options] (KEYWORDS...)

Options:
    --search FIELD      Column to search. [default: names]
    --max_count COUNT   Maximum number of results to return. [default: 10]
    --sort_by FIELD     Sort results by this field name. [default: mass]
    --postfix_glob G    Use provided keyword as start of query. Appends G. [default: *]
    --prefix_glob G     Preface keyword with G for glob searching.
    --no_glob           Disables globbing.
    --index PATH        Specify path to the index made by ChEBI_Indexer.py. [default: index]
    --field_help        Returns available fieldnames for searching and sorting.
```

#### Examples

```
 $ pipenv run search methylene blue
<Top 10 Results for And([Term('names', 'methylene'), Term('names', 'blue')]) runtime=0.014890465012285858>
<Hit {'CAS': '', 'ChEBI': 43830, 'InChI': 'InChI=1S/C16H18N3S/c1-18(2)11-5-7-13-15(9-11)20-16-10-12(19(3)4)6-8-14(16)17-13/h5-10H,1-4H3/q+1', 'InChIKey': 'RBTBFTRPCNLSDE-UHFFFAOYSA-N', 'SMILES': 'CN(C)c1ccc2nc3ccc(cc3[s+]c2c1)N(C)C', 'charge': 1, 'definition': "An organic cation that is phenothiazin-5-ium substituted by dimethylamino groups at positions 3 and 7. The chloride salt is the histological dye 'methylene blue'.", 'formula': 'C16H18N3S', 'mass': 284.40034, 'names': '3,7-bis(dimethylamino)phenothiazin-5-ium; 3,7-bis(dimethylamino)phenothiazin-5-ium; methylene blue cation'}>
<Hit {'CAS': '613-11-6', 'ChEBI': 134180, 'InChI': 'InChI=1S/C16H19N3S/c1-18(2)11-5-7-13-15(9-11)20-16-10-12(19(3)4)6-8-14(16)17-13/h5-10,17H,1-4H3', 'InChIKey': 'QTWZICCBKBYHDM-UHFFFAOYSA-N', 'SMILES': 'CN(C)C=1C=CC2=C(C1)SC=3C=C(C=CC3N2)N(C)C', 'charge': 0, 'definition': 'A member of the class of phenothiazines that is 10<element>H</element>-phenothiazine in which the ring hydrogens at positions 3 and 7 have been replaced by dimethylamino groups.', 'formula': 'C16H19N3S', 'mass': 285.409, 'names': 'leucomethylene blue; N(3),N(3),N(7),N(7)-tetramethyl-10H-phenothiazine-3,7-diamine; Panatone; Reduced methylene blue'}>
<Hit {'CAS': '61-73-4', 'ChEBI': 6872, 'InChI': 'InChI=1S/C16H18N3S.ClH/c1-18(2)11-5-7-13-15(9-11)20-16-10-12(19(3)4)6-8-14(16)17-13;/h5-10H,1-4H3;1H/q+1;/p-1', 'InChIKey': 'CXKWCBBOMKCUKX-UHFFFAOYSA-M', 'SMILES': '[Cl-].CN(C)c1ccc2nc3ccc(cc3[s+]c2c1)N(C)C', 'charge': 0, 'definition': 'An organic chloride salt having 3,7-bis(dimethylamino)phenothiazin-5-ium as the counterion. A commonly used dye that also exhibits antioxidant, antimalarial, antidepressant and cardioprotective properties.', 'formula': 'C16H18N3S.Cl', 'mass': 319.852, 'names': 'methylene blue; 3,7-bis(dimethylamino)phenothiazin-5-ium chloride; Basic Blue 9; C.I. 52015; Methylenblau; Methylene Blue anhydrous; Methylene blue; Methylthioninium chloride; Solvent blue 8; Swiss blue; azul de metileno; bleu de methylene'}>
```

```
 $ pipenv run search --prefix_glob '*' --max_count 5 tryptamine
<Top 5 Results for Wildcard('names', '*tryptamine*') runtime=3.3186410569906>
<Hit {'CAS': '61-54-1', 'ChEBI': 16765, 'InChI': 'InChI=1S/C10H12N2/c11-6-5-8-7-12-10-4-2-1-3-9(8)10/h1-4,7,12H,5-6,11H2', 'InChIKey': 'APJYDQYYACXCRM-UHFFFAOYSA-N', 'SMILES': 'NCCc1c[nH]c2ccccc12', 'charge': 0, 'definition': 'An aminoalkylindole consisting of indole having a 2-aminoethyl group at the 3-position.', 'formula': 'C10H12N2', 'mass': 160.2157, 'names': 'tryptamine; 2-(1H-indol-3-yl)ethanamine; 1H-indole-3-ethanamine; 2-(1H-INDOL-3-YL)ETHANAMINE; 2-(3-indolyl)ethylamine; 3-(2-Aminoethyl)indole; Tryptamine'}>
<Hit {'CAS': '', 'ChEBI': 57887, 'InChI': 'InChI=1S/C10H12N2/c11-6-5-8-7-12-10-4-2-1-3-9(8)10/h1-4,7,12H,5-6,11H2/p+1', 'InChIKey': 'APJYDQYYACXCRM-UHFFFAOYSA-O', 'SMILES': '[NH3+]CCc1c[nH]c2ccccc12', 'charge': 1, 'definition': 'An  ammonium ion that is the conjugate acid of tryptamine arising from protonation of the primary amino group; major species at pH 7.3.', 'formula': 'C10H13N2', 'mass': 161.2231, 'names': 'tryptaminium; 2-(1H-indol-3-yl)ethanaminium; tryptamine; tryptaminium cation; tryptaminium(1+)'}>
<Hit {'CAS': '61-49-4', 'ChEBI': 28136, 'InChI': 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3', 'InChIKey': 'NCIKQJBVUNUXLW-UHFFFAOYSA-N', 'SMILES': 'CNCCc1c[nH]c2ccccc12', 'charge': 0, 'definition': '', 'formula': 'C11H14N2', 'mass': 174.2423, 'names': 'N-methyltryptamine; 2-(1H-indol-3-yl)-N-methylethanamine; 3-(2-methylaminoethyl)indole; N(omega)-methyltryptamine; N-Methyltryptamine; N-methyl-1H-indole-3-ethanamine; N-monomethyltryptamine'}>
...
```

#### An aside on SDF

SDF is a somewhat terrible format - it's a pseudo-heirarchical key-value mapping with objects separated by a the "$$$$" string. Originally designed to distribute [Molfile](http://en.wikipedia.org/wiki/Molfile) connection table information, EBI made use of associated data functionality to distribute a large amount of incredibly useful molecular metadata in addition to the standard table.

The only parser I could find for the SDF format was part of the overcomplicated [OpenBabel](http://openbabel.org) project. I wanted to play with the information contained in the ChEBI database, but didn't want to deal with an absurdly complex program to get at it. An hour or four and a bit of Python later and I had a beautiful, albiet large, 22k element list of dictionaries.


