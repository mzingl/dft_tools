.. _vaspio:

VASP input-output
#################

The following VASP files are used by PLOtools:
  * PROJCAR, LOCPROJ: raw projectors generated by VASP-PLO interface (VASP version >= 5.4.1)
  * EIGENVAL: Kohn-Sham eigenvalues as well as `k`-points with weights and Fermi weights
  * IBZKPT: `k`-point data (:math:`\Gamma`)
  * POSCAR: crystal structure data

Starting from version 5.4.1 VASP now supports an official output of various types of
projectors that are requested in INCAR by specifying a set of sites, orbitals and types
of projectors. The calculated projectors are output into files **PROJCAR** and **LOCPROJ**.
The difference between these two files is that **LOCPROJ** contains raw matrices without
any reference to sites/orbitals, while **PROJCAR** is more detailed on that.
In particular, the information that can be obtained for each projector from **PROJCAR** is the following:

  * site (and species) index
  * for each `k`-point and band: a set of complex numbers for labeled orbitals

At the same time, **LOCPROJ** contains the total number of projectors (as well as the
number of `k`-points, bands, and spin channels) in the first line,
which can be used to allocate the arrays before parsing.

To enhance the performance of the parser, it is implemented in plain C. The idea is
that the python part of the parser first reads the first line of **LOCPROJ** and
then calls the C-routine with necessary parameters to parse **PROJCAR**.

The projectors are read in and stored in class `Plocar`. Two major data structures are stored:

  * complex array `plo = nd.array((nproj, nspin, nk, nband))`
  * list of projector descriptors `proj_params` containing the information on
    the character of projectors

When a ProjectorShell is initialized it copies a subset of projectors corresponding
to selected sites/orbitals. This can be done by looping all shell sites/orbitals and
searching for the corresponding projector using the descriptor list `proj_params`.

