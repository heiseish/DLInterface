from setuptools import setup, find_packages, Extension
from Cython.Build import build_ext

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
        extra_compile_args=["-O3", "-std=c++17"],
        language="c++"
    ),
    Extension(
        "src.utils.color",
        sources=["src/utils/color.pyx"],
        extra_compile_args=["-O3"],
        language="c++"
    ),
]

setup(
    name='DawnPy',
    cmdclass=cmdclass,
    packages=find_packages(),
    include_package_data=True,
    package_data = { 
        'src.utils.logger': ['src/utils/logger.pxd'],
        'src.utils.color': ['src/utils/color.pxd'],
    },
    ext_modules=extensions,
)

