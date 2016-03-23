#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

import numpy
from pyscf import gto
from pyscf import scf

'''
Control the SCF procedure by different initial guess.
'''

mol = gto.Mole()
mol.build(
    verbose = 5,
    output = None,
    symmetry = 'D2h',
    atom = [['Cr',(0, 0, 0)], ],
    basis = 'cc-pvdz',
    charge = 6,
    spin = 0,
)
mf = scf.RHF(mol)
mf.scf()
#
# use cation to produce initial guess
#
mo = mf.mo_coeff
rdm1 = (numpy.dot(mo[:,:15], mo[:,:15].T),
        numpy.dot(mo[:,:9 ], mo[:,:9 ].T))

mol.charge = 0
mol.spin = 6
mol.build(False,False)

mf = scf.RHF(mol)
mf.chkfile = 'cr_atom.chk'
mf.irrep_nelec = {'Ag': (6,3), 'B1g': (1,0), 'B2g': (1,0), 'B3g': (1,0)}
mf.scf(dm0=rdm1)


#
# the converged ROHF of small basis to produce initial guess for large basis
#
mol.basis = 'aug-cc-pvdz'
mol.build(False, False)
mf = scf.RHF(mol)
mf.level_shift = .2
mf.irrep_nelec = {'Ag': (6,3), 'B1g': (1,0), 'B2g': (1,0), 'B3g': (1,0)}
# init guess can also be read from chkfile
dm = mf.from_chk('cr_atom.chk')
mf.scf(dm)


#
# UHF is another way to produce initial guess
#
charge = 0
spin = 6
mol.basis = 'aug-cc-pvdz'
mol.build(False,False)

mf = scf.UHF(mol)
mf.irrep_nelec = {'Ag': (6,3), 'B1g': (1,0), 'B2g': (1,0), 'B3g': (1,0)}
mf.scf()
rdm1 = mf.make_rdm1()

mf = scf.RHF(mol)
mf.irrep_nelec = {'Ag': (6,3), 'B1g': (1,0), 'B2g': (1,0), 'B3g': (1,0)}
mf.scf(rdm1)
