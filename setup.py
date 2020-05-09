from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy
from distutils.command.sdist import sdist as _sdist


cmdclass = {}
cmdclass.update({'build_ext': build_ext})

extensions = [
    Extension(
        "src.utils.logger",
        sources=["src/utils/logger.pyx"],
        extra_compile_args=["-O3"],
        language="c++"
    ),
    Extension(
        "src.model.DialoGPT",
        sources=["src/model/DialoGPT.pyx"],
        extra_compile_args=["-O3"],
        language="c++"
    ),
    Extension(
        "src.utils.context",
        sources=["src/utils/context.pyx"],
        extra_compile_args=["-O3"],
        language="c++"
    ),
]

class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        cythonize(extensions)
        _sdist.run(self)

cmdclass['sdist'] = sdist

setup(
    name='DawnPy',
    cmdclass=cmdclass,
    ext_modules=extensions,
)

