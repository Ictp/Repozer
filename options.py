# -*- coding: utf-8 -*-
##
##
## This file is part of Indico
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN)
##
## Indico is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico.  If not, see <http://www.gnu.org/licenses/>.
from MaKaC.i18n import _

from indico.core.config import Config

globalOptions = [

    ("indexConference", {"description" : "Repozer will index Conferences",
               "type": bool,
               "defaultValue": True,
               "editable": True,
               "visible": True} ),

    ("indexContribution", {"description" : "Repozer will index Contributions",
               "type": bool,
               "defaultValue": True,
               "editable": True,
               "visible": True} ),

    ("indexMaterial", {"description" : "Repozer will index Materials",
               "type": bool,
               "defaultValue": False,
               "editable": True,
               "visible": True} ),

# This is for external DB
#    ("DBpath", {"description": "Repozer DB path",
#                  "type": str,
#                  "defaultValue": "/opt/indico/db/repoze_catalog.fs",
#                  "editable": True,
#                  "visible": True}),

]


# if you want to use a SINGLE catalog, just use the same name
confCatalog = 'rc_Event'
contribCatalog = 'rc_Contribution'
matCatalog = 'rc_Material'

availableKeywords = [
'NOSCICAL',
'Acceleratory Mass Spectroscopy',
'Aeronomy',
'Algebra',
'Analysis',
'Applicable Mathematics',
'Applied Physics',
'Atomic and Molecular Physics',
'Basic Notions',
'Biophysics',
'Biosciences',
'Climate Change and Impacts',
'Climatology and Meteorology',
'Colloquium',
'Computational Physics in Condensed Matter',
'Condensed Matter and Statistical Physics',
'Cosmology',
'Differential Equations',
'Digital Communications and Computer Networking',
'Dynamical systems',
'Earth System Physics',
'Ecological and Environmental Economics',
'Ecology',
'Education',
'Electronic Structure and Condensed Matter Computer Simulations',
'Energy Systems',
'Fibre Optics for Communications',
'Fluid Dynamics',
'Geometric Analysis',
'Geometry',
'High Energy Cosmology and Astroparticle Physics',
'ICTP-INFN Microprocessor Project',
'Information and Computer Technology',
'Instrumentation',
'LHC Physics',
'Lasers',
'Liquids and Statistical Mechanics',
'Materials Science',
'Mathematical Physics',
'Mathematics',
'Mechanics of Earthquakes and Tectonophysics',
'Medical Physics',
'Mesoscopic and Strongly Correlated Electron Systems',
'Miscellaneous',
'Multidisciplinary Laboratory',
'Natural Climate Variability and Predictability',
'Neurophysics',
'Non-Equilibrium Physics',
'Nonlinear Dynamics of the Earth',
'Nuclear Energy related technologies',
'Nuclear Physics',
'Optics and Laser Physics',
'Others',
'Phenomenology of Particle Physics',
'Physics and Biology, including Bio-Nano',
'Physics and Development',
'Physics and Energy',
'Physics in Industry',
'Physics of Nuclear Reactors',
'Physics of Weather and Climate',
'Physics of the Atmosphere',
'Physics of the Environment',
'Physics of the Living State',
'Physics of the Oceans',
'Plasma Focus Project',
'Plasma Physics (including Fusion)',
'Policy and Planning',
'Quantitative Life Sciences',
'Quantum Phenomena (including Quantum Computation)',
'Radiopropagation',
'Relativity, Cosmology and Astrophysics',
'Remote Access to Large Experimental Facilities',
'Renewable Energies',
'Salam Distinguished Lectures',
'Soil Physics',
'Solid Earth Geophysics',
'Solid State Physics',
'Statistical Mechanics and Applications',
'Strings and Higher Dimensional Theories',
'Synchrotron Radiation Related Theory',
'Topology',
'Water and Soil',
'X-ray Imaging'
] 