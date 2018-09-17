"""Setup tools based creation for pupil package using cython
"""
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    # Python 3
    MyFileNotFoundError = FileNotFoundError
except:  # FileNotFoundError does not exist in Python 2.7
    # Python 2.7
    # - open() raises IOError
    # - remove() (not currently used here) raises OSError
    MyFileNotFoundError = (IOError, OSError)

libname = "pupil"
build_type = "optimized"

SHORTDESC = "Pupil package extracted from pupil labs"

DESC = """Pupil package from pupil labs

Tested on Python 3.6
"""

# Directories (relative to the top-level directory where setup.py resides) in which to look for data files.
datadirs  = ("test",)

# File extensions to be considered as data files. (Literal, no wildcards.)
dataexts  = (".py",  ".pyx", ".pxd",  ".c", ".cpp", ".h",  ".sh",  ".lyx", ".tex", ".txt", ".pdf")

# Standard documentation to detect (and package if it exists).
#
standard_docs     = ["README", "LICENSE", "TODO", "CHANGELOG", "AUTHORS"]  # just the basename without file extension
standard_doc_exts = [".md", ".rst", ".txt", ""]  # commonly .md for GitHub projects, but other projects may use .rst or .txt (or even blank).

#########################################################
# Init
#########################################################

# check for Python 2.7 or later
# http://stackoverflow.com/questions/19534896/enforcing-python-version-in-setup-py
import sys
if sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')

import os
import platform

from setuptools import setup
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    sys.exit("Cython not found. Cython is needed to build the extension modules.")

try:
    import numpy as np
except ImportError:
    sys.exit("Numpy not found. Numpy is required to build the module")


# Modules involving numerical computations
#
extra_compile_args_math_optimized    = ['-march=native', '-O2', '-msse', '-msse2', '-mfma', '-mfpmath=sse', '-D_USE_MATH_DEFINES', '-std=c++11', '-w']
extra_compile_args_math_debug        = ['-march=native', '-O0', '-g', '-D_USE_MATH_DEFINES']
extra_link_args_math_optimized       = []
extra_link_args_math_debug           = []

# Modules that do not involve numerical computations
#
extra_compile_args_nonmath_optimized = ['-O2', '-std=c++11', '-w']
extra_compile_args_nonmath_debug     = ['-O0', '-g']
extra_link_args_nonmath_optimized    = []
extra_link_args_nonmath_debug        = []

# Additional flags to compile/link with OpenMP
#
openmp_compile_args = ['-fopenmp']
openmp_link_args    = ['-fopenmp']

## Setup dependencies
dependencies = []
# include all header files, to recognize changes
for dirpath, dirnames, filenames in os.walk("singleeyefitter"):
    for filename in [f for f in filenames if f.endswith(".h")]:
        dependencies.append( os.path.join(dirpath, filename) )

shared_cpp_include_path = 'pupil/shared_cpp/include'
singleeyefitter_include_path = 'pupil/detectors/singleeyefitter/'

opencv_libraries = ['opencv_core', 'opencv_highgui', 'opencv_videoio', 'opencv_imgcodecs', 'opencv_imgproc', 'opencv_video']
opencv_library_dir = '/usr/local/lib'
opencv_include_dir = '/usr/local/include'

# boost includes
boost_library_dir = '/usr/local/lib'
boost_include_dir = '/usr/local/include/boost'

python_version = sys.version_info
boost_lib = 'boost_python'+str(python_version[0])+str(python_version[1])

## Setup include directories
my_include_dirs = [".", np.get_include(), 
                   '/usr/local/include/eigen3',
                   '/usr/include/eigen3',
                   shared_cpp_include_path, singleeyefitter_include_path, 
                   opencv_include_dir, 
                   boost_include_dir]

# Choose the base set of compiler and linker flags.
#
if build_type == 'optimized':
    my_extra_compile_args_math    = extra_compile_args_math_optimized
    my_extra_compile_args_nonmath = extra_compile_args_nonmath_optimized
    my_extra_link_args_math       = extra_link_args_math_optimized
    my_extra_link_args_nonmath    = extra_link_args_nonmath_optimized
    my_debug = False
    print( "build configuration selected: optimized" )
elif build_type == 'debug':
    my_extra_compile_args_math    = extra_compile_args_math_debug
    my_extra_compile_args_nonmath = extra_compile_args_nonmath_debug
    my_extra_link_args_math       = extra_link_args_math_debug
    my_extra_link_args_nonmath    = extra_link_args_nonmath_debug
    my_debug = True
    print( "build configuration selected: debug" )
else:
    raise ValueError("Unknown build configuration '%s'; valid: 'optimized', 'debug'" % (build_type))


def declare_cython_extension(extName,sources=None,libraries=None, library_dirs=None, depends=None, use_math=False, use_openmp=False, include_dirs=None):
    """Declare a Cython extension module for setuptools.

Parameters:
    extName : str
        Absolute module name, e.g. use `mylibrary.mypackage.mymodule`
        for the Cython source file `mylibrary/mypackage/mymodule.pyx`.
    
    libraries : list of str
        List of libraries to link against

    library_dirs: list of str
        List of library directories

    use_math : bool
        If True, set math flags and link with ``libm``.

    use_openmp : bool
        If True, compile and link with OpenMP.

Return value:
    Extension object
        that can be passed to ``setuptools.setup``.
"""
    # extPath = extName.replace(".", os.path.sep)+".pyx"

    if use_math:
        compile_args = list(my_extra_compile_args_math) # copy
        link_args    = list(my_extra_link_args_math)
        # libraries    = ["ceres", boost_lib] + opencv_libaries  # this is a list of library names without the "lib" prefix
        # library_dirs = [opencv_library_dir]
        # depends = dependencies
    else:
        compile_args = list(my_extra_compile_args_nonmath)
        link_args    = list(my_extra_link_args_nonmath)
        libraries    = None  # value if no libraries, see setuptools.extension._Extension

    # OpenMP
    if use_openmp:
        compile_args.insert( 0, openmp_compile_args )
        link_args.insert( 0, openmp_link_args )
    
    extra_objects = []
    language = "c++"

    # See
    #    http://docs.cython.org/src/tutorial/external.html
    #
    # on linking libraries to your Cython extensions.
    #
    return Extension(name=extName,
                     sources=sources,
                     extra_compile_args=compile_args,
                     extra_link_args=link_args,
                     include_dirs=include_dirs,
                     libraries=libraries,
                     library_dirs=library_dirs,
                     extra_objects=extra_objects,
                     depends=depends,
                     language=language,
                     )

# Gather user-defined data files
#
# http://stackoverflow.com/questions/13628979/setuptools-how-to-make-package-contain-extra-data-folder-and-all-folders-inside
#
datafiles = []
getext = lambda filename: os.path.splitext(filename)[1]
for datadir in datadirs:
    datafiles.extend( [(root, [os.path.join(root, f) for f in files if getext(f) in dataexts])
                       for root, dirs, files in os.walk(datadir)] )


# Add standard documentation (README et al.), if any, to data files
#
detected_docs = []
for docname in standard_docs:
    for ext in standard_doc_exts:
        filename = "".join( (docname, ext) )  # relative to the directory in which setup.py resides
        if os.path.isfile(filename):
            detected_docs.append(filename)
datafiles.append( ('.', detected_docs) )


# Extract __version__ from the package __init__.py
# (since it's not a good idea to actually run __init__.py during the build process).
#
# http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
#
import ast
init_py_path = os.path.join(libname, '__init__.py')
version = '0.1'
# try:
#     with open(init_py_path) as f:
#         for line in f:
#             if line.startswith('__version__'):
#                 import pdb;pdb.set_trace()
#                 version = ast.parse(line).body[0].value.s
#                 break
#         else:
#             print( "WARNING: Version information not found in '%s', using placeholder '%s'" % (init_py_path, version), file=sys.stderr )
# except MyFileNotFoundError:
#     print( "WARNING: Could not find file '%s', using placeholder version information '%s'" % (init_py_path, version), file=sys.stderr )

#########################################################
# Set up modules
#########################################################

# declare Cython extension modules here

ext_module_methods = declare_cython_extension("pupil.methods",
                                              sources=['pupil/methods.pyx'],
                                              use_math=True,
                                              use_openmp=False,
                                              include_dirs=my_include_dirs)

ext_module_detector_2d = declare_cython_extension("pupil.detectors.detector_2d",
                                                  sources=['pupil/detectors/detector_2d.pyx', 'pupil/detectors/singleeyefitter/ImageProcessing/cvx.cpp', 'pupil/detectors/singleeyefitter/utils.cpp', 'pupil/detectors/singleeyefitter/detectorUtils.cpp'],
                                                  libraries=['ceres', boost_lib] + opencv_libraries,
                                                  library_dirs=[opencv_library_dir, boost_library_dir],
                                                  depends=dependencies,
                                                  use_math=True,
                                                  use_openmp=False,
                                                  include_dirs=my_include_dirs)

# detector 3d extension
ext_module_detector_3d = declare_cython_extension("pupil.detectors.detector_3d",
                                                  sources=['pupil/detectors/detector_3d.pyx',
                                                           'pupil/detectors/singleeyefitter/ImageProcessing/cvx.cpp',
                                                           'pupil/detectors/singleeyefitter/utils.cpp',
                                                           'pupil/detectors/singleeyefitter/detectorUtils.cpp',],
                                                           # 'pupil/detectors/singleeyefitter/EyeModelFitter.cpp',
                                                           # 'pupil/detectors/singleeyefitter/EyeModel.cpp'],
                                                  libraries=['ceres', boost_lib] + opencv_libraries,
                                                  library_dirs=[opencv_library_dir, boost_library_dir],
                                                  depends=dependencies,
                                                  use_math=True,
                                                  use_openmp=False,
                                                  include_dirs=my_include_dirs)


cython_ext_modules = [ext_module_methods,
                      ext_module_detector_2d,
                      ext_module_detector_3d]

my_ext_modules = cythonize(cython_ext_modules, include_path=my_include_dirs, gdb_debug=my_debug)

#########################################################
# Call setup()
#########################################################

setup(
    name = "pupil",
    version = version,
    author = "Shankar Kulumani",
    author_email = "shankar.kulumani@rockwellcollins.com",
    url = "",

    description = SHORTDESC,
    long_description = DESC,

    # CHANGE THIS
    license = "Unlicense",

    # free-form text field; http://stackoverflow.com/questions/34994130/what-platforms-argument-to-setup-in-setup-py-does
    platforms = ["Linux"],

    # See
    #    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    #
    # for the standard classifiers.
    #
    # Remember to configure these appropriately for your project, especially license!
    #
    classifiers = [ "Development Status :: 4 - Beta",
                    "Environment :: Console",
                    "Intended Audience :: Developers",
                    "Intended Audience :: Science/Research",
                    "License :: Unlicense",  # not a standard classifier; CHANGE THIS
                    "Operating System :: POSIX :: Linux",
                    "Programming Language :: Cython",
                    "Programming Language :: Python :: 3",
                    "Programming Language :: Python :: 3.6",
                    "Topic :: Scientific/Engineering",
                    "Topic :: Scientific/Engineering :: Mathematics",
                    "Topic :: Software Development :: Libraries",
                    "Topic :: Software Development :: Libraries :: Python Modules"
                  ],

    # See
    #    http://setuptools.readthedocs.io/en/latest/setuptools.html
    #
    setup_requires = ["cython", "numpy"],
    install_requires = ["numpy"],
    provides = ["pupil"],

    # keywords for PyPI (in case you upload your project)
    #
    # e.g. the keywords your project uses as topics on GitHub, minus "python" (if there)
    #
    keywords = ["setuptools cython"],

    # All extension modules (list of Extension objects)
    #
    ext_modules = my_ext_modules,

    # Declare packages so that  python -m setup build  will copy .py files (especially __init__.py).
    #
    # This **does not** automatically recurse into subpackages, so they must also be declared.
    #
    packages = ["pupil",],

    # Install also Cython headers so that other Cython modules can cimport ours
    #
    # Fileglobs relative to each package, **does not** automatically recurse into subpackages.
    #    
    # FIXME: force sdist, but sdist only, to keep the .pyx files (this puts them also in the bdist)
    package_data={'pupil': ['*.pxd', '*.pyx'],
                  },

    # Disable zip_safe, because:
    #   - Cython won't find .pxd files inside installed .egg, hard to compile libs depending on this one
    #   - dynamic loader may need to have the library unzipped to a temporary directory anyway (at import time)
    #
    zip_safe = False,

    # Custom data files not inside a Python package
    data_files = datafiles
)

if __name__=="__main__":
    setup()
